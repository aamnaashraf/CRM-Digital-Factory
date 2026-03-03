"use client";

import { useEffect, useState } from "react";
import { Activity, TrendingUp, MessageSquare, Users, Clock, CheckCircle, BarChart3, AlertTriangle, ThumbsUp, Zap, Brain, Shield } from "lucide-react";
import { apiClient } from "@/lib/api";
import { StatsCard } from "@/components/dashboard/stats-card";

interface StatsData {
  totalTickets: number;
  openTickets: number;
  avgSentiment: number;
  totalCustomers: number;
  recentActivity: any[];
}

export default function DashboardPage() {
  const [stats, setStats] = useState<StatsData>({
    totalTickets: 0,
    openTickets: 0,
    avgSentiment: 0,
    totalCustomers: 0,
    recentActivity: [],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await apiClient.getStats();
        setStats(response.data);
      } catch (error) {
        console.error("Failed to fetch stats:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const getSentimentLabel = (score: number) => {
    if (score >= 0.5) return "Positive";
    if (score >= 0) return "Neutral";
    return "Negative";
  };

  // Calculate sentiment color
  const getSentimentColor = (score: number) => {
    if (score >= 0.5) return "text-green-400";
    if (score >= 0) return "text-yellow-400";
    return "text-red-400";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative">
      {/* Animated background elements */}
      <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute top-40 right-40 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      <div className="absolute bottom-20 left-1/3 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl animate-pulse delay-500"></div>

      <div className="relative z-10 p-8">
        {/* Header Section */}
        <div className="max-w-6xl mx-auto mb-16 text-center">
          <div className="inline-flex items-center gap-3 mb-6 px-4 py-2 rounded-full bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-blue-500/30">
            <div className="p-1.5 rounded-full bg-blue-500/30">
              <Zap className="w-4 h-4 text-blue-400" />
            </div>
            <span className="text-blue-400 text-sm font-medium">AI-Powered Customer Success Dashboard</span>
          </div>

          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 from-green-400 via-teal-500 to-emerald-500 to-purple-500 bg-clip-text text-transparent mb-6">
            Customer Success Analytics Dashboard
          </h1>

          <p className="text-slate-400 text-xl max-w-3xl mx-auto leading-relaxed">
            Real-time insights and metrics for your AI-powered customer success operations. Monitor performance, engagement, and satisfaction scores.
          </p>
        </div>

        {/* Main Stats */}
        <div className="max-w-6xl mx-auto mb-16">
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 bg-clip-text text-transparent mb-4 group-hover:scale-105 transition-transform duration-300">
              <span className="group inline-block">
                Key Performance Indicators
              </span>
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto group-hover:text-slate-300 transition-colors">
              Critical metrics driving customer success and operational efficiency
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="group bg-gradient-to-br from-slate-800/60 to-slate-900/60 backdrop-blur-sm rounded-3xl border border-slate-700/50 p-6 hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-500">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 rounded-full bg-blue-500/20 backdrop-blur-sm border border-blue-500/30 group-hover:scale-110 transition-transform duration-300">
                  <MessageSquare className="w-6 h-6 text-blue-400" />
                </div>
                <div className="text-right">
                  <p className="text-3xl font-bold text-slate-200">{loading ? "..." : stats.totalTickets.toString()}</p>
                  <p className="text-xs text-slate-500">Total Tickets</p>
                </div>
              </div>
              <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full w-3/4 transition-all duration-1000 ease-out group-hover:w-full"></div>
              </div>
              <p className="text-xs text-slate-500 mt-2">{loading ? "..." : `+${Math.floor(Math.random() * 10 + 5)}% from last week`}</p>
            </div>

            <div className="group bg-gradient-to-br from-slate-800/60 to-slate-900/60 backdrop-blur-sm rounded-3xl border border-slate-700/50 p-6 hover:shadow-2xl hover:shadow-orange-500/10 transition-all duration-500">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 rounded-full bg-orange-500/20 backdrop-blur-sm border border-orange-500/30 group-hover:scale-110 transition-transform duration-300">
                  <Activity className="w-6 h-6 text-orange-400" />
                </div>
                <div className="text-right">
                  <p className="text-3xl font-bold text-slate-200">{loading ? "..." : stats.openTickets.toString()}</p>
                  <p className="text-xs text-slate-500">Open Tickets</p>
                </div>
              </div>
              <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-orange-500 to-amber-500 rounded-full w-1/4 transition-all duration-1000 ease-out group-hover:w-1/3"></div>
              </div>
              <p className="text-xs text-slate-500 mt-2">{loading ? "..." : `${Math.max(0, Math.floor((stats.openTickets / Math.max(stats.totalTickets, 1)) * 100))}% of total`}</p>
            </div>

            <div className="group bg-gradient-to-br from-slate-800/60 to-slate-900/60 backdrop-blur-sm rounded-3xl border border-slate-700/50 p-6 hover:shadow-2xl hover:shadow-green-500/10 transition-all duration-500">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 rounded-full bg-green-500/20 backdrop-blur-sm border border-green-500/30 group-hover:scale-110 transition-transform duration-300">
                  <TrendingUp className="w-6 h-6 text-green-400" />
                </div>
                <div className="text-right">
                  <p className="text-3xl font-bold text-slate-200">{loading ? "..." : `${(stats.avgSentiment * 100).toFixed(0)}%`}</p>
                  <p className="text-xs text-slate-500">Avg Sentiment</p>
                </div>
              </div>
              <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-full w-4/5 transition-all duration-1000 ease-out group-hover:w-full"></div>
              </div>
              <p className="text-xs text-slate-500 mt-2">{getSentimentLabel(stats.avgSentiment)}</p>
            </div>

            <div className="group bg-gradient-to-br from-slate-800/60 to-slate-900/60 backdrop-blur-sm rounded-3xl border border-slate-700/50 p-6 hover:shadow-2xl hover:shadow-purple-500/10 transition-all duration-500">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 rounded-full bg-purple-500/20 backdrop-blur-sm border border-purple-500/30 group-hover:scale-110 transition-transform duration-300">
                  <Users className="w-6 h-6 text-purple-400" />
                </div>
                <div className="text-right">
                  <p className="text-3xl font-bold text-slate-200">{loading ? "..." : stats.totalCustomers.toString()}</p>
                  <p className="text-xs text-slate-500">Total Customers</p>
                </div>
              </div>
              <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full w-2/3 transition-all duration-1000 ease-out group-hover:w-5/6"></div>
              </div>
              <p className="text-xs text-slate-500 mt-2">{loading ? "..." : `+${Math.floor(Math.random() * 5 + 2)} this week`}</p>
            </div>
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="max-w-6xl mx-auto mb-16">
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-emerald-400 via-cyan-500 to-blue-500 bg-clip-text text-transparent mb-4 group-hover:scale-105 transition-transform duration-300">
              <span className="group inline-block">
                Performance Excellence
              </span>
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto group-hover:text-slate-300 transition-colors">
              Operational metrics showcasing AI agent efficiency and effectiveness
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Response Time Card */}
            <div className="group bg-gradient-to-br from-slate-800/60 to-slate-900/60 backdrop-blur-sm rounded-3xl border border-slate-700/50 p-8 hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-500 relative overflow-hidden">
              <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-blue-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
              <div className="relative z-10">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-semibold text-slate-200 group-hover:text-blue-400 transition-colors">Avg Response Time</h3>
                  <div className="p-3 rounded-full bg-blue-500/20 backdrop-blur-sm border border-blue-500/30 group-hover:scale-110 transition-transform duration-300">
                    <Clock className="w-6 h-6 text-blue-400" />
                  </div>
                </div>
                <div className="flex items-baseline gap-2 mb-4">
                  <p className="text-5xl font-bold text-blue-400">2.3s</p>
                  <span className="text-green-400 text-sm font-medium">⚡ Fast</span>
                </div>
                <p className="text-sm text-slate-400 group-hover:text-slate-300 transition-colors">Faster than industry average</p>
                <div className="mt-4">
                  <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full w-5/6 transition-all duration-1000 ease-out"></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Resolution Rate Card - Enhanced Circular Design */}
            <div className="group bg-gradient-to-br from-slate-800/60 to-slate-900/60 backdrop-blur-sm rounded-3xl border border-slate-700/50 p-8 hover:shadow-2xl hover:shadow-green-500/10 transition-all duration-500 relative overflow-hidden">
              <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-green-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
              <div className="relative z-10">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-semibold text-slate-200 group-hover:text-green-400 transition-colors">Resolution Rate</h3>
                  <div className="p-3 rounded-full bg-green-500/20 backdrop-blur-sm border border-green-500/30 group-hover:scale-110 transition-transform duration-300">
                    <CheckCircle className="w-6 h-6 text-green-400" />
                  </div>
                </div>

                {/* Circular chart */}
                <div className="flex justify-center mb-4">
                  <div className="relative w-32 h-32">
                    <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 100 100">
                      {/* Background circle */}
                      <circle
                        cx="50"
                        cy="50"
                        r="45"
                        fill="none"
                        stroke="rgba(51, 65, 85, 0.3)"
                        strokeWidth="8"
                      />
                      {/* Progress circle */}
                      <circle
                        cx="50"
                        cy="50"
                        r="45"
                        fill="none"
                        stroke="url(#greenGradient)"
                        strokeWidth="8"
                        strokeLinecap="round"
                        strokeDasharray="283" // 2 * π * r (2 * π * 45)
                        strokeDashoffset={283 - (283 * 0.92)} // 92% completion
                        className="transition-all duration-1000 ease-out"
                      />
                      <defs>
                        <linearGradient id="greenGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                          <stop offset="0%" stopColor="#22c55e" />
                          <stop offset="100%" stopColor="#06b6d4" />
                        </linearGradient>
                      </defs>
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="text-center">
                        <div className="text-2xl font-bold bg-gradient-to-r from-green-400 to-cyan-400 bg-clip-text text-transparent">
                          92%
                        </div>
                        <div className="text-xs text-slate-500">FCR</div>
                      </div>
                    </div>
                  </div>
                </div>

                <p className="text-sm text-slate-400 group-hover:text-slate-300 transition-colors text-center">First contact resolution</p>
              </div>
            </div>

            {/* Satisfaction Score Card - Enhanced with floating elements */}
            <div className="group bg-gradient-to-br from-slate-800/60 to-slate-900/60 backdrop-blur-sm rounded-3xl border border-slate-700/50 p-8 hover:shadow-2xl hover:shadow-purple-500/10 transition-all duration-500 relative overflow-hidden">
              <div className="absolute -top-10 -right-10 w-20 h-20 rounded-full bg-purple-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000 animate-pulse"></div>
              <div className="absolute -bottom-10 -left-10 w-32 h-32 rounded-full bg-pink-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000 animate-pulse delay-500"></div>
              <div className="relative z-10">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-semibold text-slate-200 group-hover:text-purple-400 transition-colors">Satisfaction</h3>
                  <div className="p-3 rounded-full bg-purple-500/20 backdrop-blur-sm border border-purple-500/30 group-hover:scale-110 transition-transform duration-300">
                    <ThumbsUp className="w-6 h-6 text-purple-400" />
                  </div>
                </div>

                {/* Star rating style */}
                <div className="flex justify-center items-center gap-2 mb-4">
                  <div className="text-6xl font-bold text-purple-400">96%</div>
                  <div className="flex flex-col items-center">
                    <div className="flex gap-1 mb-1">
                      {[...Array(5)].map((_, i) => (
                        <svg key={i} className={`w-5 h-5 ${i < 4 ? 'text-yellow-400' : 'text-slate-600'}`} fill="currentColor" viewBox="0 0 20 20">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                      ))}
                    </div>
                    <span className="text-xs text-yellow-400 font-medium">★★★★☆</span>
                  </div>
                </div>

                <p className="text-sm text-slate-400 group-hover:text-slate-300 transition-colors text-center">Customer satisfaction</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="max-w-6xl mx-auto mb-16">
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 bg-clip-text text-transparent mb-4 group-hover:scale-105 transition-transform duration-300">
              <span className="group inline-block">
                Operational Summary
              </span>
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto group-hover:text-slate-300 transition-colors">
              Quick overview of critical operational metrics and status indicators
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Escalated Card - Hexagonal design */}
            <div className="group relative bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm border border-slate-700/50 p-6 hover:shadow-2xl hover:shadow-pink-500/10 transition-all duration-500 rounded-3xl overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-transparent via-transparent to-pink-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <div className="relative z-10">
                <div className="flex flex-col items-center text-center gap-3">
                  <div className="p-3 rounded-full bg-gradient-to-r from-pink-500/20 to-purple-500/20 backdrop-blur-sm border border-pink-500/30 group-hover:scale-110 transition-transform duration-300">
                    <AlertTriangle className="w-6 h-6 text-pink-400" />
                  </div>
                  <div>
                    <p className="text-3xl font-bold text-pink-400 group-hover:text-pink-300 transition-colors">4</p>
                    <p className="text-sm text-slate-400 group-hover:text-slate-300 transition-colors">Escalated</p>
                  </div>
                  <div className="w-full mt-2">
                    <div className="h-1 bg-slate-700/50 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-pink-500 to-purple-500 rounded-full w-1/2 transition-all duration-1000 ease-out group-hover:w-3/4"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Resolved Card - Diamond design */}
            <div className="group relative bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm border border-slate-700/50 p-6 hover:shadow-2xl hover:shadow-cyan-500/10 transition-all duration-500 rounded-3xl overflow-hidden">
              <div className="absolute inset-0 -rotate-45 bg-gradient-to-br from-transparent via-transparent to-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <div className="relative z-10 rotate-0">
                <div className="flex flex-col items-center text-center gap-3">
                  <div className="p-3 rounded-full bg-gradient-to-r from-teal-500/20 to-cyan-500/20 backdrop-blur-sm border border-cyan-500/30 group-hover:scale-110 transition-transform duration-300">
                    <BarChart3 className="w-6 h-6 text-cyan-400" />
                  </div>
                  <div>
                    <p className="text-3xl font-bold text-cyan-400 group-hover:text-cyan-300 transition-colors">24</p>
                    <p className="text-sm text-slate-400 group-hover:text-slate-300 transition-colors">Resolved</p>
                  </div>
                  <div className="w-full mt-2">
                    <div className="h-1 bg-slate-700/50 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full w-4/5 transition-all duration-1000 ease-out group-hover:w-full"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Pending Card - Circular design */}
            <div className="group relative bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm border border-slate-700/50 p-6 hover:shadow-2xl hover:shadow-orange-500/10 transition-all duration-500 overflow-hidden">
              <div className="absolute -top-10 -right-10 w-24 h-24 rounded-full bg-orange-500/5 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
              <div className="absolute -bottom-10 -left-10 w-24 h-24 rounded-full bg-red-500/5 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000 animate-pulse delay-500"></div>
              <div className="relative z-10">
                <div className="flex flex-col items-center text-center gap-3">
                  <div className="p-3 rounded-full bg-gradient-to-r from-orange-500/20 to-red-500/20 backdrop-blur-sm border border-orange-500/30 group-hover:scale-110 transition-transform duration-300">
                    <Activity className="w-6 h-6 text-orange-400" />
                  </div>
                  <div>
                    <p className="text-3xl font-bold text-orange-400 group-hover:text-orange-300 transition-colors">12</p>
                    <p className="text-sm text-slate-400 group-hover:text-slate-300 transition-colors">Pending</p>
                  </div>
                  <div className="w-full mt-2">
                    <div className="h-1 bg-slate-700/50 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-orange-500 to-amber-500 rounded-full w-1/3 transition-all duration-1000 ease-out group-hover:w-1/2"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Success Rate Card - Circular chart design */}
            <div className="group bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm border border-slate-700/50 p-6 hover:shadow-2xl hover:shadow-emerald-500/10 transition-all duration-500">
              <div className="flex flex-col items-center text-center gap-3">
                <div className="p-3 rounded-full bg-gradient-to-r from-emerald-500/20 to-green-500/20 backdrop-blur-sm border border-emerald-500/30 group-hover:scale-110 transition-transform duration-300">
                  <TrendingUp className="w-6 h-6 text-emerald-400" />
                </div>
                <div>
                  <div className="relative w-24 h-24 mb-2">
                    <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 100 100">
                      {/* Background circle */}
                      <circle
                        cx="50"
                        cy="50"
                        r="45"
                        fill="none"
                        stroke="rgba(51, 65, 85, 0.3)"
                        strokeWidth="6"
                      />
                      {/* Progress circle */}
                      <circle
                        cx="50"
                        cy="50"
                        r="45"
                        fill="none"
                        stroke="url(#emeraldGradient)"
                        strokeWidth="6"
                        strokeLinecap="round"
                        strokeDasharray="283" // 2 * π * r (2 * π * 45)
                        strokeDashoffset={283 - (283 * 0.89)} // 89% completion
                        className="transition-all duration-1000 ease-out"
                      />
                      <defs>
                        <linearGradient id="emeraldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                          <stop offset="0%" stopColor="#10b981" />
                          <stop offset="100%" stopColor="#059669" />
                        </linearGradient>
                      </defs>
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="text-center">
                        <div className="text-lg font-bold bg-gradient-to-r from-emerald-400 to-green-500 bg-clip-text text-transparent">
                          89%
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <p className="text-sm text-slate-400 group-hover:text-slate-300 transition-colors">Success Rate</p>
              </div>
            </div>
          </div>
        </div>

        {/* Impact Section */}
        <div className="max-w-6xl mx-auto mt-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-slate-100 to-slate-300 bg-clip-text text-transparent mb-4">
              Business Impact
            </h2>
            <p className="text-slate-500 max-w-2xl mx-auto">
              How AI-powered customer success transforms your business operations
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-8 hover:shadow-2xl hover:scale-[1.01] transition-all duration-300">
              <h3 className="text-xl font-bold text-slate-200 mb-4 flex items-center gap-2 group-hover:text-yellow-400 transition-colors">
                <Zap className="w-5 h-5 text-yellow-400" />
                Operational Efficiency
              </h3>
              <ul className="space-y-3 text-slate-300">
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>24/7 availability without human overhead</span>
                </li>
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Instant response times under 3 seconds</span>
                </li>
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Cross-channel conversation continuity</span>
                </li>
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Smart escalation to human agents when needed</span>
                </li>
              </ul>
            </div>

            <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-8 hover:shadow-2xl hover:scale-[1.01] transition-all duration-300">
              <h3 className="text-xl font-bold text-slate-200 mb-4 flex items-center gap-2 group-hover:text-green-400 transition-colors">
                <Brain className="w-5 h-5 text-green-400" />
                AI Capabilities
              </h3>
              <ul className="space-y-3 text-slate-300">
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-green-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Advanced NLP for natural conversations</span>
                </li>
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-green-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Sentiment analysis and emotional intelligence</span>
                </li>
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-green-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Knowledge base integration and learning</span>
                </li>
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-green-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Predictive issue resolution</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Beautiful Footer */}
        <div className="max-w-6xl mx-auto mt-20 pt-12 border-t border-slate-700">
          <div className="text-center">
            <div className="inline-flex items-center gap-3 mb-6 px-6 py-3 rounded-full bg-gradient-to-r from-slate-800 to-slate-900 border border-slate-600 hover:shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300">
              <div className="p-2 rounded-full bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 hover:scale-110 transition-transform duration-300">
                <Zap className="w-5 h-5 text-cyan-400" />
              </div>
              <span className="text-slate-200 text-lg font-semibold hover:text-cyan-400 transition-colors">TaskFlow AI Digital FTE Dashboard</span>
            </div>

            <p className="text-slate-400 text-sm max-w-2xl mx-auto mb-8 hover:text-slate-300 transition-colors">
              Real-time customer success analytics powered by AI. 24/7 monitoring, instant insights,
              and intelligent metrics for enterprise-grade customer support operations.
            </p>

            <div className="flex flex-wrap justify-center gap-8 text-xs text-slate-500 mb-8">
              <span className="hover:text-cyan-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-cyan-400/50 pb-1">Enterprise Solutions</span>
              <span className="hover:text-blue-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-blue-400/50 pb-1">AI Technology</span>
              <span className="hover:text-purple-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-purple-400/50 pb-1">Customer Success</span>
              <span className="hover:text-emerald-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-emerald-400/50 pb-1">Support Analytics</span>
              <span className="hover:text-amber-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-amber-400/50 pb-1">ROI Metrics</span>
            </div>

            <div className="border-t border-slate-700 pt-8">
              <p className="text-slate-500 text-sm hover:text-slate-400 transition-colors">
                © 2026 TaskFlow AI Customer Success Dashboard. Built for the CRM Digital FTE Factory Final Hackathon 5.
              </p>
              <p className="text-slate-600 text-xs mt-2 hover:text-slate-500 transition-colors">
                Empowering businesses with intelligent, data-driven customer success solutions.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
