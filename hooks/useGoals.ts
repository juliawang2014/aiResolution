import { useState, useCallback } from 'react'
import { Goal } from '../types'

export function useGoals() {
  const [goals, setGoals] = useState<Goal[]>([])

  // Add goal with duplicate prevention
  const addGoal = useCallback((newGoal: Goal) => {
    setGoals(prev => {
      // Check if goal already exists
      const existingIndex = prev.findIndex(goal => goal.id === newGoal.id)

      if (existingIndex >= 0) {
        console.log(`Goal with ID ${newGoal.id} already exists, updating instead of adding`)
        // Update existing goal
        const updated = [...prev]
        updated[existingIndex] = newGoal
        return updated
      }

      // Add new goal
      console.log(`Adding new goal with ID ${newGoal.id}`)
      return [...prev, newGoal]
    })
  }, [])

  // Update goal
  const updateGoal = useCallback((updatedGoal: Goal) => {
    setGoals(prev => prev.map(goal =>
      goal.id === updatedGoal.id ? updatedGoal : goal
    ))
  }, [])

  // Remove goal
  const removeGoal = useCallback((goalId: number) => {
    setGoals(prev => prev.filter(goal => goal.id !== goalId))
  }, [])

  // Set all goals (for initial load)
  const setAllGoals = useCallback((newGoals: Goal[]) => {
    // Remove duplicates by ID
    const uniqueGoals = newGoals.reduce((acc: Goal[], goal) => {
      const existingIndex = acc.findIndex(g => g.id === goal.id)
      if (existingIndex >= 0) {
        // Keep the newer one (or the one with more data)
        acc[existingIndex] = goal
      } else {
        acc.push(goal)
      }
      return acc
    }, [])

    setGoals(uniqueGoals)
  }, [])

  // Clear all goals
  const clearGoals = useCallback(() => {
    setGoals([])
  }, [])

  return {
    goals,
    addGoal,
    updateGoal,
    removeGoal,
    setAllGoals,
    clearGoals
  }
}