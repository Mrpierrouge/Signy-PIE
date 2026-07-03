import type { Word } from "./word"

export type Lesson = {
  id: number
  title: string
  status: "locked" | "unlocked" | "completed"
}
export type LessonWithWords = Lesson & {
  words: Word[]
}
