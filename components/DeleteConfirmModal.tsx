import { useState } from 'react'
import { Goal } from '../types'

interface DeleteConfirmModalProps {
  goal: Goal
  onClose: () => void
  onConfirm: () => void
}

export function DeleteConfirmModal({ goal, onClose, onConfirm }: DeleteConfirmModalProps) {
  const [loading, setLoading] = useState(false)
  const [confirmText, setConfirmText] = useState('')

  const handleConfirm = async () => {
    setLoading(true)
    try {
      await onConfirm()
    } finally {
      setLoading(false)
    }
  }

  const isConfirmValid = confirmText.toLowerCase() === 'delete'

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50 modal-overlay">
      <div className="bg-white rounded-lg max-w-md w-full modal-content">
        <div className="p-6">
          <div className="flex items-center mb-4">
            <div className="flex-shrink-0">
              <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Delete Goal</h3>
              <p className="text-sm text-gray-500">This action cannot be undone</p>
            </div>
          </div>

          <div className="mb-4">
            <p className="text-sm text-gray-700 mb-2">
              You are about to delete the goal:
            </p>
            <div className="bg-gray-50 rounded-lg p-3 border">
              <h4 className="font-medium text-gray-900">{goal.title}</h4>
              {goal.description && (
                <p className="text-sm text-gray-600 mt-1">{goal.description}</p>
              )}
              <div className="flex items-center mt-2 space-x-4 text-xs text-gray-500">
                {goal.category && <span>Category: {goal.category}</span>}
                <span>Progress: {Math.round(goal.progress_percentage)}%</span>
                {goal.progress_entries && goal.progress_entries.length > 0 && (
                  <span>{goal.progress_entries.length} progress entries</span>
                )}
              </div>
            </div>
          </div>

          <div className="mb-4">
            <p className="text-sm text-gray-700 mb-2">
              This will permanently delete:
            </p>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• The goal and all its details</li>
              <li>• All progress entries and updates</li>
              <li>• All historical data and analytics</li>
            </ul>
          </div>

          <div className="mb-6">
            <label htmlFor="confirmText" className="block text-sm font-medium text-gray-700 mb-2">
              Type <span className="font-mono bg-gray-100 px-1 rounded">delete</span> to confirm:
            </label>
            <input
              type="text"
              id="confirmText"
              value={confirmText}
              onChange={(e) => setConfirmText(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
              placeholder="Type 'delete' to confirm"
              autoComplete="off"
            />
          </div>

          <div className="flex space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md transition-colors"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={handleConfirm}
              disabled={loading || !isConfirmValid}
              className="flex-1 bg-red-600 hover:bg-red-700 disabled:bg-red-300 disabled:cursor-not-allowed text-white font-medium py-2 px-4 rounded-md transition-colors"
            >
              {loading ? 'Deleting...' : 'Delete Goal'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}