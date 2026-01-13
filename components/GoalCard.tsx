import { useState } from 'react'
import { Goal } from '../types'
import { ProgressUpdateModal } from './ProgressUpdateModal'
import { DeleteConfirmModal } from './DeleteConfirmModal'
import { format } from 'date-fns'

interface GoalCardProps {
  goal: Goal
  onGoalDeleted?: (goalId: number) => void
  onProgressUpdated?: (goalId: number) => void
}

export function GoalCard({ goal, onGoalDeleted, onProgressUpdated }: GoalCardProps) {
  const [showUpdateModal, setShowUpdateModal] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800'
      case 'active': return 'bg-blue-100 text-blue-800'
      case 'paused': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getProgressColor = (progress: number) => {
    if (progress >= 80) return 'bg-green-500'
    if (progress >= 50) return 'bg-blue-500'
    if (progress >= 25) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  const handleDelete = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/goals/${goal.id}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        setShowDeleteModal(false)
        if (onGoalDeleted) {
          onGoalDeleted(goal.id)
        }
      } else {
        const errorText = await response.text()
        console.error('Failed to delete goal:', response.status, errorText)
        alert(`Failed to delete goal: ${response.status} - ${errorText}`)
      }
    } catch (error) {
      console.error('Error deleting goal:', error)
      alert(`Error deleting goal: ${error}`)
    }
  }

  return (
    <>
      <div className="card hover:shadow-lg transition-shadow">
        <div className="flex justify-between items-start mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
              {goal.title}
            </h3>
          </div>
          <div className="flex items-center space-x-2 ml-4">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(goal.status)}`}>
              {goal.status}
            </span>
            <div className="relative">
              <button
                onClick={() => setShowDeleteModal(true)}
                className="delete-button"
                title="Delete goal"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        {goal.description && (
          <p className="text-gray-600 text-sm mb-4 line-clamp-3">
            {goal.description}
          </p>
        )}

        {goal.category && (
          <div className="mb-4">
            <span className="inline-block bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">
              {goal.category}
            </span>
          </div>
        )}

        {/* Progress Bar */}
        <div className="mb-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Progress</span>
            <span className="text-sm text-gray-600">{Math.round(goal.progress_percentage)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(goal.progress_percentage)}`}
              style={{ width: `${goal.progress_percentage}%` }}
            ></div>
          </div>
        </div>

        {goal.target_date && (
          <div className="mb-4 text-sm text-gray-600">
            <span className="font-medium">Target: </span>
            {format(new Date(goal.target_date), 'MMM dd, yyyy')}
          </div>
        )}

        {/* Recent Progress */}
        {goal.progress_entries && goal.progress_entries.length > 0 && (
          <div className="mb-4">
            <h4 className="text-sm font-medium text-gray-700 mb-2">Latest Update</h4>
            <div className="bg-gray-50 rounded p-3">
              {(() => {
                // Sort progress entries by created_at descending to ensure latest is first
                const sortedEntries = [...goal.progress_entries].sort((a, b) =>
                  new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
                )
                const latestEntry = sortedEntries[0]

                return (
                  <>
                    <p className="text-sm text-gray-600 line-clamp-2">
                      {latestEntry.text}
                    </p>
                    <div className="flex items-center mt-2 space-x-2">
                      {latestEntry.sentiment && (
                        <span className={`px-2 py-1 rounded text-xs ${latestEntry.sentiment === 'positive' ? 'bg-green-100 text-green-700' :
                          latestEntry.sentiment === 'negative' ? 'bg-red-100 text-red-700' :
                            'bg-gray-100 text-gray-700'
                          }`}>
                          {latestEntry.sentiment}
                        </span>
                      )}
                      <span className="text-xs text-gray-500">
                        {format(new Date(latestEntry.created_at), 'MMM dd')}
                      </span>
                    </div>
                  </>
                )
              })()}
            </div>
          </div>
        )}

        <button
          onClick={() => setShowUpdateModal(true)}
          className="w-full btn-primary"
          disabled={goal.status === 'completed'}
        >
          {goal.status === 'completed' ? 'Completed' : 'Add Progress Update'}
        </button>
      </div>

      {showUpdateModal && (
        <ProgressUpdateModal
          goal={goal}
          onClose={() => setShowUpdateModal(false)}
          onProgressUpdated={onProgressUpdated}
        />
      )}

      {showDeleteModal && (
        <DeleteConfirmModal
          goal={goal}
          onClose={() => setShowDeleteModal(false)}
          onConfirm={handleDelete}
        />
      )}
    </>
  )
}
