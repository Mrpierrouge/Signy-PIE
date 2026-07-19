"""
AI service — LSF (Langue des Signes Française) word predictor.

The ONNX model was trained on MediaPipe Holistic keypoint sequences saved as
NumPy .npy files (shape: [T, F] where T = sequence length, F = feature size).

At inference time the client may send either:
  • A raw .npy file (preferred — already extracted keypoints)
  • A video blob (fallback — bytes are used as a hash to pick a label, since
    real MediaPipe extraction requires a full Python/OpenCV environment)
"""
from __future__ import annotations

import json
import io
import os
import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np

try:
    import onnxruntime as ort
except ImportError:  # pragma: no cover
    ort = None


DEFAULT_LABELS = [
    "France",
    "bonjour",
    "non",
    "orange couleur",
    "oui",
    "prénom",
    "sept",
    "sirène",
    "six",
    "âge",
]

LOGGER = logging.getLogger(__name__)

# Magic bytes that identify a NumPy .npy file
_NPY_MAGIC = b"\x93NUMPY"


def _softmax(values: np.ndarray) -> np.ndarray:
    shifted = values - np.max(values)
    exp_values = np.exp(shifted)
    return exp_values / np.sum(exp_values)


def _parse_labels(raw_labels: str | None) -> list[str]:
    if not raw_labels:
        return DEFAULT_LABELS
    labels = [label.strip() for label in raw_labels.split(",") if label.strip()]
    return labels or DEFAULT_LABELS


def _load_labels_from_meta(model_path: Path) -> list[str] | None:
    meta_path = model_path.with_name("model_meta.json")
    if not meta_path.exists():
        return None

    try:
        meta = json.loads(meta_path.read_text())
    except Exception as exc:  # pragma: no cover - defensive fallback
        LOGGER.warning("Failed to read model metadata from %s: %s", meta_path, exc)
        return None

    classes = meta.get("classes")
    if not isinstance(classes, list):
        return None

    labels = [str(label).strip() for label in classes if str(label).strip()]
    return labels or None


def _load_npy(data: bytes) -> np.ndarray | None:
    """Try to deserialise *data* as a NumPy array. Returns None on failure."""
    if not data.startswith(_NPY_MAGIC):
        return None
    try:
        return np.load(io.BytesIO(data), allow_pickle=False)
    except Exception:
        return None


@dataclass
class PredictionResult:
    word: str
    confidence: float | None = None


class VideoWordPredictor:
    def __init__(self) -> None:
        self.model_path = Path(os.getenv("AI_MODEL_PATH", "lsf_model.onnx"))
        meta_labels = _load_labels_from_meta(self.model_path)
        env_labels = _parse_labels(os.getenv("AI_LABELS"))
        self.labels = meta_labels or env_labels

        if meta_labels and env_labels != meta_labels:
            LOGGER.warning(
                "Using labels from %s instead of AI_LABELS because they differ from the model metadata.",
                self.model_path.with_name("model_meta.json"),
            )

        self.session = self._load_session()

    # ── Private ───────────────────────────────────────────────────────────────

    def _load_session(self):
        if ort is None or not self.model_path.exists():
            return None
        try:
            return ort.InferenceSession(
                str(self.model_path), providers=["CPUExecutionProvider"]
            )
        except Exception:
            return None

    def _expected_shape(self) -> tuple[int, int]:
        """Return (sequence_length, feature_size) from the loaded ONNX model."""
        shape = self.session.get_inputs()[0].shape  # e.g. [1, 30, 444]
        seq_len = int(shape[1]) if isinstance(shape[1], int) else 30
        feat_size = int(shape[2]) if isinstance(shape[2], int) else 444
        return seq_len, feat_size

    def _prepare_tensor(self, payload: bytes) -> np.ndarray:
        """
        Convert incoming bytes into a float32 tensor of shape [1, T, F].

        Priority:
          1. NumPy .npy keypoint array  → reshape / pad to [1, T, F]
          2. Raw bytes (video blob)     → treated as flat float data (fallback)
        """
        seq_len, feat_size = self._expected_shape()
        required = seq_len * feat_size

        npy_array = _load_npy(payload)
        if npy_array is not None:
            # Expected shape from training: (T, F)  or  (1, T, F)
            arr = npy_array.astype(np.float32).reshape(-1, feat_size)
            if arr.shape[0] < seq_len:
                # Pad along the time axis with zeros
                pad = np.zeros((seq_len - arr.shape[0], feat_size), dtype=np.float32)
                arr = np.vstack([arr, pad])
            # Truncate to exactly seq_len frames and add batch dim
            return arr[:seq_len].reshape(1, seq_len, feat_size)

        # Fallback: treat raw bytes as flat uint8 normalised to [0, 1]
        features = np.frombuffer(payload, dtype=np.uint8).astype(np.float32) / 255.0
        if features.size < required:
            features = np.pad(features, (0, required - features.size))
        return features[:required].reshape(1, seq_len, feat_size)

    # ── Public ────────────────────────────────────────────────────────────────

    def predict(self, payload: bytes) -> PredictionResult:
        """
        Predict the LSF word from *payload*.

        *payload* can be either:
          • A NumPy .npy file containing MediaPipe keypoints (preferred)
          • A raw video blob (the model will not be very accurate in this mode)
        """
        if not payload:
            raise ValueError("Empty payload")

        # No ONNX session → deterministic stub (useful for local dev / CI)
        if self.session is None:
            index = sum(payload) % len(self.labels)
            return PredictionResult(word=self.labels[index], confidence=None)

        input_name = self.session.get_inputs()[0].name
        tensor = self._prepare_tensor(payload)

        non_zero = int(np.count_nonzero(tensor))
        print(
            f"[predict] tensor shape={tensor.shape} non_zero={non_zero}/{tensor.size}"
            f" ({100.0 * non_zero / tensor.size:.1f}%)"
            f" min={tensor.min():.4f} max={tensor.max():.4f} mean={tensor.mean():.4f}",
            flush=True,
        )

        logits = self.session.run(None, {input_name: tensor})[0][0]
        probabilities = _softmax(np.asarray(logits, dtype=np.float32))
        print(f"[predict] probs={np.round(probabilities, 3)}", flush=True)
        index = int(np.argmax(probabilities))
        word = self.labels[index] if index < len(self.labels) else f"class_{index}"
        return PredictionResult(word=word, confidence=float(probabilities[index]))