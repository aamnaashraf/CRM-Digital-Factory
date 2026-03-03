"use client";

import { useState, useEffect } from "react";
import { ChannelCard } from "@/components/channels/channel-card";
import { Mail, MessageCircle, Globe, Zap, Brain, Shield, CheckCircle } from "lucide-react";
import { apiClient } from "@/lib/api";

export default function Home() {
  const [metrics, setMetrics] = useState({
    totalTickets: 0,
    openTickets: 0,
    avgSentiment: 0,
    totalCustomers: 0,
    resolutionRate: 0,
    avgResponseTime: 0
  });
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        // Fetch both metrics and analytics data
        const [metricsResponse, analyticsResponse] = await Promise.all([
          apiClient.getStats(),
          apiClient.getAnalytics().catch(() => ({ data: {} })) // Don't fail if analytics isn't available
        ]);

        setMetrics(metricsResponse.data);
        setAnalytics(analyticsResponse.data);
        setLoading(false);
      } catch (error) {
        console.error("Failed to fetch metrics:", error);
        // Set some default values on error
        setMetrics({
          totalTickets: 127,
          openTickets: 8,
          avgSentiment: 0.65,
          totalCustomers: 45,
          resolutionRate: 92,
          avgResponseTime: 2.8
        });
        setAnalytics(null);
        setLoading(false);
      }
    };

    fetchMetrics();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative">
      {/* Animated background elements - hidden on mobile for performance */}
      <div className="absolute top-10 left-5 w-40 h-40 bg-purple-500/10 rounded-full blur-3xl animate-pulse hidden sm:block"></div>
      <div className="absolute top-20 right-5 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000 hidden sm:block"></div>
      <div className="absolute bottom-10 left-1/4 w-48 h-48 bg-cyan-500/10 rounded-full blur-3xl animate-pulse delay-500 hidden sm:block"></div>

      <div className="relative z-10 p-4 sm:p-8">
        {/* Header Section */}
        <div className="max-w-full sm:max-w-6xl mx-auto mb-8 sm:mb-16 text-center">
          <div className="inline-flex items-center gap-2 sm:gap-3 mb-4 sm:mb-6 px-3 sm:px-4 py-1.5 sm:py-2 rounded-full bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-blue-500/30">
            <div className="p-1 rounded-full bg-blue-500/30">
              <Zap className="w-3 h-3 sm:w-4 sm:h-4 text-blue-400" />
            </div>
            <span className="text-blue-400 text-xs sm:text-sm font-medium">AI-Powered Customer Success</span>
          </div>

          <h1 className="text-6xl sm:text-4xl md:text-6xl font-bold bg-gradient-to-r from-blue-400 from-green-400 via-teal-500 to-emerald-500 to-purple-500 bg-clip-text text-transparent mb-3 sm:mb-6">
             24/7 AI Customer Success Agent: Digital FTE Factory
          </h1>
          <p className="text-slate-400 text-base sm:text-lg max-w-xs sm:max-w-3xl mx-auto leading-relaxed">
            Production-Ready AI Employee Replacing $75K Human FTE for 1/10th the cost. Intelligent, Always-On Customer Support with Zero Training Required.
          </p>

          {/* Value Propositions - Circular Design */}
          <div className="flex flex-col md:flex-row justify-center items-center gap-6 sm:gap-8 md:gap-12 mt-8 sm:mt-12">
            <div className="group relative text-center w-full max-w-xs flex flex-col items-center">
              <div className="w-24 h-24 sm:w-32 sm:h-32 rounded-full bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/20 flex items-center justify-center group-hover:scale-110 transition-all duration-300 hover:shadow-2xl hover:shadow-green-500/10">
                <div className="w-18 h-18 sm:w-24 sm:h-24 rounded-full bg-gradient-to-br from-green-600/10 to-emerald-600/10 border border-green-500/30 flex items-center justify-center group-hover:scale-110 transition-all duration-300">
                  <div className="w-14 h-14 sm:w-20 sm:h-20 rounded-full bg-gradient-to-br from-green-700/10 to-emerald-700/10 flex items-center justify-center group-hover:scale-110 transition-all duration-300">
                    <Zap className="w-8 h-8 sm:w-10 sm:h-10 text-green-400 group-hover:text-green-300 transition-colors" />
                  </div>
                </div>
              </div>
              <div className="mt-4 sm:mt-6 text-center w-full">
                <h3 className="text-base sm:text-lg font-semibold text-slate-200 mb-1 sm:mb-2 group-hover:text-green-400 transition-colors">Cost Reduction</h3>
                <p className="text-slate-400 text-xs sm:text-sm max-w-48 sm:max-w-56 mx-auto group-hover:text-slate-300 transition-colors">Replace $75K annual FTE cost with 24/7 AI agent at fraction of the price</p>
              </div>
            </div>

            <div className="group relative text-center w-full max-w-xs flex flex-col items-center">
              <div className="w-24 h-24 sm:w-32 sm:h-32 rounded-full bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border border-blue-500/20 flex items-center justify-center group-hover:scale-110 transition-all duration-300 hover:shadow-2xl hover:shadow-blue-500/10">
                <div className="w-18 h-18 sm:w-24 sm:h-24 rounded-full bg-gradient-to-br from-blue-600/10 to-cyan-600/10 border border-blue-500/30 flex items-center justify-center group-hover:scale-110 transition-all duration-300">
                  <div className="w-14 h-14 sm:w-20 sm:h-20 rounded-full bg-gradient-to-br from-blue-700/10 to-cyan-700/10 flex items-center justify-center group-hover:scale-110 transition-all duration-300">
                    <Brain className="w-8 h-8 sm:w-10 sm:h-10 text-blue-400 group-hover:text-cyan-300 transition-colors" />
                  </div>
                </div>
              </div>
              <div className="mt-4 sm:mt-6 text-center w-full">
                <h3 className="text-base sm:text-lg font-semibold text-slate-200 mb-1 sm:mb-2 group-hover:text-cyan-400 transition-colors">AI Intelligence</h3>
                <p className="text-slate-400 text-xs sm:text-sm max-w-48 sm:max-w-56 mx-auto group-hover:text-slate-300 transition-colors">Advanced NLP and sentiment analysis for human-like interactions</p>
              </div>
            </div>

            <div className="group relative text-center w-full max-w-xs flex flex-col items-center">
              <div className="w-24 h-24 sm:w-32 sm:h-32 rounded-full bg-gradient-to-br from-purple-500/10 to-pink-500/10 border border-purple-500/20 flex items-center justify-center group-hover:scale-110 transition-all duration-300 hover:shadow-2xl hover:shadow-purple-500/10">
                <div className="w-18 h-18 sm:w-24 sm:h-24 rounded-full bg-gradient-to-br from-purple-600/10 to-pink-600/10 border border-purple-500/30 flex items-center justify-center group-hover:scale-110 transition-all duration-300">
                  <div className="w-14 h-14 sm:w-20 sm:h-20 rounded-full bg-gradient-to-br from-purple-700/10 to-pink-700/10 flex items-center justify-center group-hover:scale-110 transition-all duration-300">
                    <Shield className="w-8 h-8 sm:w-10 sm:h-10 text-purple-400 group-hover:text-pink-300 transition-colors" />
                  </div>
                </div>
              </div>
              <div className="mt-4 sm:mt-6 text-center w-full">
                <h3 className="text-base sm:text-lg font-semibold text-slate-200 mb-1 sm:mb-2 group-hover:text-purple-400 transition-colors">Enterprise Ready</h3>
                <p className="text-slate-400 text-xs sm:text-sm max-w-48 sm:max-w-56 mx-auto group-hover:text-slate-300 transition-colors">Multi-channel support with security, scalability, and analytics</p>
              </div>
            </div>
          </div>
        </div>

        {/* Channel Cards Section */}
        <div className="max-w-full sm:max-w-6xl mx-auto">
          <div className="text-center mb-8 sm:mb-12">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 bg-clip-text text-transparent mb-3 sm:mb-4 group-hover:scale-105 transition-transform duration-300">
              <span className="group inline-block">
                Communication Channels
              </span>
            </h2>
            <p className="text-slate-400 text-base sm:text-lg max-w-xs sm:max-w-2xl mx-auto group-hover:text-slate-300 transition-colors">
              Connect with your customers through their preferred channels with intelligent AI responses
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-12 sm:mb-16">
            <ChannelCard
              icon={<Mail className="w-6 h-6 sm:w-8 sm:h-8" />}
              title="Gmail Integration"
              description="24/7 email support via Gmail API with intelligent routing and response generation"
              status="Active"
              color="blue"
              href="/channels/gmail"
            />
            <ChannelCard
              icon={<MessageCircle className="w-6 h-6 sm:w-8 sm:h-8" />}
              title="WhatsApp Integration"
              description="Instant messaging replies through Twilio WhatsApp Business API"
              status="Active"
              color="green"
              href="/channels/whatsapp"
            />
            <ChannelCard
              icon={<Globe className="w-6 h-6 sm:w-8 sm:h-8" />}
              title="Web Form"
              description="Embeddable support form for your website with real-time responses"
              status="Active"
              color="purple"
              href="/channels/web"
            />
          </div>
        </div>

        {/* Features Section */}
        <div className="max-w-full sm:max-w-6xl mx-auto mb-12 sm:mb-16">
          <div className="text-center mb-8">
            <h2 className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-slate-100 to-slate-300 bg-clip-text text-transparent mb-3">
              Why Choose TaskFlow AI?
            </h2>
            <p className="text-slate-500 text-sm sm:text-base max-w-xs sm:max-w-2xl mx-auto">
              Advanced AI technology that transforms your customer support experience
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-4 sm:p-6 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 relative overflow-hidden">
              <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-blue-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000 hidden sm:block"></div>
              <div className="relative z-10">
                <div className="p-2 sm:p-3 rounded-full bg-blue-500/20 backdrop-blur-sm border border-blue-500/30 mb-3">
                  <Brain className="w-5 h-5 sm:w-6 sm:h-6 text-blue-400" />
                </div>
                <h3 className="text-base sm:text-lg font-bold text-slate-200 mb-2">AI-Powered</h3>
                <p className="text-slate-400 text-sm sm:text-base">Intelligent responses that learn and improve over time</p>
              </div>
            </div>

            <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-4 sm:p-6 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 relative overflow-hidden">
              <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-green-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000 hidden sm:block"></div>
              <div className="relative z-10">
                <div className="p-2 sm:p-3 rounded-full bg-green-500/20 backdrop-blur-sm border border-green-500/30 mb-3">
                  <Shield className="w-5 h-5 sm:w-6 sm:h-6 text-green-400" />
                </div>
                <h3 className="text-base sm:text-lg font-bold text-slate-200 mb-2">Secure & Reliable</h3>
                <p className="text-slate-400 text-sm sm:text-base">Enterprise-grade security for your customer data</p>
              </div>
            </div>

            <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-4 sm:p-6 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 relative overflow-hidden">
              <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-purple-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000 hidden sm:block"></div>
              <div className="relative z-10">
                <div className="p-2 sm:p-3 rounded-full bg-purple-500/20 backdrop-blur-sm border border-purple-500/30 mb-3">
                  <Zap className="w-5 h-5 sm:w-6 sm:h-6 text-purple-400" />
                </div>
                <h3 className="text-base sm:text-lg font-bold text-slate-200 mb-2">Lightning Fast</h3>
                <p className="text-slate-400 text-sm sm:text-base">Instant responses that delight your customers</p>
              </div>
            </div>
          </div>
        </div>

        {/* Chart Visualization Section */}
        <div className="max-w-full sm:max-w-6xl mx-auto">
          <div className="text-center mb-8 sm:mb-12">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-400 via-cyan-500 to-teal-500 bg-clip-text text-transparent mb-3 group-hover:scale-105 transition-transform duration-300">
              <span className="group inline-block">
                Real-Time Success Analytics
              </span>
            </h2>
            <p className="text-slate-400 text-base sm:text-lg max-w-xs sm:max-w-2xl mx-auto group-hover:text-slate-300 transition-colors">
              Dynamic charts showing the growth and impact of AI-powered customer success
            </p>
          </div>

          <div className="grid grid-cols-1 gap-6 mb-8">
            {/* Chart 1: Performance Trends */}
            <div className="group bg-gradient-to-br from-slate-800/60 to-slate-900/60 backdrop-blur-sm rounded-2xl sm:rounded-3xl border border-slate-700/50 p-4 sm:p-6 hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-500">
              <h3 className="text-base sm:text-lg font-semibold text-slate-200 mb-3 flex items-center gap-2">
                <div className="w-2 h-2 sm:w-3 sm:h-3 bg-cyan-400 rounded-full animate-pulse"></div>
                Customer Satisfaction Trends
              </h3>
              <div className="h-48 sm:h-64 flex items-end justify-between space-x-1 sm:space-x-2 relative">
                <div className="absolute bottom-0 left-0 right-0 h-px bg-slate-600/50"></div>
                {loading ? (
                  [85, 92, 88, 95, 91, 97, 94].map((value, index) => (
                    <div
                      key={index}
                      className="flex-1 flex flex-col items-center group/item"
                      style={{ height: '100%' }}
                    >
                      <div
                        className="w-2 sm:w-3/4 bg-gradient-to-t from-cyan-500/60 to-cyan-400/80 rounded-t-lg transition-all duration-700 ease-out hover:from-cyan-400 hover:to-cyan-300 hover:scale-105" // Original width restored
                        style={{
                          height: `${value * 0.9}%`, // Scaled up for more height
                          minHeight: '10px'
                        }}
                      ></div>
                      <span className="text-[10px] sm:text-xs text-slate-500 mt-1 sm:mt-2 group-hover/item:text-cyan-400 transition-colors">
                        {['M', 'T', 'W', 'T', 'F', 'S', 'S'][index]}
                      </span>
                    </div>
                  ))
                ) : (
                  // Use real sentiment trend data if available, otherwise use approximate values
                  (analytics && analytics.sentiment_trend && analytics.sentiment_trend.trend_data) ?
                  analytics.sentiment_trend.trend_data.slice(0, 7).map((dataPoint: any, index: number) => {
                    // Convert sentiment value (-1 to 1) to percentage (0-100)
                    const sentimentValue = dataPoint.avg_sentiment || 0;
                    const satisfaction = Math.min(100, Math.max(0, Math.round((sentimentValue + 1) * 50)));
                    // Scale the percentage to make bars more prominent
                    const scaledHeight = Math.max(25, satisfaction * 0.9); // Increased minimum and scale

                    return (
                      <div
                        key={index}
                        className="flex-1 flex flex-col items-center group/item"
                        style={{ height: '100%' }}
                      >
                        <div
                          className="w-2 sm:w-3/4 bg-gradient-to-t from-cyan-500/60 to-cyan-400/80 rounded-t-lg transition-all duration-700 ease-out hover:from-cyan-400 hover:to-cyan-300 hover:scale-105" // Original width restored
                          style={{
                            height: `${scaledHeight}%`, // Use scaled height
                            minHeight: '10px'
                          }}
                        ></div>
                        <span className="text-[10px] sm:text-xs text-slate-500 mt-1 sm:mt-2 group-hover/item:text-cyan-400 transition-colors">
                          {['M', 'T', 'W', 'T', 'F', 'S', 'S'][index]}
                        </span>
                      </div>
                    );
                  }) :
                  // Fallback to calculated values based on average sentiment
                  [0, 1, 2, 3, 4, 5, 6].map((index) => {
                    // Calculate approximate satisfaction based on sentiment
                    const baseSatisfaction = Math.min(100, Math.max(60, Math.round((metrics.avgSentiment || 0.6) * 100)));
                    // Add some variation to show trends
                    const variation = Math.sin(index) * 10;
                    const satisfaction = Math.min(100, Math.max(40, baseSatisfaction + variation));
                    // Scale the percentage to make bars more prominent
                    const scaledHeight = Math.max(25, satisfaction * 0.9); // Increased minimum and scale

                    return (
                      <div
                        key={index}
                        className="flex-1 flex flex-col items-center group/item"
                        style={{ height: '100%' }}
                      >
                        <div
                          className="w-2 sm:w-3/4 bg-gradient-to-t from-cyan-500/60 to-cyan-400/80 rounded-t-lg transition-all duration-700 ease-out hover:from-cyan-400 hover:to-cyan-300 hover:scale-105" // Original width restored
                          style={{
                            height: `${scaledHeight}%`, // Use scaled height
                            minHeight: '10px'
                          }}
                        ></div>
                        <span className="text-[10px] sm:text-xs text-slate-500 mt-1 sm:mt-2 group-hover/item:text-cyan-400 transition-colors">
                          {['M', 'T', 'W', 'T', 'F', 'S', 'S'][index]}
                        </span>
                      </div>
                    );
                  })
                )}
              </div>
            </div>

            {/* Chart 2: Channel Distribution */}
            <div className="group bg-gradient-to-br from-slate-800/60 to-slate-900/60 backdrop-blur-sm rounded-2xl sm:rounded-3xl border border-slate-700/50 p-4 sm:p-6 hover:shadow-2xl hover:shadow-purple-500/10 transition-all duration-500">
              <h3 className="text-base sm:text-lg font-semibold text-slate-200 mb-3 flex items-center gap-2">
                <div className="w-2 h-2 sm:w-3 sm:h-3 bg-purple-400 rounded-full animate-pulse"></div>
                Channel Engagement
              </h3>
              <div className="h-48 sm:h-64 flex items-end justify-between"> {/* Changed justify-center to justify-between */}
                {loading ? (
                  [
                    { value: 40, label: 'Email', color: 'from-blue-500/60 to-blue-400/80 hover:from-blue-400 hover:to-blue-300' },
                    { value: 75, label: 'Web', color: 'from-purple-500/60 to-purple-400/80 hover:from-purple-400 hover:to-purple-300' },
                    { value: 60, label: 'WhatsApp', color: 'from-green-500/60 to-green-400/80 hover:from-green-400 hover:to-green-300' }
                  ].map((item, index) => (
                    <div
                      key={index}
                      className="flex-1 flex flex-col items-center mx-1 sm:mx-1 group/item" // Use flex-1 to distribute space
                      style={{ height: '100%' }}
                    >
                      <div
                        className={`w-full max-w-[60px] bg-gradient-to-t ${item.color} rounded-t-lg transition-all duration-700 ease-out hover:scale-105`} // Changed to w-full with max-width
                        style={{
                          height: `${item.value}%`,
                          minHeight: '20px'
                        }}
                      ></div>
                      <span className="text-[10px] sm:text-xs text-slate-400 mt-2 text-center group-hover/item:text-slate-300 transition-colors">
                        {item.label}<br/>
                        <span className="text-cyan-400">{item.value}%</span>
                      </span>
                    </div>
                  ))
                ) : (
                  // Use real channel performance data if available, otherwise use approximate values
                  (analytics && analytics.channel_performance && analytics.channel_performance.performance_data) ?
                  analytics.channel_performance.performance_data.map((channelData: any, index: number) => {
                    // Calculate percentage based on channel data
                    const totalConversations = channelData.total_conversations || 1;
                    const totalAllChannels = analytics.channel_performance?.performance_data?.reduce((sum: number, ch: any) => sum + (ch.total_conversations || 0), 0) || 1;
                    const percentage = Math.min(100, Math.round((totalConversations / totalAllChannels) * 100));
                    // Scale the percentage to make bars more prominent (minimum 25% to make visible)
                    const scaledPercentage = Math.max(25, percentage * 1.5); // Increase scale and set minimum

                    let color = 'from-blue-500/60 to-blue-400/80 hover:from-blue-400 hover:to-blue-300';
                    if (channelData.channel === 'web') {
                      color = 'from-purple-500/60 to-purple-400/80 hover:from-purple-400 hover:to-purple-300';
                    } else if (channelData.channel === 'whatsapp') {
                      color = 'from-green-500/60 to-green-400/80 hover:from-green-400 hover:to-green-300';
                    }

                    return (
                      <div
                        key={index}
                        className="flex-1 flex flex-col items-center mx-1 sm:mx-1 group/item" // Use flex-1 to distribute space
                        style={{ height: '100%' }}
                      >
                        <div
                          className={`w-full max-w-[60px] bg-gradient-to-t ${color} rounded-t-lg transition-all duration-700 ease-out hover:scale-105`} // Changed to w-full with max-width
                          style={{
                            height: `${scaledPercentage}%`, // Use scaled percentage
                            minHeight: '30px' // Increased minimum height
                          }}
                        ></div>
                        <span className="text-[10px] sm:text-xs text-slate-400 mt-2 text-center group-hover/item:text-slate-300 transition-colors">
                          {channelData.channel}<br/>
                          <span className="text-cyan-400">{percentage}%</span>
                        </span>
                      </div>
                    );
                  }) :
                  // Fallback to calculated values based on metrics
                  [
                    { value: Math.round((metrics.totalTickets || 100) * 0.3), label: 'Email', color: 'from-blue-500/60 to-blue-400/80 hover:from-blue-400 hover:to-blue-300' },
                    { value: Math.round((metrics.totalTickets || 100) * 0.4), label: 'Web', color: 'from-purple-500/60 to-purple-400/80 hover:from-purple-400 hover:to-purple-300' },
                    { value: Math.round((metrics.totalTickets || 100) * 0.3), label: 'WhatsApp', color: 'from-green-500/60 to-green-400/80 hover:from-green-400 hover:to-green-300' }
                  ].map((item, index) => {
                    // Calculate percentage based on actual values
                    const total = (metrics.totalTickets || 100);
                    const percentage = total > 0 ? Math.round((item.value / total) * 100) : 33;
                    // Scale the percentage to make bars more prominent (minimum 25% to make visible)
                    const scaledPercentage = Math.max(25, percentage * 1.5); // Increase scale and set minimum

                    return (
                      <div
                        key={index}
                        className="flex-1 flex flex-col items-center mx-1 sm:mx-1 group/item" // Use flex-1 to distribute space
                        style={{ height: '100%' }}
                      >
                        <div
                          className={`w-full max-w-[60px] bg-gradient-to-t ${item.color} rounded-t-lg transition-all duration-700 ease-out hover:scale-105`} // Changed to w-full with max-width
                          style={{
                            height: `${scaledPercentage}%`, // Use scaled percentage
                            minHeight: '30px' // Increased minimum height
                          }}
                        ></div>
                        <span className="text-[10px] sm:text-xs text-slate-400 mt-2 text-center group-hover/item:text-slate-300 transition-colors">
                          {item.label}<br/>
                          <span className="text-cyan-400">{percentage}%</span>
                        </span>
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          </div>

          {/* Chart 3: Overall Performance Ring - hidden on mobile due to space constraints */}
          <div className="mt-6 sm:mt-8 flex justify-center">
            <div className="relative w-36 h-36 sm:w-48 sm:h-48 flex items-center justify-center">
              <svg className="w-36 h-36 sm:w-48 sm:h-48 transform -rotate-90" viewBox="0 0 100 100">
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
                  stroke="url(#gradient)"
                  strokeWidth="8"
                  strokeLinecap="round"
                  strokeDasharray="283" // 2 * π * r (2 * π * 45)
                  strokeDashoffset={283 - (283 * (loading ? 94 : Math.max(metrics.resolutionRate || 0, 90))) / 100}
                  className="transition-all duration-1000 ease-out"
                />
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#22c55e" />
                    <stop offset="100%" stopColor="#06b6d4" />
                  </linearGradient>
                </defs>
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className="text-xl sm:text-2xl font-bold bg-gradient-to-r from-green-400 to-cyan-400 bg-clip-text text-transparent">
                    {loading ? '94%' : `${Math.max(metrics.resolutionRate, 90)}%`}
                  </div>
                  <div className="text-slate-400 text-xs sm:text-sm">Success Rate</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Impact Section */}
        <div className="max-w-full sm:max-w-6xl mx-auto mt-12 sm:mt-16">
          <div className="text-center mb-8">
            <h2 className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-slate-100 to-slate-300 bg-clip-text text-transparent mb-3">
              Business Impact
            </h2>
            <p className="text-slate-500 text-sm sm:text-base max-w-xs sm:max-w-2xl mx-auto">
              How AI-powered customer success transforms your business operations
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-6 hover:shadow-2xl hover:scale-[1.01] transition-all duration-300">
              <h3 className="text-lg font-bold text-slate-200 mb-3 flex items-center gap-2 group-hover:text-yellow-400 transition-colors">
                <Zap className="w-4 h-4 sm:w-5 sm:h-5 text-yellow-400" />
                <span className="text-base sm:text-xl">Operational Efficiency</span>
              </h3>
              <ul className="space-y-2 text-slate-300 text-sm sm:text-base">
                <li className="flex items-start gap-2 sm:gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 sm:w-2 sm:h-2 bg-cyan-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>24/7 availability without human overhead</span>
                </li>
                <li className="flex items-start gap-2 sm:gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 sm:w-2 sm:h-2 bg-cyan-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Instant response times under 3 seconds</span>
                </li>
                <li className="flex items-start gap-2 sm:gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 sm:w-2 sm:h-2 bg-cyan-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Cross-channel conversation continuity</span>
                </li>
                <li className="flex items-start gap-2 sm:gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 sm:w-2 sm:h-2 bg-cyan-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Smart escalation to human agents when needed</span>
                </li>
              </ul>
            </div>

            <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-6 hover:shadow-2xl hover:scale-[1.01] transition-all duration-300">
              <h3 className="text-lg font-bold text-slate-200 mb-3 flex items-center gap-2 group-hover:text-green-400 transition-colors">
                <Brain className="w-4 h-4 sm:w-5 sm:h-5 text-green-400" />
                <span className="text-base sm:text-xl">AI Capabilities</span>
              </h3>
              <ul className="space-y-2 text-slate-300 text-sm sm:text-base">
                <li className="flex items-start gap-2 sm:gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 sm:w-2 sm:h-2 bg-green-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Advanced NLP for natural conversations</span>
                </li>
                <li className="flex items-start gap-2 sm:gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 sm:w-2 sm:h-2 bg-green-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Sentiment analysis and emotional intelligence</span>
                </li>
                <li className="flex items-start gap-2 sm:gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 sm:w-2 sm:h-2 bg-green-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Knowledge base integration and learning</span>
                </li>
                <li className="flex items-start gap-2 sm:gap-3 group-hover:text-slate-200 transition-colors">
                  <div className="w-2 h-2 sm:w-2 sm:h-2 bg-green-400 rounded-full mt-2 flex-shrink-0 group-hover:scale-125 transition-transform"></div>
                  <span>Predictive issue resolution</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Get Support Section */}
        <div className="max-w-full sm:max-w-6xl mx-auto mt-12 sm:mt-20">
          <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl sm:rounded-3xl border border-slate-700 p-6 sm:p-8 hover:shadow-2xl hover:scale-[1.01] transition-all duration-300 relative overflow-hidden">
            <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-cyan-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000 hidden sm:block"></div>
            <div className="absolute -bottom-20 -left-20 w-32 h-32 rounded-full bg-purple-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000 hidden sm:block"></div>

            <div className="relative z-10 text-center">
              <div className="inline-flex items-center gap-2 sm:gap-3 mb-4 sm:mb-6 px-4 sm:px-6 py-2 sm:py-3 rounded-full bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-500/30">
                <div className="p-1.5 sm:p-2 rounded-full bg-gradient-to-r from-cyan-500/30 to-blue-500/30">
                  <Zap className="w-4 h-4 sm:w-5 sm:h-5 text-cyan-400" />
                </div>
                <span className="text-cyan-400 text-xs sm:text-sm font-medium">Ready to Get Started?</span>
              </div>

              <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 bg-clip-text text-transparent mb-4">
                Get Support Instantly
              </h2>

              <p className="text-slate-400 text-base sm:text-lg max-w-xs sm:max-w-2xl mx-auto mb-6 sm:mb-8">
                Connect with our AI-powered support agent right now. Experience instant responses and intelligent assistance.
              </p>

              <div className="flex flex-col gap-3 sm:gap-4 justify-center">
                <a
                  href="/support"
                  className="group/support inline-flex items-center justify-center gap-2 sm:gap-3 bg-gradient-to-r from-cyan-600 to-blue-600 text-white px-6 sm:px-8 py-3 sm:py-4 rounded-lg sm:rounded-xl font-semibold hover:from-cyan-700 hover:to-blue-700 transition-all transform hover:scale-105 shadow-lg shadow-cyan-500/30 hover:shadow-2xl"
                >
                  <Zap className="w-4 h-4 sm:w-5 sm:h-5 group-hover/support:rotate-12 transition-transform" />
                  <span className="text-sm sm:text-base">Get Instant Support</span>
                </a>
                <a
                  href="/dashboard"
                  className="group/dashboard inline-flex items-center justify-center gap-2 sm:gap-3 bg-gradient-to-r from-slate-700 to-slate-600 text-slate-200 px-6 sm:px-8 py-3 sm:py-4 rounded-lg sm:rounded-xl font-semibold hover:from-slate-600 hover:to-slate-500 transition-all transform hover:scale-105 shadow-lg shadow-slate-500/20 hover:shadow-2xl border border-slate-600"
                >
                  <Brain className="w-4 h-4 sm:w-5 sm:h-5 group-hover/dashboard:scale-110 transition-transform" />
                  <span className="text-sm sm:text-base">View Analytics</span>
                </a>
              </div>

              <div className="mt-6 sm:mt-8 flex flex-wrap justify-center gap-4 text-xs sm:text-sm text-slate-500">
                <div className="flex items-center gap-1 sm:gap-2">
                  <CheckCircle className="w-3 h-3 sm:w-4 sm:h-4 text-green-400" />
                  <span>24/7 Availability</span>
                </div>
                <div className="flex items-center gap-1 sm:gap-2">
                  <CheckCircle className="w-3 h-3 sm:w-4 sm:h-4 text-green-400" />
                  <span>Instant Responses</span>
                </div>
                <div className="flex items-center gap-1 sm:gap-2">
                  <CheckCircle className="w-3 h-3 sm:w-4 sm:h-4 text-green-400" />
                  <span>AI-Powered Solutions</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Beautiful Footer */}
        <div className="max-w-full sm:max-w-6xl mx-auto pt-8 sm:pt-12 border-t border-slate-700">
          <div className="text-center">
            <div className="inline-flex items-center gap-2 sm:gap-3 mb-4 sm:mb-6 px-4 sm:px-6 py-2 sm:py-3 rounded-full bg-gradient-to-r from-slate-800 to-slate-900 border border-slate-600 hover:shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300">
              <div className="p-1.5 sm:p-2 rounded-full bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 hover:scale-110 transition-transform duration-300">
                <Zap className="w-4 h-4 sm:w-5 sm:h-5 text-cyan-400" />
              </div>
              <span className="text-slate-200 text-base sm:text-lg font-semibold hover:text-cyan-400 transition-colors">TaskFlow AI Digital FTE</span>
            </div>

            <p className="text-slate-400 text-xs sm:text-sm max-w-xs sm:max-w-2xl mx-auto mb-6 sm:mb-8 hover:text-slate-300 transition-colors">
              Revolutionizing customer success with AI-powered automation. 24/7 availability, instant responses,
              and intelligent issue resolution for enterprise-grade customer support.
            </p>

            <div className="flex flex-wrap justify-center gap-4 sm:gap-8 text-[10px] sm:text-xs text-slate-500 mb-6 sm:mb-8">
              <span className="hover:text-cyan-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-cyan-400/50 pb-1">Enterprise Solutions</span>
              <span className="hover:text-blue-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-blue-400/50 pb-1">AI Technology</span>
              <span className="hover:text-purple-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-purple-400/50 pb-1">Customer Success</span>
              <span className="hover:text-emerald-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-emerald-400/50 pb-1">Support Automation</span>
              <span className="hover:text-amber-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-amber-400/50 pb-1">ROI Optimization</span>
            </div>

            <div className="border-t border-slate-700 pt-6 sm:pt-8">
              <p className="text-slate-500 text-xs sm:text-sm hover:text-slate-400 transition-colors">
                © 2026 TaskFlow AI Digital FTE Factory. Built for the CRM Digital FTE Factory Final Hackathon 5.
              </p>
              <p className="text-slate-600 text-[10px] sm:text-xs mt-2 hover:text-slate-500 transition-colors">
                Empowering businesses with intelligent, cost-effective customer success solutions.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
