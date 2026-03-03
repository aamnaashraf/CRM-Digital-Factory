"use client";

import { useState, useEffect } from "react";
import { FileText, Download, Calendar, TrendingUp, AlertTriangle, ThumbsUp, ThumbsDown, Zap, Brain, Shield } from "lucide-react";
import { apiClient } from "@/lib/api";
import { format } from "date-fns";

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:7860';

interface DailyReport {
  report_date: string;
  period_start: string;
  period_end: string;
  metrics: {
    total_messages: number;
    positive_interactions: number;
    neutral_interactions: number;
    negative_interactions: number;
    average_sentiment_score: number;
    total_conversations: number;
    escalations: number;
    positive_ratio: number;
    negative_ratio: number;
    escalation_rate: number;
  };
  channel_breakdown: Record<string, any>;
  top_negative_topics: string[];
  trend_comparison: {
    message_volume_change: number;
    sentiment_trend: number;
  };
}

interface ReportSummary {
  date: string;
  total_messages: number;
  average_sentiment: number;
  escalations: number;
}

export default function DailyReportsPage() {
  const [reports, setReports] = useState<ReportSummary[]>([]);
  const [selectedReport, setSelectedReport] = useState<DailyReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [reportLoading, setReportLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchReportSummaries();
  }, []);

  const fetchReportSummaries = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getDailyReports();
      setReports(response.data);
    } catch (err) {
      console.error("Failed to fetch report summaries:", err);
      setError("Failed to load report summaries");
    } finally {
      setLoading(false);
    }
  };

  const handleViewReport = async (date: string) => {
    try {
      setReportLoading(true);
      const response = await apiClient.getDailyReport(date);
      setSelectedReport(response.data);
    } catch (err) {
      console.error("Failed to fetch daily report:", err);
      setError("Failed to load daily report");
    } finally {
      setReportLoading(false);
    }
  };

  const handleDownloadReport = (date: string) => {
    // Direct file download via URL
    window.open(`${API_BASE_URL}/api/reports/sentiment/download/${date}`, '_blank');
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
            <span className="text-blue-400 text-sm font-medium">AI-Powered Sentiment Analytics</span>
          </div>

          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 from-green-400 via-teal-500 to-emerald-500 to-purple-500 bg-clip-text text-transparent mb-6">
            Customer Sentiment Intelligence
          </h1>

          <p className="text-slate-400 text-xl max-w-3xl mx-auto leading-relaxed">
            Advanced analytics dashboard for customer sentiment tracking, engagement metrics, and performance insights.
          </p>
        </div>

        <div className="max-w-6xl mx-auto mb-16">
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 bg-clip-text text-transparent mb-4 group-hover:scale-105 transition-transform duration-300">
              <span className="group inline-block">
                Available Reports
              </span>
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto group-hover:text-slate-300 transition-colors">
              Browse daily sentiment analysis reports and customer engagement metrics
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Report List */}
            <div className="lg:col-span-1">
              <div className="group bg-gradient-to-br from-slate-800/60 to-slate-900/60 backdrop-blur-sm rounded-3xl border border-slate-700/50 p-6 hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-500">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-3">
                    <div className="p-3 rounded-full bg-blue-500/20 backdrop-blur-sm border border-blue-500/30 group-hover:scale-110 transition-transform duration-300">
                      <FileText className="w-6 h-6 text-blue-400" />
                    </div>
                    <h3 className="text-xl font-semibold text-slate-200 group-hover:text-blue-400 transition-colors">Sentiment Reports</h3>
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold text-slate-300">{reports.length}</p>
                    <p className="text-xs text-slate-500">Reports</p>
                  </div>
                </div>

                {loading ? (
                  <div className="text-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-3"></div>
                    <p className="text-slate-500">Loading reports...</p>
                  </div>
                ) : error ? (
                  <div className="text-center py-8">
                    <AlertTriangle className="w-12 h-12 text-slate-600 mx-auto mb-3" />
                    <p className="text-slate-500">{error}</p>
                  </div>
                ) : reports.length === 0 ? (
                  <div className="text-center py-8">
                    <FileText className="w-12 h-12 text-slate-600 mx-auto mb-3" />
                    <p className="text-slate-500">No reports available</p>
                    <p className="text-sm text-slate-600 mt-1">Reports are generated daily at 11:59 PM</p>
                  </div>
                ) : (
                  <div className="space-y-4 max-h-[600px] overflow-y-auto">
                    {reports.map((report) => (
                      <div
                        key={report.date}
                        className={`p-5 rounded-2xl border cursor-pointer transition-all duration-300 transform hover:scale-[1.02] ${
                          selectedReport?.report_date?.split('T')[0] === report.date
                            ? 'bg-gradient-to-r from-blue-500/10 to-cyan-500/10 border-cyan-500/50 shadow-lg shadow-cyan-500/10'
                            : 'bg-gradient-to-r from-slate-800/50 to-slate-700/30 border-slate-700/50 hover:border-slate-600'
                        }`}
                        onClick={() => handleViewReport(report.date)}
                      >
                        <div className="flex justify-between items-start mb-3">
                          <div className="flex items-center gap-2">
                            <Calendar className="w-5 h-5 text-slate-500" />
                            <span className="text-slate-200 font-medium">{report.date}</span>
                          </div>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDownloadReport(report.date);
                            }}
                            className="p-2 rounded-full hover:bg-slate-600/50 transition-colors group/download"
                          >
                            <Download className="w-4 h-4 text-slate-400 group-hover/download:text-cyan-400 transition-colors" />
                          </button>
                        </div>
                        <div className="grid grid-cols-3 gap-2 text-xs">
                          <div className="text-center">
                            <div className="text-slate-500">Messages</div>
                            <div className="text-slate-300 font-medium">{report.total_messages}</div>
                          </div>
                          <div className="text-center">
                            <div className="text-slate-500">Avg Sentiment</div>
                            <div className="text-slate-300 font-medium">
                              {report.average_sentiment?.toFixed(2)}
                            </div>
                          </div>
                          <div className="text-center">
                            <div className="text-slate-500">Escalations</div>
                            <div className="text-slate-300 font-medium">{report.escalations}</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Report Details */}
            <div className="lg:col-span-2">
              <div className="group bg-gradient-to-br from-slate-800/60 to-slate-900/60 backdrop-blur-sm rounded-3xl border border-slate-700/50 p-8 hover:shadow-2xl hover:shadow-indigo-500/10 transition-all duration-500">
                <div className="flex items-center justify-between mb-8">
                  <div className="flex items-center gap-3">
                    <div className="p-3 rounded-full bg-indigo-500/20 backdrop-blur-sm border border-indigo-500/30 group-hover:scale-110 transition-transform duration-300">
                      <TrendingUp className="w-6 h-6 text-indigo-400" />
                    </div>
                    <h3 className="text-xl font-semibold text-slate-200 group-hover:text-indigo-400 transition-colors">Detailed Analysis</h3>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-slate-500">Report Details</p>
                  </div>
                </div>

                {reportLoading ? (
                  <div className="text-center py-12">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500 mx-auto mb-3"></div>
                    <p className="text-slate-500">Loading report details...</p>
                  </div>
                ) : selectedReport ? (
                  <div className="space-y-8">
                    {/* Report Header */}
                    <div className="bg-gradient-to-r from-slate-800/50 to-slate-700/30 rounded-2xl p-6 border border-slate-700/50">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="group/item">
                          <div className="text-slate-400 text-sm mb-1">Report Period</div>
                          <div className="text-slate-200 font-semibold group-hover/item:text-cyan-400 transition-colors">
                            {new Date(selectedReport.report_date).toLocaleDateString()}
                          </div>
                        </div>
                        <div className="group/item">
                          <div className="text-slate-400 text-sm mb-1">Time Range</div>
                          <div className="text-slate-200 font-semibold group-hover/item:text-purple-400 transition-colors">
                            {new Date(selectedReport.period_start).toLocaleDateString()} - {new Date(selectedReport.period_end).toLocaleDateString()}
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Key Metrics */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                      <div className="group bg-gradient-to-br from-slate-800/50 to-slate-700/30 rounded-2xl p-6 border border-slate-700/50 hover:shadow-lg hover:shadow-cyan-500/10 transition-all duration-300">
                        <div className="text-slate-400 text-sm mb-2">Total Messages</div>
                        <div className="text-3xl font-bold text-cyan-400 group-hover:text-cyan-300 transition-colors">
                          {selectedReport.metrics.total_messages}
                        </div>
                        <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden mt-3">
                          <div className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full w-full transition-all duration-1000 ease-out"></div>
                        </div>
                      </div>
                      <div className="group bg-gradient-to-br from-slate-800/50 to-slate-700/30 rounded-2xl p-6 border border-slate-700/50 hover:shadow-lg hover:shadow-slate-500/10 transition-all duration-300">
                        <div className="text-slate-400 text-sm mb-2">Avg Sentiment</div>
                        <div className="text-3xl font-bold text-slate-200 group-hover:text-slate-100 transition-colors">
                          {selectedReport.metrics.average_sentiment_score.toFixed(2)}
                        </div>
                        <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden mt-3">
                          <div className="h-full bg-gradient-to-r from-slate-500 to-slate-400 rounded-full w-2/3 transition-all duration-1000 ease-out"></div>
                        </div>
                      </div>
                      <div className="group bg-gradient-to-br from-slate-800/50 to-slate-700/30 rounded-2xl p-6 border border-slate-700/50 hover:shadow-lg hover:shadow-green-500/10 transition-all duration-300">
                        <div className="text-slate-400 text-sm mb-2">Conversations</div>
                        <div className="text-3xl font-bold text-green-400 group-hover:text-green-300 transition-colors">
                          {selectedReport.metrics.total_conversations}
                        </div>
                        <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden mt-3">
                          <div className="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-full w-4/5 transition-all duration-1000 ease-out"></div>
                        </div>
                      </div>
                      <div className="group bg-gradient-to-br from-slate-800/50 to-slate-700/30 rounded-2xl p-6 border border-slate-700/50 hover:shadow-lg hover:shadow-orange-500/10 transition-all duration-300">
                        <div className="text-slate-400 text-sm mb-2">Escalations</div>
                        <div className="text-3xl font-bold text-orange-400 group-hover:text-orange-300 transition-colors">
                          {selectedReport.metrics.escalations}
                        </div>
                        <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden mt-3">
                          <div className="h-full bg-gradient-to-r from-orange-500 to-red-500 rounded-full w-1/4 transition-all duration-1000 ease-out"></div>
                        </div>
                      </div>
                    </div>

                    {/* Sentiment Breakdown */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div className="group bg-gradient-to-br from-green-500/10 to-emerald-500/10 rounded-2xl p-6 border border-green-500/20 hover:shadow-lg hover:shadow-green-500/20 transition-all duration-300">
                        <div className="flex items-center gap-3 mb-4 group/item">
                          <ThumbsUp className="w-6 h-6 text-green-400" />
                          <div className="text-green-400 text-sm font-medium group-hover/item:text-green-300 transition-colors">Positive</div>
                        </div>
                        <div className="text-2xl font-bold text-green-400 mb-2 group-hover:text-green-300 transition-colors">
                          {selectedReport.metrics.positive_interactions}
                        </div>
                        <div className="text-sm text-green-400/80">
                          {selectedReport.metrics.positive_ratio}%
                        </div>
                        <div className="h-2 bg-green-500/20 rounded-full overflow-hidden mt-4">
                          <div className="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-full w-1/4 transition-all duration-1000 ease-out group-hover:w-1/2"></div>
                        </div>
                      </div>

                      <div className="group bg-gradient-to-br from-slate-600/10 to-slate-500/10 rounded-2xl p-6 border border-slate-600/20 hover:shadow-lg hover:shadow-slate-500/20 transition-all duration-300">
                        <div className="flex items-center gap-3 mb-4 group/item">
                          <div className="w-6 h-6 text-slate-400"></div>
                          <div className="text-slate-400 text-sm font-medium group-hover/item:text-slate-300 transition-colors">Neutral</div>
                        </div>
                        <div className="text-2xl font-bold text-slate-400 mb-2 group-hover:text-slate-300 transition-colors">
                          {selectedReport.metrics.neutral_interactions}
                        </div>
                        <div className="text-sm text-slate-400/80">
                          {((selectedReport.metrics.neutral_interactions / selectedReport.metrics.total_messages) * 100 || 0).toFixed(1)}%
                        </div>
                        <div className="h-2 bg-slate-600/20 rounded-full overflow-hidden mt-4">
                          <div className="h-full bg-gradient-to-r from-slate-600 to-slate-500 rounded-full w-2/3 transition-all duration-1000 ease-out group-hover:w-3/4"></div>
                        </div>
                      </div>

                      <div className="group bg-gradient-to-br from-red-500/10 to-pink-500/10 rounded-2xl p-6 border border-red-500/20 hover:shadow-lg hover:shadow-red-500/20 transition-all duration-300">
                        <div className="flex items-center gap-3 mb-4 group/item">
                          <ThumbsDown className="w-6 h-6 text-red-400" />
                          <div className="text-red-400 text-sm font-medium group-hover/item:text-red-300 transition-colors">Negative</div>
                        </div>
                        <div className="text-2xl font-bold text-red-400 mb-2 group-hover:text-red-300 transition-colors">
                          {selectedReport.metrics.negative_interactions}
                        </div>
                        <div className="text-sm text-red-400/80">
                          {selectedReport.metrics.negative_ratio}%
                        </div>
                        <div className="h-2 bg-red-500/20 rounded-full overflow-hidden mt-4">
                          <div className="h-full bg-gradient-to-r from-red-500 to-pink-500 rounded-full w-1/10 transition-all duration-1000 ease-out group-hover:w-1/5"></div>
                        </div>
                      </div>
                    </div>

                    {/* Channel Breakdown */}
                    <div className="group">
                      <div className="text-slate-400 text-sm mb-4 flex items-center gap-2">
                        <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></div>
                        Channel Breakdown
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {Object.entries(selectedReport.channel_breakdown).map(([channel, data]: [string, any]) => (
                          <div key={channel} className="group/item bg-gradient-to-br from-slate-800/40 to-slate-700/30 rounded-2xl p-5 border border-slate-700/50 hover:shadow-lg hover:shadow-cyan-500/10 transition-all duration-300">
                            <div className="text-slate-200 font-semibold capitalize group-hover/item:text-cyan-400 transition-colors">{channel}</div>
                            <div className="text-sm text-slate-400">
                              {data.positive + data.neutral + data.negative} interactions
                            </div>
                            <div className="flex gap-2 mt-3">
                              <div className="flex-1 bg-green-500/20 h-3 rounded group-hover:bg-green-500/40 transition-colors"></div>
                              <div className="flex-1 bg-slate-500/20 h-3 rounded group-hover:bg-slate-500/40 transition-colors"></div>
                              <div className="flex-1 bg-red-500/20 h-3 rounded group-hover:bg-red-500/40 transition-colors"></div>
                            </div>
                            <div className="flex justify-between text-xs text-slate-500 mt-2">
                              <span className="text-green-400">P:{data.positive}</span>
                              <span className="text-slate-400">N:{data.neutral}</span>
                              <span className="text-red-400">N:{data.negative}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Top Negative Topics */}
                    {selectedReport.top_negative_topics.length > 0 && (
                      <div className="group">
                        <div className="text-slate-400 text-sm mb-4 flex items-center gap-2">
                          <div className="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
                          Top Negative Topics
                        </div>
                        <div className="space-y-3">
                          {selectedReport.top_negative_topics.map((topic, index) => (
                            <div key={index} className="group/item bg-gradient-to-r from-red-500/5 to-pink-500/5 rounded-xl p-4 border border-red-500/10 hover:shadow-lg hover:shadow-red-500/10 transition-all duration-300">
                              <div className="text-red-300 text-sm group-hover/item:text-red-200 transition-colors">{topic}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Trend Comparison */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="group bg-gradient-to-br from-slate-800/50 to-slate-700/30 rounded-2xl p-6 border border-slate-700/50 hover:shadow-lg hover:shadow-green-500/10 transition-all duration-300">
                        <div className="text-slate-400 text-sm mb-2">Message Volume Change</div>
                        <div className={`text-2xl font-bold ${selectedReport.trend_comparison.message_volume_change >= 0 ? 'text-green-400' : 'text-red-400'} group-hover:text-green-300 transition-colors`}>
                          {selectedReport.trend_comparison.message_volume_change >= 0 ? '+' : ''}{selectedReport.trend_comparison.message_volume_change}%
                        </div>
                        <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden mt-3">
                          <div className={`h-full ${selectedReport.trend_comparison.message_volume_change >= 0 ? 'bg-gradient-to-r from-green-500 to-emerald-500' : 'bg-gradient-to-r from-red-500 to-pink-500'} rounded-full w-3/4 transition-all duration-1000 ease-out`}></div>
                        </div>
                      </div>
                      <div className="group bg-gradient-to-br from-slate-800/50 to-slate-700/30 rounded-2xl p-6 border border-slate-700/50 hover:shadow-lg hover:shadow-purple-500/10 transition-all duration-300">
                        <div className="text-slate-400 text-sm mb-2">Sentiment Trend</div>
                        <div className={`text-2xl font-bold ${selectedReport.trend_comparison.sentiment_trend >= 0 ? 'text-green-400' : 'text-red-400'} group-hover:text-purple-300 transition-colors`}>
                          {selectedReport.trend_comparison.sentiment_trend >= 0 ? '+' : ''}{selectedReport.trend_comparison.sentiment_trend.toFixed(3)}
                        </div>
                        <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden mt-3">
                          <div className={`h-full ${selectedReport.trend_comparison.sentiment_trend >= 0 ? 'bg-gradient-to-r from-green-500 to-emerald-500' : 'bg-gradient-to-r from-red-500 to-pink-500'} rounded-full w-2/3 transition-all duration-1000 ease-out`}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <FileText className="w-16 h-16 text-slate-600 mx-auto mb-6" />
                    <p className="text-slate-500 text-xl mb-2">Select a report to view details</p>
                    <p className="text-sm text-slate-600">Choose from the available reports to see detailed analysis</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Impact Section */}
        <div className="max-w-6xl mx-auto mt-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-slate-100 to-slate-300 bg-clip-text text-transparent mb-4">
              Report Insights
            </h2>
            <p className="text-slate-500 max-w-2xl mx-auto">
              Transform customer sentiment data into actionable business intelligence
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-8 hover:shadow-2xl hover:scale-[1.01] transition-all duration-300">
              <h3 className="text-xl font-bold text-slate-200 mb-4 flex items-center gap-2 group-hover:text-yellow-400 transition-colors">
                <Zap className="w-5 h-5 text-yellow-400" />
                Performance Analysis
              </h3>
              <ul className="space-y-3 text-slate-300">
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Detailed sentiment breakdown by channel and topic</span>
                </li>
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Escalation pattern identification and trend analysis</span>
                </li>
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Customer satisfaction metrics over time</span>
                </li>
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Proactive identification of negative topics</span>
                </li>
              </ul>
            </div>

            <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-8 hover:shadow-2xl hover:scale-[1.01] transition-all duration-300">
              <h3 className="text-xl font-bold text-slate-200 mb-4 flex items-center gap-2 group-hover:text-green-400 transition-colors">
                <Brain className="w-5 h-5 text-green-400" />
                Strategic Intelligence
              </h3>
              <ul className="space-y-3 text-slate-300">
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-green-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>AI-powered sentiment analysis across all channels</span>
                </li>
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-green-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Real-time performance tracking and alerts</span>
                </li>
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-green-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Automated report generation and trend comparisons</span>
                </li>
                <li className="flex items-start gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 bg-green-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Early warning system for potential issues</span>
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
              <span className="text-slate-200 text-lg font-semibold hover:text-cyan-400 transition-colors">Customer Sentiment Intelligence</span>
            </div>

            <p className="text-slate-400 text-sm max-w-2xl mx-auto mb-8 hover:text-slate-300 transition-colors">
              Actionable insights from customer sentiment data. Automated analysis for proactive customer success.
            </p>

            <div className="flex flex-wrap justify-center gap-8 text-xs text-slate-500 mb-8">
              <span className="hover:text-cyan-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-cyan-400/50 pb-1">Sentiment Analysis</span>
              <span className="hover:text-blue-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-blue-400/50 pb-1">Trend Reports</span>
              <span className="hover:text-purple-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-purple-400/50 pb-1">Channel Insights</span>
              <span className="hover:text-emerald-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-emerald-400/50 pb-1">Performance Metrics</span>
              <span className="hover:text-amber-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-amber-400/50 pb-1">AI Intelligence</span>
            </div>

            <div className="border-t border-slate-700 pt-8">
              <p className="text-slate-500 text-sm hover:text-slate-400 transition-colors">
                © 2026 Customer Sentiment Intelligence Dashboard. Built for the CRM Digital FTE Factory Final Hackathon 5.
              </p>
              <p className="text-slate-600 text-xs mt-2 hover:text-slate-500 transition-colors">
                Transforming customer feedback into strategic business value.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}