import { useState, useEffect } from 'react';
import { Loader, TrendingUp, Clock, Target, Award } from 'lucide-react';
import toast from 'react-hot-toast';
import { progressAPI } from '../services/api';

export default function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      // For demo, use a dummy user ID. In production, get from auth context
      const response = await progressAPI.getDashboard('user-id');
      setDashboard(response.data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
      // Use mock data for demo
      setDashboard({
        total_documents: 0,
        total_games_played: 0,
        total_quizzes_completed: 0,
        average_score: 0,
        total_study_time_minutes: 0,
        recent_activities: [],
        subject_breakdown: {},
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    );
  }

  const stats = [
    {
      icon: Target,
      label: 'Documents',
      value: dashboard.total_documents,
      color: 'bg-blue-500',
    },
    {
      icon: Award,
      label: 'Games Played',
      value: dashboard.total_games_played,
      color: 'bg-green-500',
    },
    {
      icon: TrendingUp,
      label: 'Quizzes Completed',
      value: dashboard.total_quizzes_completed,
      color: 'bg-purple-500',
    },
    {
      icon: Clock,
      label: 'Study Time (min)',
      value: dashboard.total_study_time_minutes,
      color: 'bg-orange-500',
    },
  ];

  return (
    <div className="animate-fade-in">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">My Dashboard</h1>
        <p className="text-lg text-gray-600">Track your learning progress</p>
      </div>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="bg-white rounded-xl shadow-sm p-6">
              <div className={`${stat.color} w-12 h-12 rounded-xl flex items-center justify-center mb-4`}>
                <Icon className="w-6 h-6 text-white" />
              </div>
              <p className="text-3xl font-bold text-gray-900 mb-1">{stat.value}</p>
              <p className="text-sm text-gray-600">{stat.label}</p>
            </div>
          );
        })}
      </div>

      {/* Average Score */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white mb-8">
        <h2 className="text-2xl font-bold mb-4">Average Score</h2>
        <div className="flex items-end">
          <div className="text-6xl font-bold">{dashboard.average_score.toFixed(0)}%</div>
          <TrendingUp className="w-12 h-12 ml-4 mb-2" />
        </div>
        <p className="mt-2 text-blue-100">
          {dashboard.average_score >= 80 ? 'Excellent performance!' : 'Keep up the good work!'}
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Recent Activities */}
        <div className="bg-white rounded-2xl shadow-sm p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Activities</h2>
          {dashboard.recent_activities.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No activities yet</p>
          ) : (
            <div className="space-y-3">
              {dashboard.recent_activities.map((activity, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">{activity.content_title}</p>
                    <p className="text-sm text-gray-500">{activity.content_type}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-primary-600">{activity.score?.toFixed(0)}%</p>
                    <p className="text-xs text-gray-500">
                      {new Date(activity.completed_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Subject Breakdown */}
        <div className="bg-white rounded-2xl shadow-sm p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Subject Breakdown</h2>
          {Object.keys(dashboard.subject_breakdown).length === 0 ? (
            <p className="text-gray-500 text-center py-8">No data yet</p>
          ) : (
            <div className="space-y-4">
              {Object.entries(dashboard.subject_breakdown).map(([subject, count]) => (
                <div key={subject}>
                  <div className="flex justify-between mb-2">
                    <span className="font-medium text-gray-900 capitalize">{subject}</span>
                    <span className="text-gray-600">{count}</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary-600"
                      style={{
                        width: `${(count / Math.max(...Object.values(dashboard.subject_breakdown))) * 100}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
