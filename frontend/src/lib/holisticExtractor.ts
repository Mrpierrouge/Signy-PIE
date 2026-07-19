import { FilesetResolver, HolisticLandmarker } from "@mediapipe/tasks-vision"
import type { NormalizedLandmark } from "@mediapipe/tasks-vision"

// Feature layout matches the Python training extraction script exactly:
//   left_hand (21×3) | right_hand (21×3) | pose (33×3) | face (73×3) = 444
//
// - No visibility for pose (training used [x, y, z] only for all landmarks)
// - Face uses exact 73 landmark indices from training (lips, eyebrows, eyes, nose, contour)
// - Coordinates are shoulder-normalized per frame (see normalizeSequence)
// - Handedness follows camera perspective: left_hand = left side of image

const HAND_LANDMARK_COUNT = 21
const POSE_LANDMARK_COUNT = 33
const FACE_LANDMARK_COUNT = 73

export const FEATURE_SIZE = (HAND_LANDMARK_COUNT * 2 + POSE_LANDMARK_COUNT + FACE_LANDMARK_COUNT) * 3 // 444

// Exact 73 face landmark indices from the training extraction script
const FACE_LANDMARK_INDICES: readonly number[] = [
  // Lèvres extérieures
  61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291,
  // Lèvres intérieures
  78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308,
  // Sourcil gauche
  70, 63, 105, 66, 107,
  // Sourcil droit
  336, 296, 334, 293, 300,
  // Œil gauche
  33, 7, 163, 144, 145, 153, 154, 155, 133,
  // Œil droit
  362, 382, 381, 380, 374, 373, 390, 249, 263,
  // Nez
  1, 2, 5, 4, 6, 19, 94,
  // Contour du visage
  10, 338, 297, 332, 284, 251, 389, 356, 454, 127, 162, 21, 54, 103, 67, 109,
]

// Landmark order: [lh(0-20), rh(21-41), pose(42-74), face(75-147)]
// Shoulder indices within the global landmark array (pose starts at 42)
const SHOULDER_LEFT_FLOAT_IDX = (42 + 11) * 3 // landmark 53, float offset 159
const SHOULDER_RIGHT_FLOAT_IDX = (42 + 12) * 3 // landmark 54, float offset 162

const WASM_BASE_URL = "/mediapipe/wasm"
const MODEL_ASSET_PATH = "/mediapipe/models/holistic_landmarker.task"

let landmarkerPromise: Promise<HolisticLandmarker> | null = null

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

export function preloadHolisticExtractor(): void {
  void loadLandmarker()
}

function writeLandmarks(
  target: Float32Array,
  offset: number,
  landmarks: (NormalizedLandmark | undefined)[] | undefined,
  count: number,
): number {
  for (let i = 0; i < count; i++) {
    const lm = landmarks?.[i]
    target[offset++] = lm?.x ?? 0
    target[offset++] = lm?.y ?? 0
    target[offset++] = lm?.z ?? 0
  }
  return offset
}

/**
 * Shoulder-normalize a full sequence in place.
 * Matches _normalize() in the training extraction script:
 *   origin = midpoint of shoulders, scale = inter-shoulder distance.
 * Forward-fills the last valid shoulders when pose is absent on a frame.
 */
export function normalizeSequence(sequence: Float32Array, frameCount: number): void {
  let lastOriginX = 0,
    lastOriginY = 0,
    lastOriginZ = 0,
    lastScale = 0
  let hasLastShoulder = false

  for (let f = 0; f < frameCount; f++) {
    const base = f * FEATURE_SIZE
    const lsX = sequence[base + SHOULDER_LEFT_FLOAT_IDX]
    const lsY = sequence[base + SHOULDER_LEFT_FLOAT_IDX + 1]
    const lsZ = sequence[base + SHOULDER_LEFT_FLOAT_IDX + 2]
    const rsX = sequence[base + SHOULDER_RIGHT_FLOAT_IDX]
    const rsY = sequence[base + SHOULDER_RIGHT_FLOAT_IDX + 1]
    const rsZ = sequence[base + SHOULDER_RIGHT_FLOAT_IDX + 2]

    const detected = lsX !== 0 || lsY !== 0 || rsX !== 0 || rsY !== 0
    if (detected) {
      lastOriginX = (lsX + rsX) / 2
      lastOriginY = (lsY + rsY) / 2
      lastOriginZ = (lsZ + rsZ) / 2
      const dx = lsX - rsX,
        dy = lsY - rsY,
        dz = lsZ - rsZ
      lastScale = Math.sqrt(dx * dx + dy * dy + dz * dz) || 1
      hasLastShoulder = true
    } else if (!hasLastShoulder) {
      continue // no reference yet — skip this frame (leave as zeros)
    }

    for (let i = 0; i < FEATURE_SIZE; i += 3) {
      sequence[base + i] = (sequence[base + i] - lastOriginX) / lastScale
      sequence[base + i + 1] = (sequence[base + i + 1] - lastOriginY) / lastScale
      sequence[base + i + 2] = (sequence[base + i + 2] - lastOriginZ) / lastScale
    }
  }
}

export async function detectFrame(
  videoEl: HTMLVideoElement,
  timestampMs: number,
): Promise<Float32Array> {
  const landmarker = await loadLandmarker()
  const result = landmarker.detectForVideo(videoEl, timestampMs)

  const features = new Float32Array(FEATURE_SIZE)
  let offset = 0

  // Order: left_hand | right_hand | pose | face  (matches training script)
  // HolisticLandmarker leftHandLandmarks = hand on left side of image (camera perspective)
  // which matches training HandLandmarker handedness "Left" (camera perspective)
  offset = writeLandmarks(features, offset, result.leftHandLandmarks[0], HAND_LANDMARK_COUNT)
  offset = writeLandmarks(features, offset, result.rightHandLandmarks[0], HAND_LANDMARK_COUNT)
  offset = writeLandmarks(features, offset, result.poseLandmarks[0], POSE_LANDMARK_COUNT)

  const faceLandmarks = result.faceLandmarks[0]
  for (const idx of FACE_LANDMARK_INDICES) {
    const lm = faceLandmarks?.[idx]
    features[offset++] = lm?.x ?? 0
    features[offset++] = lm?.y ?? 0
    features[offset++] = lm?.z ?? 0
  }

  return features
}
