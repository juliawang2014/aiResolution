import { useState, useEffect } from 'react'
import Head from 'next/head'
import { GoalCard } from '../components/GoalCard'
import { StatsOverview } from '../components/StatsOverview'
import { AddGoalForm } from '../components/AddGoalForm'
import { ProgressChart } from '../components/ProgressChart'
import { useWebSocket } from '../hooks/useWebSocket'
import { Goal, DashboardStats } from '../types'

export default function Dashboard() {
  const [goals, setGoals] = useState<Goal[]>([])
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [showAddForm, setShowAddForm] = useState(false)

  // WebSocket connection for real-time updates
  const { lastMessage, connectionStatus } = useWebSocket('ws://localhost:8000/ws')

  // Load initial data
  useEffect(() => {
    fetchDashboardData()
  }, [])

  // Handle WebSocket messages
  useEffect(() => {
    if (lastMessage) {
      const data = JSON.parse(lastMessage.data)

      if (data.type === 'goal_created') {
        setGoals(prev => [...prev, data.data])
      } else if (data.type === 'progress_updated') {
        setGoals(prev => prev.map(goal =>
          goal.id === data.data.goal_id ? data.data.updated_goal : goal
        ))
      }
    }
  }, [lastMessage])

  const fetchDashboardData = async () => {
    try {
      const response = await fetch('http://localhost:8000/dashboard')
      const data = await response.json()
      setGoals(data.goals)
      setStats(data.statistics)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleGoalAdded = (newGoal: Goal) => {
    setGoals(prev => [...prev, newGoal])
    setShowAddForm(false)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your goals...</p>
        </div>
      </div>
    )
  }

  return (
    <>
      <Head>
        <title>Goal Tracker - Public Dashboard</title>
        <meta name="description" content="Real-time goal tracking dashboard" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Goal Tracker</h1>
                <p className="text-gray-600">Real-time progress dashboard</p>
              </div>
              <div className="flex items-center space-x-4">
                <div className={`flex items-center space-x-2 ${connectionStatus === 'Connected' ? 'text-green-600' : 'text-red-600'
                  }`}>
                  <div className={`w-2 h-2 rounded-full ${connectionStatus === 'Connected' ? 'bg-green-500' : 'bg-red-500'
                    }`}></div>
                  <span className="text-sm">{connectionStatus}</span>
                </div>
                <button
                  onClick={() => setShowAddForm(true)}
                  className="btn-primary"
                >
                  Add Goal
                </button>
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Stats Overview */}
          {stats && <StatsOverview stats={stats} />}

          {/* Progress Chart */}
          <div className="mt-8">
            <ProgressChart goals={goals} />
          </div>

          {/* Goals Grid */}
          <div className="mt-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Active Goals</h2>
            {goals.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-gray-500 text-lg">No goals yet. Create your first goal to get started!</p>
                <button
                  onClick={() => setShowAddForm(true)}
                  className="btn-primary mt-4"
                >
                  Create Your First Goal
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {goals.map((goal) => (
                  <GoalCard key={goal.id} goal={goal} />
                ))}
              </div>
            )}
          </div>
        </main>

        {/* Add Goal Modal */}
        {showAddForm && (
          <AddGoalForm
            onClose={() => setShowAddForm(false)}
            onGoalAdded={handleGoalAdded}
          />
        )}
      </div>
    </>
  )
}