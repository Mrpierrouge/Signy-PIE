import { FilesetResolver, HolisticLandmarker } from "@mediapipe/tasks-vision"
import type { NormalizedLandmark } from "@mediapipe/tasks-vision"

// ── Assumed per-frame feature layout ────────────────────────────────────────
// backend/lsf_model.onnx was trained on "MediaPipe Holistic keypoint
// sequences" (per backend/ai_service.py's docstring), with feature_dim: 444
// (backend/model_meta.json). Nowhere in the repo is the exact composition of
// those 444 floats documented — this is a best-effort, clearly isolated
// guess. If predictions stay inconsistent once this pipeline runs without
// errors, this layout is the first thing to revisit.
//
//   pose (33 landmarks x [x, y, z, visibility])  = 132
//   left hand (21 landmarks x [x, y, z])         =  63
//   right hand (21 landmarks x [x, y, z])        =  63
//   face subset (62 landmarks x [x, y, z])        = 186
//                                                   ---
//                                                   444
const POSE_LANDMARK_COUNT = 33
const HAND_LANDMARK_COUNT = 21
const FACE_SUBSET_COUNT = 62
export const FEATURE_SIZE =
  POSE_LANDMARK_COUNT * 4 + HAND_LANDMARK_COUNT * 3 * 2 + FACE_SUBSET_COUNT * 3 // 444

const WASM_BASE_URL = "/mediapipe/wasm"
const MODEL_ASSET_PATH = "/mediapipe/models/holistic_landmarker.task"

/**
 * Builds the 62 face landmark indices used above, by sampling evenly across
 * HolisticLandmarker's own lips/eyebrows/eyes connector index sets (the
 * facial regions most relevant to LSF's non-manual markers), rather than
 * hand-typing landmark numbers from memory.
 */
function buildFaceSubsetIndices(): number[] {
  const regions = [
    HolisticLandmarker.FACE_LANDMARKS_LIPS,
    HolisticLandmarker.FACE_LANDMARKS_LEFT_EYEBROW,
    HolisticLandmarker.FACE_LANDMARKS_RIGHT_EYEBROW,
    HolisticLandmarker.FACE_LANDMARKS_LEFT_EYE,
    HolisticLandmarker.FACE_LANDMARKS_RIGHT_EYE,
  ]

  const pool: number[] = []
  const seen = new Set<number>()
  for (const region of regions) {
    for (const { start, end } of region) {
      if (!seen.has(start)) {
        seen.add(start)
        pool.push(start)
      }
      if (!seen.has(end)) {
        seen.add(end)
        pool.push(end)
      }
    }
  }

  return Array.from(
    { length: FACE_SUBSET_COUNT },
    (_, i) => pool[Math.round((i * (pool.length - 1)) / (FACE_SUBSET_COUNT - 1))],
  )
}

let landmarkerPromise: Promise<HolisticLandmarker> | null = null
let faceSubsetIndices: number[] | null = null

function loadLandmarker(): Promise<HolisticLandmarker> {
  if (!landmarkerPromise) {
    landmarkerPromise = FilesetResolver.forVisionTasks(WASM_BASE_URL).then((vision) =>
      HolisticLandmarker.createFromOptions(vision, {
        baseOptions: { modelAssetPath: MODEL_ASSET_PATH },
        runningMode: "VIDEO",
      }),
    )
  }
  return landmarkerPromise
}

/** Warm up the landmarker ahead of time so the first recording isn't stalled waiting for it. */
export function preloadHolisticExtractor(): void {
  void loadLandmarker()
}

function writeLandmarks(
  target: Float32Array,
  offset: number,
  landmarks: (NormalizedLandmark | undefined)[] | undefined,
  count: number,
  withVisibility: boolean,
): number {
  for (let i = 0; i < count; i++) {
    const landmark = landmarks?.[i]
    target[offset++] = landmark?.x ?? 0
    target[offset++] = landmark?.y ?? 0
    target[offset++] = landmark?.z ?? 0
    if (withVisibility) {
      target[offset++] = landmark?.visibility ?? 0
    }
  }
  return offset
}

export async function detectFrame(
  videoEl: HTMLVideoElement,
  timestampMs: number,
): Promise<Float32Array> {
  const landmarker = await loadLandmarker()
  if (!faceSubsetIndices) {
    faceSubsetIndices = buildFaceSubsetIndices()
  }

  const result = landmarker.detectForVideo(videoEl, timestampMs)

  const features = new Float32Array(FEATURE_SIZE)
  let offset = 0

  offset = writeLandmarks(features, offset, result.poseLandmarks[0], POSE_LANDMARK_COUNT, true)
  offset = writeLandmarks(features, offset, result.leftHandLandmarks[0], HAND_LANDMARK_COUNT, false)
  offset = writeLandmarks(features, offset, result.rightHandLandmarks[0], HAND_LANDMARK_COUNT, false)

  const faceLandmarks = result.faceLandmarks[0]
  const faceSubset = faceSubsetIndices.map((index) => faceLandmarks?.[index])
  writeLandmarks(features, offset, faceSubset, FACE_SUBSET_COUNT, false)

  return features
}
