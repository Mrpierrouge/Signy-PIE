export type Word = {
  id: number
  video: string
  string: string
}

export type AIWordResponse = {
  word: string
  confidence: number | null
  label: string
  true_label?: string
  matched_words: string[]
  is_valid: boolean
  message?: string | null
}
