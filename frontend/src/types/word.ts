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
  matched_word_ids: number[]
  matched_words: string[]
  is_valid: boolean
  tested_word?: string | null
  message?: string | null
}

export type WordCorespondance = {
  id: number
  label: string
  words: number[]
  matched_words?: Word[]
}

