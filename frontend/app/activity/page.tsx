"use client";

import { useEffect, useState } from "react";
import { Clock, Activity as ActivityIcon, MessageSquare, Filter } from "lucide-react";
import { apiClient } from "@/lib/api";
import { RecentActivity } from "@/components/dashboard/recent-activity";

interface ActivityItem {
  id: string;
  customer: string;
  message: string;
  channel: string;
  time: string;
  sentiment: number;
  status: string;
}

export default function ActivityPage() {
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const fetchActivity = async () => {
      try {
        // Use the balanced activity endpoint to ensure all channels are represented
        const response = await apiClient.getBalancedActivity();
        setActivities(response.data.activities);
      } catch (error) {
        console.error("Failed to fetch activity:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchActivity();
  }, []);

  const filteredActivities = activities.filter(activity => {
    if (filter === 'all') return true;
    if (filter === 'open') return activity.status === 'open';
    if (filter === 'resolved') return activity.status === 'resolved';
    if (filter === 'escalated') return activity.status === 'escalated';
    if (filter === 'web') return activity.channel === 'web';
    if (filter === 'email') return activity.channel === 'email';
    if (filter === 'whatsapp') return activity.channel === 'whatsapp';
    return true;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative">
      {/* Animated background */}
      <div className="absolute top-20 left-10 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl animate-pulse delay-1000"></div>

      <div className="relative z-10 p-8">
        {/* Header */}
        <div className="mb-10 text-center">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent mb-4">
            Activity Feed
          </h1>
          <p className="text-slate-400 max-w-2xl mx-auto">
            Track all customer interactions and support requests in real-time
          </p>
        </div>

        {/* Filter Controls */}
        <div className="mb-8 flex flex-wrap items-center justify-center gap-4">
          {[
            { key: 'all', label: 'All Activity', icon: ActivityIcon },
            { key: 'open', label: 'Open', icon: MessageSquare },
            { key: 'resolved', label: 'Resolved', icon: MessageSquare, color: 'green' },
            { key: 'escalated', label: 'Escalated', icon: MessageSquare, color: 'orange' },
            { key: 'web', label: 'Web', icon: MessageSquare, color: 'blue' },
            { key: 'email', label: 'Email', icon: MessageSquare, color: 'amber' },
            { key: 'whatsapp', label: 'WhatsApp', icon: MessageSquare, color: 'green' },
          ].map(({ key, label, icon: Icon, color }) => (
            <button
              key={key}
              onClick={() => setFilter(key)}
              className={`flex items-center gap-2 px-4 py-2 rounded-full border transition-all duration-200 ${
                filter === key
                  ? color === 'green' ? 'bg-green-500/20 border-green-500/50 text-green-400' :
                    color === 'orange' ? 'bg-orange-500/20 border-orange-500/50 text-orange-400' :
                    color === 'blue' ? 'bg-blue-500/20 border-blue-500/50 text-blue-400' :
                    color === 'amber' ? 'bg-amber-500/20 border-amber-500/50 text-amber-400' :
                    'bg-gradient-to-r from-blue-500/20 to-purple-500/20 border-blue-500/50 text-blue-400'
                  : 'bg-slate-800/50 border-slate-600 text-slate-400 hover:border-slate-500'
              }`}
            >
              <Icon className="w-4 h-4" />
              {label}
            </button>
          ))}
        </div>

        {/* Stats Summary */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border border-slate-700">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-full bg-blue-500/20 border border-blue-500/30">
                <ActivityIcon className="w-5 h-5 text-blue-400" />
              </div>
              <div>
                <p className="text-2xl font-bold text-slate-200">{activities.length}</p>
                <p className="text-xs text-slate-500">Total</p>
              </div>
            </div>
          </div>
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border border-slate-700">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-full bg-orange-500/20 border border-orange-500/30">
                <MessageSquare className="w-5 h-5 text-orange-400" />
              </div>
              <div>
                <p className="text-2xl font-bold text-slate-200">
                  {activities.filter(a => a.status === 'open').length}
                </p>
                <p className="text-xs text-slate-500">Open</p>
              </div>
            </div>
          </div>
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border border-slate-700">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-full bg-green-500/20 border border-green-500/30">
                <MessageSquare className="w-5 h-5 text-green-400" />
              </div>
              <div>
                <p className="text-2xl font-bold text-slate-200">
                  {activities.filter(a => a.status === 'resolved').length}
                </p>
                <p className="text-xs text-slate-500">Resolved</p>
              </div>
            </div>
          </div>
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border border-slate-700">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-full bg-red-500/20 border border-red-500/30">
                <MessageSquare className="w-5 h-5 text-red-400" />
              </div>
              <div>
                <p className="text-2xl font-bold text-slate-200">
                  {activities.filter(a => a.status === 'escalated').length}
                </p>
                <p className="text-xs text-slate-500">Escalated</p>
              </div>
            </div>
          </div>
        </div>

        {/* Activity List */}
        <div className="max-w-6xl mx-auto">
          <RecentActivity activities={filteredActivities} loading={loading} />
        </div>

        {/* Beautiful Footer */}
        <div className="max-w-6xl mx-auto mt-20 pt-12 border-t border-slate-700">
          <div className="text-center">
            <div className="inline-flex items-center gap-3 mb-6 px-6 py-3 rounded-full bg-gradient-to-r from-slate-800 to-slate-900 border border-slate-600 hover:shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300">
              <div className="p-2 rounded-full bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 hover:scale-110 transition-transform duration-300">
                <ActivityIcon className="w-5 h-5 text-cyan-400" />
              </div>
              <span className="text-slate-200 text-lg font-semibold hover:text-cyan-400 transition-colors">Real-Time Activity Feed</span>
            </div>

            <p className="text-slate-400 text-sm max-w-2xl mx-auto mb-8 hover:text-slate-300 transition-colors">
              Live tracking of all customer interactions across channels. Transparent visibility into AI agent performance.
            </p>

            <div className="flex flex-wrap justify-center gap-8 text-xs text-slate-500 mb-8">
              <span className="hover:text-cyan-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-cyan-400/50 pb-1">Live Tracking</span>
              <span className="hover:text-blue-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-blue-400/50 pb-1">Channel Activity</span>
              <span className="hover:text-purple-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-purple-400/50 pb-1">Status Updates</span>
              <span className="hover:text-emerald-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-emerald-400/50 pb-1">Performance Logs</span>
              <span className="hover:text-amber-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-amber-400/50 pb-1">AI Transparency</span>
            </div>

            <div className="border-t border-slate-700 pt-8">
              <p className="text-slate-500 text-sm hover:text-slate-400 transition-colors">
                © 2026 TaskFlow AI Activity Monitoring. Built for the CRM Digital FTE Factory Final Hackathon 5.
              </p>
              <p className="text-slate-600 text-xs mt-2 hover:text-slate-500 transition-colors">
                Real-time visibility into customer engagement across all channels.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
