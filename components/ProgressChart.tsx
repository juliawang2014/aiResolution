import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import { Goal } from '../types'
import { format, subDays } from 'date-fns'

interface ProgressChartProps {
  goals: Goal[]
}

export function ProgressChart({ goals }: ProgressChartProps) {
  // Generate progress over time data (mock data for demo)
  const generateProgressData = () => {
    const days = 30
    const data = []

    for (let i = days; i >= 0; i--) {
      const date = subDays(new Date(), i)
      const avgProgress = goals.reduce((sum, goal) => sum + goal.progress_percentage, 0) / (goals.length || 1)

      // Add some variation to make it look realistic
      const variation = (Math.random() - 0.5) * 10
      const progress = Math.max(0, Math.min(100, avgProgress + variation - (i * 0.5)))

      data.push({
        date: format(date, 'MMM dd'),
        progress: Math.round(progress)
      })
    }

    return data
  }

  // Generate category distribution data
  const getCategoryData = () => {
    const categories: Record<string, number> = {}

    goals.forEach(goal => {
      const category = goal.category || 'Uncategorized'
      categories[category] = (categories[category] || 0) + 1
    })

    return Object.entries(categories).map(([name, value]) => ({
      name,
      value,
      progress: goals
        .filter(g => (g.category || 'Uncategorized') === name)
        .reduce((sum, g) => sum + g.progress_percentage, 0) /
        goals.filter(g => (g.category || 'Uncategorized') === name).length || 0
    }))
  }

  const progressData = generateProgressData()
  const categoryData = getCategoryData()

  if (goals.length === 0) {
    return (
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Progress Analytics</h3>
        <div className="text-center py-8 text-gray-500">
          <p>No data to display yet. Add some goals to see your progress analytics!</p>
        </div>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Progress Over Time */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Progress Over Time</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={progressData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis domain={[0, 100]} />
            <Tooltip
              formatter={(value) => [`${value}%`, 'Average Progress']}
              labelStyle={{ color: '#374151' }}
            />
            <Line
              type="monotone"
              dataKey="progress"
              stroke="#3B82F6"
              strokeWidth={2}
              dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Goals by Category */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Goals by Category</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={categoryData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip
              formatter={(value, name) => [
                name === 'value' ? `${value} goals` : `${Math.round(value as number)}% avg`,
                name === 'value' ? 'Count' : 'Avg Progress'
              ]}
              labelStyle={{ color: '#374151' }}
            />
            <Bar dataKey="value" fill="#3B82F6" />
            <Bar dataKey="progress" fill="#10B981" />
          </BarChart>
        </ResponsiveContainer>
        <div className="mt-4 flex justify-center space-x-6 text-sm">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-blue-500 rounded mr-2"></div>
            <span>Goal Count</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded mr-2"></div>
            <span>Avg Progress</span>
          </div>
        </div>
      </div>
    </div>
  )
}