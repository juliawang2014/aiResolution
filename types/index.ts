export interface Goal {
  id: number
  title: string
  description?: string
  category?: string
  target_date?: string
  created_at: string
  updated_at: string
  progress_percentage: number
  status: string
  progress_entries: ProgressEntry[]
}

export interface ProgressEntry {
  id: number
  goal_id: number
  text: string
  progress_percentage?: number
  sentiment?: string
  key_insights?: string[]
  created_at: string
}

export interface DashboardStats {
  total_goals: number
  completed_goals: number
  active_goals: number
  average_progress: number
  goals_by_category: Record<string, number>
}

export interface GoalCreate {
  title: string
  description?: string
  category?: string
  target_date?: string
}

export interface ProgressUpdate {
  text: string
}