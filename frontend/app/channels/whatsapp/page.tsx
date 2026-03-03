"use client";

import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api";
import {
  MessageCircle,
  Clock,
  User,
  CheckCircle,
  AlertCircle,
  ArrowLeft,
  MessageSquare,
  Phone
} from "lucide-react";
import Link from "next/link";

// Simple Card component
const Card = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => (
  <div className={`bg-white/5 border border-slate-700 rounded-xl ${className}`}>
    {children}
  </div>
);

const CardHeader = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => (
  <div className={`p-6 border-b border-slate-700 ${className}`}>
    {children}
  </div>
);

const CardContent = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => (
  <div className={`p-6 ${className}`}>
    {children}
  </div>
);

const CardTitle = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => (
  <h3 className={`text-lg font-semibold text-slate-200 ${className}`}>
    {children}
  </h3>
);

// Simple Badge component
const Badge = ({ children, variant = "default", className = "" }: { children: React.ReactNode; variant?: "default" | "destructive"; className?: string }) => {
  const baseClasses = "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium";

  const variantClasses = variant === "destructive"
    ? "bg-red-500/20 text-red-400 border border-red-500/30"
    : "bg-blue-500/20 text-blue-400 border border-blue-500/30";

  return (
    <span className={`${baseClasses} ${variantClasses} ${className}`}>
      {children}
    </span>
  );
};

export default function WhatsAppChannelPage() {
  const [recentTickets, setRecentTickets] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRecentTickets = async () => {
      try {
        setLoading(true);
        const response = await apiClient.getBalancedActivity();
        const activities: any[] = response.data.activities || [];
        const whatsappTickets = activities.filter((ticket: any) => ticket.channel === 'whatsapp');
        setRecentTickets(whatsappTickets.slice(0, 5));
        setLoading(false);
      } catch (err) {
        setError("Failed to load recent activity");
        setLoading(false);
        console.error("Error fetching tickets:", err);
      }
    };

    fetchRecentTickets();
  }, []);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 py-12 px-4 sm:px-6 lg:px-8">
      {/* Animated background elements */}
      <div className="absolute top-20 left-20 w-72 h-72 bg-green-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-20 right-20 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      <div className="absolute top-1/2 right-1/4 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl animate-pulse delay-500"></div>

      <div className="relative z-10 max-w-6xl mx-auto">
        <div className="mb-8">
          <Link href="/" className="inline-flex items-center gap-2 text-slate-400 hover:text-slate-300 transition-colors">
            <ArrowLeft className="w-4 h-4" />
            Back to Dashboard
          </Link>
        </div>

        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-3 mb-6 px-6 py-3 rounded-full bg-gradient-to-r from-green-500/20 to-teal-500/20 border border-green-500/30 backdrop-blur-sm">
            <div className="p-2 rounded-full bg-green-500/30">
              <MessageSquare className="w-5 h-5 text-green-400" />
            </div>
            <span className="text-green-400 text-sm font-medium">WhatsApp Integration</span>
          </div>

          <h1 className="text-5xl font-bold bg-gradient-to-r from-green-400 via-teal-500 to-emerald-500 bg-clip-text text-transparent mb-6">
            WhatsApp Channel
          </h1>

          <p className="text-xl text-slate-400 max-w-3xl mx-auto leading-relaxed">
            Real-time messaging with AI-powered responses
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Instructions Card */}
          <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 hover:shadow-2xl hover:scale-[1.01] transition-all duration-300 relative overflow-hidden">
            <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-green-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
            <div className="absolute -bottom-20 -left-20 w-32 h-32 rounded-full bg-teal-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>

            <CardHeader>
              <CardTitle className="flex items-center gap-3 text-slate-200">
                <div className="p-2 rounded-full bg-green-500/20 border border-green-500/30">
                  <MessageCircle className="w-5 h-5 text-green-400" />
                </div>
                <span>How to Test WhatsApp Channel</span>
              </CardTitle>
            </CardHeader>

            <CardContent className="space-y-4 relative z-10">
              <div className="p-4 bg-slate-700/50 rounded-xl border border-slate-600">
                <h3 className="font-semibold text-slate-300 mb-2 flex items-center gap-2">
                  <Phone className="w-4 h-4 text-emerald-400" />
                  Send a WhatsApp Message
                </h3>
                <p className="text-slate-400 text-sm">
                  Send a WhatsApp message to: <span className="font-mono bg-slate-800 px-2 py-1 rounded text-emerald-400">+1 415 523 8886</span>
                </p>
                <p className="text-slate-500 text-xs mt-2">
                  (Twilio WhatsApp Sandbox number - configure TWILIO_WHATSAPP_NUMBER in production)
                </p>
              </div>

              <div className="p-4 bg-slate-700/50 rounded-xl border border-slate-600">
                <h3 className="font-semibold text-slate-300 mb-2 flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  Automatic Processing
                </h3>
                <p className="text-slate-400 text-sm">
                  Our AI will automatically:
                </p>
                <ul className="text-slate-400 text-sm mt-2 space-y-1 ml-4">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-3 h-3 text-green-400 mt-0.5 flex-shrink-0" />
                    Create a ticket with channel="whatsapp"
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-3 h-3 text-green-400 mt-0.5 flex-shrink-0" />
                    Process with AI agent
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-3 h-3 text-green-400 mt-0.5 flex-shrink-0" />
                    Reply via Twilio API
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-3 h-3 text-green-400 mt-0.5 flex-shrink-0" />
                    Mark conversation as resolved
                  </li>
                </ul>
              </div>

              <div className="p-4 bg-slate-700/50 rounded-xl border border-slate-600">
                <h3 className="font-semibold text-slate-300 mb-2 flex items-center gap-2">
                  <AlertCircle className="w-4 h-4 text-amber-400" />
                  Note
                </h3>
                <p className="text-slate-400 text-sm">
                  This channel uses inbound webhook - no manual form submission required.
                  Customers send messages directly via WhatsApp app.
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Recent Activity Card */}
          <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 hover:shadow-2xl hover:scale-[1.01] transition-all duration-300 relative overflow-hidden">
            <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-teal-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
            <div className="absolute -bottom-20 -left-20 w-32 h-32 rounded-full bg-green-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>

            <CardHeader>
              <CardTitle className="flex items-center gap-3 text-slate-200">
                <div className="p-2 rounded-full bg-teal-500/20 border border-teal-500/30">
                  <Clock className="w-5 h-5 text-teal-400" />
                </div>
                <span>Recent WhatsApp Activity</span>
              </CardTitle>
            </CardHeader>

            <CardContent className="space-y-4 relative z-10">
              {loading ? (
                <div className="flex items-center justify-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-500"></div>
                </div>
              ) : error ? (
                <div className="text-center py-8 text-slate-400">
                  <AlertCircle className="w-12 h-12 mx-auto mb-4 text-red-400" />
                  <p>Failed to load recent activity</p>
                </div>
              ) : recentTickets.length === 0 ? (
                <div className="text-center py-8 text-slate-400">
                  <MessageSquare className="w-12 h-12 mx-auto mb-4 text-slate-600" />
                  <p>No recent WhatsApp activity</p>
                  <p className="text-sm mt-2">Send a message to test the integration!</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {recentTickets.map((ticket: any) => (
                    <div key={ticket.id} className="p-4 bg-slate-700/30 rounded-lg border border-slate-600">
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="font-medium text-slate-200 truncate max-w-[200px]">
                          {ticket.message || 'No Subject'}
                        </h4>
                        <Badge
                          variant={ticket.status === 'resolved' ? 'default' : 'destructive'}
                          className="text-xs"
                        >
                          {ticket.status}
                        </Badge>
                      </div>
                      <div className="flex items-center gap-4 text-xs text-slate-400">
                        <div className="flex items-center gap-1">
                          <User className="w-3 h-3" />
                          {ticket.customer?.split('@')[0] || ticket.customer}
                        </div>
                        <div className="flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {ticket.time}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="mt-12 text-center mb-12">
          <div className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-gradient-to-r from-green-500/20 to-teal-500/20 border border-green-500/30 backdrop-blur-sm">
            <CheckCircle className="w-4 h-4 text-green-400" />
            <span className="text-slate-300 text-sm">
              Real-time WhatsApp messaging with AI-powered responses
            </span>
          </div>
        </div>

        {/* Beautiful Footer */}
        <div className="max-w-6xl mx-auto pt-12 border-t border-slate-700">
          <div className="text-center">
            <div className="inline-flex items-center gap-3 mb-6 px-6 py-3 rounded-full bg-gradient-to-r from-slate-800 to-slate-900 border border-slate-600 hover:shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300">
              <div className="p-2 rounded-full bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 hover:scale-110 transition-transform duration-300">
                <MessageSquare className="w-5 h-5 text-cyan-400" />
              </div>
              <span className="text-slate-200 text-lg font-semibold hover:text-cyan-400 transition-colors">WhatsApp Integration</span>
            </div>

            <p className="text-slate-400 text-sm max-w-2xl mx-auto mb-8 hover:text-slate-300 transition-colors">
              Instant messaging support through WhatsApp. Real-time responses with intelligent AI assistance.
            </p>

            <div className="flex flex-wrap justify-center gap-8 text-xs text-slate-500 mb-8">
              <span className="hover:text-cyan-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-cyan-400/50 pb-1">WhatsApp API</span>
              <span className="hover:text-blue-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-blue-400/50 pb-1">Twilio Integration</span>
              <span className="hover:text-purple-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-purple-400/50 pb-1">Real-time Responses</span>
              <span className="hover:text-emerald-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-emerald-400/50 pb-1">Webhook Processing</span>
              <span className="hover:text-amber-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-amber-400/50 pb-1">AI Automation</span>
            </div>

            <div className="border-t border-slate-700 pt-8">
              <p className="text-slate-500 text-sm hover:text-slate-400 transition-colors">
                © 2026 TaskFlow AI WhatsApp Integration. Built for the CRM Digital FTE Factory Final Hackathon 5.
              </p>
              <p className="text-slate-600 text-xs mt-2 hover:text-slate-500 transition-colors">
                Connecting customers through their preferred messaging platform.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}