"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api";
import { Loader2, CheckCircle, XCircle } from "lucide-react";

export default function SupportPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
    priority: "medium",
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [showAIResponse, setShowAIResponse] = useState(false);
  const [error, setError] = useState("");
  const [ticketId, setTicketId] = useState("");
  const [aiResponse, setAIResponse] = useState("");
  const [responseStatus, setResponseStatus] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess(false);
    setShowAIResponse(false);

    try {
      const response = await apiClient.submitTicket(formData);

      // Handle the AI response from the API
      if (response.data.response) {
        setAIResponse(response.data.response);
        setResponseStatus(response.data.status);
        setShowAIResponse(true);
      }

      setTicketId(response.data.ticket_id);
      setSuccess(true);

      // Reset form
      setFormData({
        name: "",
        email: "",
        subject: "",
        message: "",
        priority: "medium",
      });
    } catch (err: any) {
      setError(
        err.response?.data?.detail || "Failed to submit ticket. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative">
      {/* Animated background elements */}
      <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-20 right-20 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      <div className="absolute top-1/2 right-1/4 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl animate-pulse delay-500"></div>

      <div className="relative z-10 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">
          {/* Header Section */}
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-3 mb-6 px-6 py-3 rounded-full bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-blue-500/30 backdrop-blur-sm">
              <div className="p-2 rounded-full bg-blue-500/30">
                <CheckCircle className="w-5 h-5 text-blue-400" />
              </div>
              <span className="text-blue-400 text-sm font-medium">AI-Powered Customer Support</span>
            </div>

            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent mb-6">
              Get Support Now
            </h1>

            <p className="text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
              Connect with our AI-powered support team. We typically respond in under 3 seconds!
            </p>
          </div>

          {/* Form Card */}
          <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-3xl border border-slate-700 p-8 hover:shadow-2xl hover:scale-[1.01] transition-all duration-300 relative overflow-hidden">
            <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-blue-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
            <div className="absolute -bottom-20 -left-20 w-32 h-32 rounded-full bg-purple-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>

            <div className="relative z-10">
              {success ? (
              <div className="py-6">
                {/* Ticket Confirmation */}
                <div className="text-center mb-8">
                  <div className="relative p-6 rounded-full bg-gradient-to-r from-green-500/20 to-emerald-500/20 border-2 border-green-500/30 mx-auto w-24 h-24 flex items-center justify-center mb-6">
                    <div className="absolute inset-0 rounded-full bg-gradient-to-r from-green-500/10 to-emerald-500/10 animate-pulse"></div>
                    <CheckCircle className="w-12 h-12 text-green-400 relative z-10" />
                  </div>

                  <h2 className="text-3xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent mb-4">
                    Request Submitted Successfully!
                  </h2>

                  <p className="text-slate-300 mb-6 max-w-md mx-auto">Great! Your request has been received and is being processed by our AI assistant.</p>

                  <div className="mb-6 p-4 bg-slate-800/50 rounded-xl border border-slate-700 inline-block">
                    <p className="text-slate-400 mb-2">Ticket ID</p>
                    <div className="flex items-center gap-2 justify-center">
                      <span className="font-mono text-lg font-bold bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-transparent">
                        {ticketId}
                      </span>
                      <button
                        onClick={() => navigator.clipboard.writeText(ticketId)}
                        className="text-slate-500 hover:text-slate-300 transition-colors text-sm"
                        title="Copy ticket ID"
                      >
                        Copy
                      </button>
                    </div>
                  </div>

                  <div className="bg-slate-800/30 rounded-xl p-4 mb-6 inline-block">
                    <div className="flex items-center gap-2 text-green-400 text-sm">
                      <CheckCircle className="w-4 h-4" />
                      <span>AI Response Generated</span>
                    </div>
                  </div>
                </div>

                {/* AI Response Section */}
                {showAIResponse && aiResponse && (
                  <div className="mb-8">
                    <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-600 p-6 relative overflow-hidden">
                      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-transparent to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300"></div>
                      <div className="relative z-10">
                        <div className="flex items-center gap-3 mb-4">
                          <div className="p-2 rounded-full bg-gradient-to-r from-blue-500/30 to-purple-500/30">
                            <CheckCircle className="w-5 h-5 text-blue-400" />
                          </div>
                          <h3 className="text-xl font-bold text-slate-200">
                            AI Response
                            <span className={`ml-2 px-2 py-1 rounded-full text-xs font-medium ${
                              responseStatus === 'resolved'
                                ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                                : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                            }`}>
                              {responseStatus === 'resolved' ? 'Resolved' : 'Escalated'}
                            </span>
                          </h3>
                        </div>

                        <div className="prose prose-invert max-w-none">
                          <div className="text-slate-300 leading-relaxed whitespace-pre-wrap bg-slate-900/30 rounded-lg p-4 border border-slate-700/50">
                            {aiResponse}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                <p className="text-slate-400 mb-8 text-lg max-w-lg mx-auto text-center">
                  {showAIResponse
                    ? "An immediate response has been provided above. A copy has been sent to your email."
                    : "We're processing your request and will respond shortly."
                  }
                  <br />
                  <span className="font-semibold text-amber-400">
                    Estimated response time: {showAIResponse ? "Response provided above" : "3 seconds"}
                  </span>
                </p>

                <div className="flex gap-4 justify-center">
                  <button
                    onClick={() => {
                      setSuccess(false);
                      setTicketId("");
                      setShowAIResponse(false);
                      setAIResponse("");
                      setResponseStatus("");
                    }}
                    className="bg-gradient-to-r from-slate-700 to-slate-600 text-slate-200 px-6 py-3 rounded-full font-semibold hover:from-slate-600 hover:to-slate-500 transition-all shadow-lg shadow-slate-500/20"
                  >
                    Submit Another Request
                  </button>
                </div>
              </div>
            ) : (
                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Name Field */}
                  <div className="group/field">
                    <label
                      htmlFor="name"
                      className="block text-sm font-medium text-slate-300 mb-3 flex items-center gap-2"
                    >
                      <div className="p-1.5 rounded-full bg-slate-700 group-focus-within/field:bg-blue-500/30 transition-colors">
                        <CheckCircle className="w-3 h-3 text-blue-400 group-focus-within/field:text-blue-300 transition-colors" />
                      </div>
                      Your Name *
                    </label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      required
                      value={formData.name}
                      onChange={handleChange}
                      className="w-full px-4 py-4 bg-slate-900/50 border border-slate-700 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-slate-100 placeholder-slate-500 backdrop-blur-sm group-hover:border-blue-500/50 focus:bg-slate-900/70"
                      placeholder="Enter your full name"
                      aria-describedby="name-help"
                    />
                    <p id="name-help" className="mt-2 text-xs text-slate-500">Enter your full name for personalized support</p>
                  </div>

                  {/* Email Field */}
                  <div className="group/field">
                    <label
                      htmlFor="email"
                      className="block text-sm font-medium text-slate-300 mb-3 flex items-center gap-2"
                    >
                      <div className="p-1.5 rounded-full bg-slate-700 group-focus-within/field:bg-amber-500/30 transition-colors">
                        <CheckCircle className="w-3 h-3 text-amber-400 group-focus-within/field:text-amber-300 transition-colors" />
                      </div>
                      Email Address *
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      required
                      value={formData.email}
                      onChange={handleChange}
                      className="w-full px-4 py-4 bg-slate-900/50 border border-slate-700 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent transition-all text-slate-100 placeholder-slate-500 backdrop-blur-sm group-hover:border-amber-500/50 focus:bg-slate-900/70"
                      placeholder="your.email@example.com"
                      aria-describedby="email-help"
                    />
                    <p id="email-help" className="mt-2 text-xs text-slate-500">We'll send a confirmation and response to this email</p>
                  </div>

                  {/* Subject Field */}
                  <div className="group/field">
                    <label
                      htmlFor="subject"
                      className="block text-sm font-medium text-slate-300 mb-3 flex items-center gap-2"
                    >
                      <div className="p-1.5 rounded-full bg-slate-700 group-focus-within/field:bg-green-500/30 transition-colors">
                        <CheckCircle className="w-3 h-3 text-green-400 group-focus-within/field:text-green-300 transition-colors" />
                      </div>
                      Subject *
                    </label>
                    <input
                      type="text"
                      id="subject"
                      name="subject"
                      required
                      value={formData.subject}
                      onChange={handleChange}
                      className="w-full px-4 py-4 bg-slate-900/50 border border-slate-700 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all text-slate-100 placeholder-slate-500 backdrop-blur-sm group-hover:border-green-500/50 focus:bg-slate-900/70"
                      placeholder="Brief description of your issue"
                      aria-describedby="subject-help"
                    />
                    <p id="subject-help" className="mt-2 text-xs text-slate-500">A clear subject helps us categorize and respond faster</p>
                  </div>

                  {/* Message Field */}
                  <div className="group/field">
                    <label
                      htmlFor="message"
                      className="block text-sm font-medium text-slate-300 mb-3 flex items-center gap-2"
                    >
                      <div className="p-1.5 rounded-full bg-slate-700 group-focus-within/field:bg-cyan-500/30 transition-colors">
                        <CheckCircle className="w-3 h-3 text-cyan-400 group-focus-within/field:text-cyan-300 transition-colors" />
                      </div>
                      Message *
                    </label>
                    <textarea
                      id="message"
                      name="message"
                      required
                      rows={6}
                      value={formData.message}
                      onChange={handleChange}
                      className="w-full px-4 py-4 bg-slate-900/50 border border-slate-700 rounded-xl focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all resize-none text-slate-100 placeholder-slate-500 backdrop-blur-sm group-hover:border-cyan-500/50 focus:bg-slate-900/70"
                      placeholder="Please describe your issue in detail..."
                      aria-describedby="message-help"
                    />
                    <p id="message-help" className="mt-2 text-xs text-slate-500">Include any relevant details, steps to reproduce, or error messages</p>
                  </div>

                  {/* Priority Field */}
                  <div className="group/field">
                    <label
                      htmlFor="priority"
                      className="block text-sm font-medium text-slate-300 mb-3 flex items-center gap-2"
                    >
                      <div className="p-1.5 rounded-full bg-slate-700 group-focus-within/field:bg-purple-500/30 transition-colors">
                        <CheckCircle className="w-3 h-3 text-purple-400 group-focus-within/field:text-purple-300 transition-colors" />
                      </div>
                      Priority Level
                    </label>
                    <select
                      id="priority"
                      name="priority"
                      value={formData.priority}
                      onChange={handleChange}
                      className="w-full px-4 py-4 bg-slate-900/50 border border-slate-700 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-slate-100 backdrop-blur-sm group-hover:border-purple-500/50 focus:bg-slate-900/70"
                      aria-describedby="priority-help"
                    >
                      <option value="low" className="bg-slate-800 text-slate-300">Low - Standard Response</option>
                      <option value="medium" className="bg-slate-800 text-slate-300">Medium - Within 1 Hour</option>
                      <option value="high" className="bg-slate-800 text-slate-300">High - Within 15 Minutes</option>
                      <option value="urgent" className="bg-slate-800 text-slate-300">Urgent - Within 5 Minutes</option>
                    </select>
                    <p id="priority-help" className="mt-2 text-xs text-slate-500">Choose priority based on the impact of your issue</p>
                  </div>

                  {error && (
                    <div className="flex items-center gap-3 p-4 bg-gradient-to-r from-red-500/20 to-rose-500/20 border border-red-500/30 rounded-xl backdrop-blur-sm">
                      <div className="p-2 rounded-full bg-red-500/30">
                        <XCircle className="w-5 h-5 text-red-400" />
                      </div>
                      <p className="text-red-300 text-sm">{error}</p>
                    </div>
                  )}

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-cyan-600 to-blue-600 text-white py-4 px-6 rounded-xl font-semibold hover:from-cyan-700 hover:to-blue-700 transition-all transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-3 shadow-lg shadow-cyan-500/30 backdrop-blur-sm group/btn"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        Processing Your Request...
                      </>
                    ) : (
                      <>
                        <span className="group-hover/btn:animate-pulse">
                          <CheckCircle className="w-5 h-5" />
                        </span>
                        Submit Support Request
                      </>
                    )}
                  </button>
                </form>
              )}

              {/* Beautiful Footer */}
              <div className="mt-20 pt-12 border-t border-slate-700">
                <div className="text-center">
                  <div className="inline-flex items-center gap-3 mb-6 px-6 py-3 rounded-full bg-gradient-to-r from-slate-800 to-slate-900 border border-slate-600 hover:shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300">
                    <div className="p-2 rounded-full bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 hover:scale-110 transition-transform duration-300">
                      <CheckCircle className="w-5 h-5 text-cyan-400" />
                    </div>
                    <span className="text-slate-200 text-lg font-semibold hover:text-cyan-400 transition-colors">AI-Powered Customer Support</span>
                  </div>

                  <p className="text-slate-400 text-sm max-w-2xl mx-auto mb-8 hover:text-slate-300 transition-colors">
                    Instant help with intelligent AI agents. Available 24/7 for immediate assistance.
                  </p>

                  <div className="flex flex-wrap justify-center gap-8 text-xs text-slate-500 mb-8">
                    <span className="hover:text-cyan-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-cyan-400/50 pb-1">Instant Support</span>
                    <span className="hover:text-blue-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-blue-400/50 pb-1">AI Agent</span>
                    <span className="hover:text-purple-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-purple-400/50 pb-1">24/7 Availability</span>
                    <span className="hover:text-emerald-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-emerald-400/50 pb-1">Secure Platform</span>
                    <span className="hover:text-amber-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-amber-400/50 pb-1">Fast Resolution</span>
                  </div>

                  <div className="border-t border-slate-700 pt-8">
                    <p className="text-slate-500 text-sm hover:text-slate-400 transition-colors">
                      © 2026 TaskFlow AI Customer Support. Built for the CRM Digital FTE Factory Final Hackathon 5.
                    </p>
                    <p className="text-slate-600 text-xs mt-2 hover:text-slate-500 transition-colors">
                      Instant AI-powered assistance for all your needs.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
