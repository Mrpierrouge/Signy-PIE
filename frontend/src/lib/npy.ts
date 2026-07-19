// Minimal writer for the NumPy .npy binary format (v1.0), just enough to
// serialize a 2D float32 array — no external dependency needed.
// Spec: https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html

const NPY_MAGIC = [0x93, 0x4e, 0x55, 0x4d, 0x50, 0x59] // "\x93NUMPY"
const HEADER_ALIGNMENT = 64

export function encodeNpyFloat32(data: Float32Array, shape: [number, number]): Blob {
  const dict = `{'descr': '<f4', 'fortran_order': False, 'shape': (${shape[0]}, ${shape[1]}), }`

  // Preamble = magic (6 bytes) + version (2 bytes) + header length field (2 bytes).
  // Total preamble+header length must be a multiple of HEADER_ALIGNMENT, and the
  // header itself must end with '\n'.
  const preambleLength = 10
  const unpaddedLength = preambleLength + dict.length + 1
  const paddedLength = Math.ceil(unpaddedLength / HEADER_ALIGNMENT) * HEADER_ALIGNMENT
  const header = dict + " ".repeat(paddedLength - unpaddedLength) + "\n"
  const headerBytes = new TextEncoder().encode(header)

  const buffer = new ArrayBuffer(preambleLength + headerBytes.length + data.byteLength)
  const view = new DataView(buffer)

  new Uint8Array(buffer, 0, 6).set(NPY_MAGIC)
  view.setUint8(6, 1) // major version
  view.setUint8(7, 0) // minor version
  view.setUint16(8, headerBytes.length, true)

  new Uint8Array(buffer, preambleLength, headerBytes.length).set(headerBytes)
  new Float32Array(buffer, preambleLength + headerBytes.length).set(data)

  return new Blob([buffer], { type: "application/octet-stream" })
}
