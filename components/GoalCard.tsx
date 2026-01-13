import { useState } from 'react'
import { Goal } from '../types'
import { ProgressUpdateModal } from './ProgressUpdateModal'
import { format } from 'date-fns'

interface GoalCardProps {
  goal: Goal
}

export function GoalCard({ goal }: GoalCardProps) {
  const [showUpdateModal, setShowUpdateModal] = useState(false)

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

  return (
    <>
      <div className="card hover:shadow-lg transition-shadow">
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
            {goal.title}
          </h3>
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(goal.status)}`}>
            {goal.status}
          </span>
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
              <p className="text-sm text-gray-600 line-clamp-2">
                {goal.progress_entries[0].text}
              </p>
              <div className="flex items-center mt-2 space-x-2">
                {goal.progress_entries[0].sentiment && (
                  <span className={`px-2 py-1 rounded text-xs ${goal.progress_entries[0].sentiment === 'positive' ? 'bg-green-100 text-green-700' :
                    goal.progress_entries[0].sentiment === 'negative' ? 'bg-red-100 text-red-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                    {goal.progress_entries[0].sentiment}
                  </span>
                )}
                <span className="text-xs text-gray-500">
                  {format(new Date(goal.progress_entries[0].created_at), 'MMM dd')}
                </span>
              </div>
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
        />
      )}
    </>
  )
}
