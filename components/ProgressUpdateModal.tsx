import { useState } from 'react'
import { Goal } from '../types'

interface ProgressUpdateModalProps {
  goal: Goal
  onClose: () => void
  onProgressUpdated?: (goalId: number) => void
}

export function ProgressUpdateModal({ goal, onClose, onProgressUpdated }: ProgressUpdateModalProps) {
  const [updateText, setUpdateText] = useState('')
  const [loading, setLoading] = useState(false)
  const [feedback, setFeedback] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!updateText.trim()) return

    setLoading(true)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/goals/${goal.id}/update`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: updateText
        }),
      })

      if (response.ok) {
        const result = await response.json()
        setFeedback(result.feedback)
        setUpdateText('')

        // Notify parent that progress was updated
        if (onProgressUpdated) {
          onProgressUpdated(goal.id)
        }

        // Close modal after showing feedback for a moment
        setTimeout(() => {
          onClose()
        }, 3000)
      } else {
        console.error('Failed to update progress')
      }
    } catch (error) {
      console.error('Error updating progress:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-md w-full">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-900">Update Progress</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="mb-4">
            <h3 className="font-medium text-gray-900 mb-2">{goal.title}</h3>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-primary-600 h-2 rounded-full"
                style={{ width: `${goal.progress_percentage}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-600 mt-1">Current progress: {Math.round(goal.progress_percentage)}%</p>
          </div>

          {feedback ? (
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-medium text-blue-900 mb-2">AI Feedback</h4>
              <p className="text-blue-800">{feedback}</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="updateText" className="block text-sm font-medium text-gray-700 mb-2">
                  How's your progress? (Use natural language)
                </label>
                <textarea
                  id="updateText"
                  value={updateText}
                  onChange={(e) => setUpdateText(e.target.value)}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="e.g., 'I completed 3 chapters today and feel great about my progress!' or 'Struggling with motivation this week, only did 20% of what I planned'"
                  required
                />
              </div>

              <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded">
                <p className="font-medium mb-1">Tips for better AI analysis:</p>
                <ul className="text-xs space-y-1">
                  <li>• Mention specific achievements or milestones</li>
                  <li>• Include percentages or fractions (e.g., "50%" or "3/10 done")</li>
                  <li>• Describe your feelings and challenges</li>
                  <li>• Be specific about what you accomplished</li>
                </ul>
              </div>

              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={onClose}
                  className="flex-1 btn-secondary"
                  disabled={loading}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 btn-primary"
                  disabled={loading || !updateText.trim()}
                >
                  {loading ? 'Processing...' : 'Update Progress'}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  )
}