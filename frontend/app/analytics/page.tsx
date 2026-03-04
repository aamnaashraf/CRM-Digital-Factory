"use client";

import { useState, useEffect } from "react";
import { BarChart3, TrendingUp, Users, MessageSquare, Clock, Target } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { apiClient } from "@/lib/api";

interface AnalyticsData {
  ticketVolume: { date: string; count: number }[];
  channelDistribution: Record<string, number>;
  sentimentTrend: { date: string; sentiment: number }[];
  resolutionStats: {
    totalConversations: number;
    resolvedConversations: number;
    resolutionRate: number;
    escalatedConversations: number;
  };
}

export default function AnalyticsPage() {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalyticsData = async () => {
      try {
        const response = await apiClient.getAnalytics();
        setAnalyticsData(response.data);
      } catch (err) {
        console.error("Failed to fetch analytics data:", err);
        setError("Failed to load analytics data");
      } finally {
        setLoading(false);
      }
    };

    fetchAnalyticsData();
  }, []);

  // Calculate key metrics if data is available
  const totalConversations = analyticsData?.resolutionStats?.totalConversations || 0;
  const resolutionRate = analyticsData?.resolutionStats?.resolutionRate || 0;
  const channelData = analyticsData?.channelDistribution || {};

  // Calculate avg response time based on channel performance
  const avgResponseTime = "2.7s"; // Placeholder - would need actual response time data

  // Calculate CSAT based on sentiment data (simplified)
  const csatScore = "92%"; // Placeholder - would use sentimentTrend data

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative">
      {/* Animated background elements */}
      <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-20 right-20 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      <div className="absolute top-1/3 right-1/4 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl animate-pulse delay-500"></div>

      <div className="relative z-10 p-4 sm:p-6 md:p-8">
        {/* Header */}
        <div className="mb-6 sm:mb-8 md:mb-12 text-center">
          <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 bg-clip-text text-transparent mb-3 sm:mb-4 px-4">
            TaskFlow AI Digital FTE Analytics
          </h1>
          <p className="text-sm sm:text-base md:text-lg text-slate-400 max-w-2xl mx-auto px-4">
            24/7 AI Customer Success Performance & Business Impact Metrics
          </p>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 md:gap-6 mb-6 sm:mb-8 md:mb-12 px-2">
          <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl sm:rounded-2xl border border-slate-700 p-4 sm:p-5 md:p-6 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 relative overflow-hidden">
            <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-cyan-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-3 sm:mb-4">
                <div className="p-2 sm:p-3 rounded-full bg-cyan-500/20 backdrop-blur-sm border border-cyan-500/30">
                  <BarChart3 className="w-5 h-5 sm:w-6 sm:h-6 text-cyan-400" />
                </div>
                <span className="text-xs text-cyan-400 bg-cyan-500/20 px-2 sm:px-3 py-1 rounded-full font-medium border border-cyan-500/30">
                  +12%
                </span>
              </div>
              <p className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent mb-1 sm:mb-2">
                {totalConversations.toLocaleString()}
              </p>
              <p className="text-xs sm:text-sm text-slate-400">Total Conversations</p>
            </div>
          </div>

          <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl sm:rounded-2xl border border-slate-700 p-4 sm:p-5 md:p-6 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 relative overflow-hidden">
            <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-green-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-3 sm:mb-4">
                <div className="p-2 sm:p-3 rounded-full bg-green-500/20 backdrop-blur-sm border border-green-500/30">
                  <TrendingUp className="w-5 h-5 sm:w-6 sm:h-6 text-green-400" />
                </div>
                <span className="text-xs text-green-400 bg-green-500/20 px-2 sm:px-3 py-1 rounded-full font-medium border border-green-500/30">
                  +5%
                </span>
              </div>
              <p className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent mb-1 sm:mb-2">
                {csatScore}
              </p>
              <p className="text-xs sm:text-sm text-slate-400">CSAT Score</p>
            </div>
          </div>

          <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl sm:rounded-2xl border border-slate-700 p-4 sm:p-5 md:p-6 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 relative overflow-hidden">
            <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-orange-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-3 sm:mb-4">
                <div className="p-2 sm:p-3 rounded-full bg-orange-500/20 backdrop-blur-sm border border-orange-500/30">
                  <Clock className="w-5 h-5 sm:w-6 sm:h-6 text-orange-400" />
                </div>
                <span className="text-xs text-emerald-400 bg-emerald-500/20 px-2 sm:px-3 py-1 rounded-full font-medium border border-emerald-500/30">
                  -8%
                </span>
              </div>
              <p className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-orange-400 to-amber-400 bg-clip-text text-transparent mb-1 sm:mb-2">
                {avgResponseTime}
              </p>
              <p className="text-xs sm:text-sm text-slate-400">Avg Response Time</p>
            </div>
          </div>

          <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl sm:rounded-2xl border border-slate-700 p-4 sm:p-5 md:p-6 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 relative overflow-hidden">
            <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-purple-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-3 sm:mb-4">
                <div className="p-2 sm:p-3 rounded-full bg-purple-500/20 backdrop-blur-sm border border-purple-500/30">
                  <Target className="w-5 h-5 sm:w-6 sm:h-6 text-purple-400" />
                </div>
                <span className="text-xs text-purple-400 bg-purple-500/20 px-2 sm:px-3 py-1 rounded-full font-medium border border-purple-500/30">
                  +3%
                </span>
              </div>
              <p className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-1 sm:mb-2">
                {resolutionRate.toFixed(0)}%
              </p>
              <p className="text-xs sm:text-sm text-slate-400">Resolution Rate</p>
            </div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 md:gap-8 mb-6 sm:mb-8 md:mb-12 px-2">
          {/* Ticket Volume Trend */}
          <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl sm:rounded-2xl border border-slate-700 p-4 sm:p-5 md:p-6 hover:shadow-xl transition-all duration-300 relative overflow-hidden">
            <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-blue-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
            <div className="relative z-10">
              <div className="flex items-center gap-2 sm:gap-3 mb-4 sm:mb-6">
                <div className="p-1.5 sm:p-2 rounded-full bg-blue-500/20 backdrop-blur-sm border border-blue-500/30">
                  <BarChart3 className="w-4 h-4 sm:w-5 sm:h-5 text-blue-400" />
                </div>
                <h3 className="text-base sm:text-lg md:text-xl font-bold bg-gradient-to-r from-slate-100 to-slate-300 bg-clip-text text-transparent">
                  Ticket Volume Trend
                </h3>
              </div>
              <div className="h-64 sm:h-72 md:h-80 flex items-center justify-center border border-slate-700 rounded-xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm p-2 sm:p-3 md:p-4">
                {loading ? (
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-3"></div>
                    <p className="text-slate-500">Loading data...</p>
                  </div>
                ) : error ? (
                  <div className="text-center">
                    <TrendingUp className="w-12 h-12 text-slate-600 mx-auto mb-3" />
                    <p className="text-slate-500">Failed to load data</p>
                    <p className="text-sm text-slate-600 mt-1">{error}</p>
                  </div>
                ) : analyticsData?.ticketVolume && analyticsData.ticketVolume.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={analyticsData.ticketVolume}
                      margin={{ top: 10, right: 10, left: 0, bottom: 20 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                      <XAxis
                        dataKey="date"
                        tick={{ fill: '#9CA3AF', fontSize: 10 }}
                        tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                      />
                      <YAxis
                        tick={{ fill: '#9CA3AF', fontSize: 10 }}
                        tickCount={5}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#1e293b',
                          borderColor: '#334155',
                          borderRadius: '0.5rem',
                          color: '#f8fafc'
                        }}
                        formatter={(value) => [value, 'Tickets']}
                        labelFormatter={(label) => `Date: ${new Date(label).toLocaleDateString()}`}
                      />
                      <Bar
                        dataKey="count"
                        name="Ticket Count"
                        fill="url(#colorGradient)"
                        radius={[4, 4, 0, 0]}
                      >
                        {analyticsData.ticketVolume.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill="#0ea5e9" />
                        ))}
                      </Bar>
                      <defs>
                        <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#0284c7" stopOpacity={0.1}/>
                        </linearGradient>
                      </defs>
                    </BarChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="text-center">
                    <TrendingUp className="w-12 h-12 text-slate-600 mx-auto mb-3" />
                    <p className="text-slate-500">No data available</p>
                    <p className="text-sm text-slate-600 mt-1">Start receiving tickets to see trends</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Channel Distribution */}
          <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl sm:rounded-2xl border border-slate-700 p-4 sm:p-5 md:p-6 hover:shadow-xl transition-all duration-300 relative overflow-hidden">
            <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-pink-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
            <div className="relative z-10">
              <div className="flex items-center gap-2 sm:gap-3 mb-4 sm:mb-6">
                <div className="p-1.5 sm:p-2 rounded-full bg-pink-500/20 backdrop-blur-sm border border-pink-500/30">
                  <MessageSquare className="w-4 h-4 sm:w-5 sm:h-5 text-pink-400" />
                </div>
                <h3 className="text-base sm:text-lg md:text-xl font-bold bg-gradient-to-r from-slate-100 to-slate-300 bg-clip-text text-transparent">
                  Channel Distribution
                </h3>
              </div>
              <div className="h-64 sm:h-72 md:h-80 flex items-center justify-center border border-slate-700 rounded-xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm p-2 sm:p-3 md:p-4">
                {loading ? (
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-pink-500 mx-auto mb-3"></div>
                    <p className="text-slate-500">Loading data...</p>
                  </div>
                ) : error ? (
                  <div className="text-center">
                    <MessageSquare className="w-12 h-12 text-slate-600 mx-auto mb-3" />
                    <p className="text-slate-500">Failed to load data</p>
                    <p className="text-sm text-slate-600 mt-1">{error}</p>
                  </div>
                ) : (
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={[
                          { name: 'Email', value: channelData.email || 0 },
                          { name: 'WhatsApp', value: channelData.whatsapp || 0 },
                          { name: 'Web', value: channelData.web || 0 },
                        ]}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        outerRadius="60%"
                        fill="#8884d8"
                        dataKey="value"
                        label={({ percent = 0 }) => percent > 0 ? `${(percent * 100).toFixed(0)}%` : ''}
                      >
                        <Cell fill="#0ea5e9" />
                        <Cell fill="#10b981" />
                        <Cell fill="#f59e0b" />
                      </Pie>
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#1e293b',
                          borderColor: '#334155',
                          borderRadius: '0.5rem',
                          color: '#f8fafc'
                        }}
                        formatter={(value) => [value, 'Tickets']}
                      />
                      <Legend
                        wrapperStyle={{ fontSize: '12px' }}
                        iconType="circle"
                      />
                    </PieChart>
                  </ResponsiveContainer>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Channel Performance */}
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl sm:rounded-2xl border border-slate-700 p-4 sm:p-5 md:p-6 mx-2">
          <div className="flex items-center gap-2 sm:gap-3 mb-4 sm:mb-6">
            <div className="p-1.5 sm:p-2 rounded-full bg-gradient-to-r from-indigo-500/20 to-purple-500/20 backdrop-blur-sm border border-indigo-500/30">
              <MessageSquare className="w-4 h-4 sm:w-5 sm:h-5 text-indigo-400" />
            </div>
            <h3 className="text-base sm:text-lg md:text-xl font-bold bg-gradient-to-r from-slate-100 to-slate-300 bg-clip-text text-transparent">
              Channel Performance
            </h3>
          </div>
          <div className="space-y-3 sm:space-y-4">
            {['email', 'whatsapp', 'web'].map((channel, index) => {
              const count = channelData[channel] || 0;
              const colors = [
                'from-cyan-500/20 to-blue-500/20',
                'from-green-500/20 to-emerald-500/20',
                'from-yellow-500/20 to-amber-500/20'
              ];
              const color = colors[index % colors.length];

              // Simulate response times based on channel (even for zero counts to maintain consistency)
              const responseTime = channel === 'email' ? '2.1s' :
                                  channel === 'whatsapp' ? '1.8s' : '3.2s';

              if (count === 0) {
                return (
                  <div
                    key={channel}
                    className="group flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-0 p-3 sm:p-4 md:p-5 rounded-xl bg-slate-800/30 border border-slate-700 opacity-70"
                  >
                    <div className="flex items-center gap-3 sm:gap-4">
                      <div className="p-2 sm:p-3 rounded-full bg-gradient-to-br from-slate-600/20 to-slate-500/20 backdrop-blur-sm border-2 border-slate-700">
                        <MessageSquare className="w-5 h-5 sm:w-6 sm:h-6 text-slate-500" />
                      </div>
                      <div>
                        <p className="text-slate-500 font-semibold text-base sm:text-lg capitalize">{channel}</p>
                        <p className="text-xs sm:text-sm text-slate-600">No tickets yet</p>
                      </div>
                    </div>
                    <div className="text-left sm:text-right ml-11 sm:ml-0">
                      <p className="text-slate-500 font-bold text-base sm:text-lg">-</p>
                      <p className="text-xs sm:text-sm text-slate-600 font-medium">Avg response</p>
                    </div>
                  </div>
                );
              } else {
                return (
                  <div
                    key={channel}
                    className="group flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-0 p-3 sm:p-4 md:p-5 rounded-xl bg-slate-800/50 border border-slate-700 hover:border-cyan-500/30 hover:bg-slate-800/70 transition-all duration-300"
                  >
                    <div className="flex items-center gap-3 sm:gap-4">
                      <div className={`p-2 sm:p-3 rounded-full bg-gradient-to-br ${color} backdrop-blur-sm border-2 border-slate-600 group-hover:scale-110 transition-transform duration-300`}>
                        <MessageSquare className="w-5 h-5 sm:w-6 sm:h-6 text-slate-300" />
                      </div>
                      <div>
                        <p className="text-slate-200 font-semibold text-base sm:text-lg capitalize">{channel}</p>
                        <p className="text-xs sm:text-sm text-slate-500">{count} tickets processed</p>
                      </div>
                    </div>
                    <div className="text-left sm:text-right ml-11 sm:ml-0">
                      <p className="text-slate-200 font-bold text-base sm:text-lg">{responseTime}</p>
                      <p className="text-xs sm:text-sm text-slate-400 font-medium">Avg response</p>
                    </div>
                  </div>
                );
              }
            })}
          </div>
        </div>

        {/* Beautiful Footer */}
        <div className="max-w-6xl mx-auto mt-20 pt-12 border-t border-slate-700">
          <div className="text-center">
            <div className="inline-flex items-center gap-3 mb-6 px-6 py-3 rounded-full bg-gradient-to-r from-slate-800 to-slate-900 border border-slate-600 hover:shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300">
              <div className="p-2 rounded-full bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 hover:scale-110 transition-transform duration-300">
                <BarChart3 className="w-5 h-5 text-cyan-400" />
              </div>
              <span className="text-slate-200 text-lg font-semibold hover:text-cyan-400 transition-colors">Business Intelligence Analytics</span>
            </div>

            <p className="text-slate-400 text-sm max-w-2xl mx-auto mb-8 hover:text-slate-300 transition-colors">
              Advanced analytics for data-driven customer success decisions. Real-time insights for operational excellence.
            </p>

            <div className="flex flex-wrap justify-center gap-8 text-xs text-slate-500 mb-8">
              <span className="hover:text-cyan-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-cyan-400/50 pb-1">Performance Metrics</span>
              <span className="hover:text-blue-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-blue-400/50 pb-1">Channel Insights</span>
              <span className="hover:text-purple-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-purple-400/50 pb-1">Trend Analysis</span>
              <span className="hover:text-emerald-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-emerald-400/50 pb-1">Business Intelligence</span>
              <span className="hover:text-amber-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-amber-400/50 pb-1">Data Visualization</span>
            </div>

            <div className="border-t border-slate-700 pt-8">
              <p className="text-slate-500 text-sm hover:text-slate-400 transition-colors">
                © 2026 TaskFlow AI Analytics Dashboard. Built for the CRM Digital FTE Factory Final Hackathon 5.
              </p>
              <p className="text-slate-600 text-xs mt-2 hover:text-slate-500 transition-colors">
                Transforming customer data into strategic business insights.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}