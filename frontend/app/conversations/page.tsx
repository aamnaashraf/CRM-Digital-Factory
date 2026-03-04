"use client";

import { useState, useEffect } from "react";
import { MessageCircle, User, Clock, Search, Filter, ChevronDown, Send } from "lucide-react";
import { apiClient } from "@/lib/api";

interface ConversationMessage {
  sender: 'customer' | 'agent';
  content: string;
  timestamp: string;
}

interface ActivityItem {
  id: string;
  customer: string;
  message: string;
  channel: string;
  time: string;
  sentiment: number;
  status: 'open' | 'resolved' | 'escalated';
}

interface ConversationDetail {
  ticket_id: string;
  status: 'open' | 'resolved' | 'escalated';
  subject?: string;
  created_at: string;
  updated_at: string;
  escalated: boolean;
  message_count: number;
  messages: ConversationMessage[];
  customer?: string;
  customer_email?: string;
}

interface Conversation {
  id: string;
  customer: string;
  customerEmail: string;
  channel: string;
  status: 'open' | 'resolved' | 'escalated';
  sentiment: number;
  lastUpdated: string;
  messages: ConversationMessage[];
  subject?: string;
  createdAt?: string;
  messageCount?: number;
  messagePreview: string;
}

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const response = await apiClient.getConversations();
        const activities = response.data.activities || [];

        // Convert activity items to conversation objects, filtering out system messages but keeping legitimate interactions
        const filteredActivities = activities.filter((activity: ActivityItem) => {
          // Filter out email bounce notifications and other system messages
          if (activity.channel === "email") {
            // Keep real customer emails, filter out system notifications
            return activity.customer !== "Mail Delivery Subsystem" &&
                   activity.customer !== "ChatGPT" &&
                   !activity.customer.includes("noreply") &&
                   !activity.customer.includes("no-reply") &&
                   !activity.customer.includes("notifications") &&
                   !activity.customer.includes("system");
          }

          // For non-email channels (web, whatsapp, etc.), keep all activities
          return true;
        });

        const conversations = filteredActivities.map((activity: ActivityItem) => ({
          id: activity.id,
          customer: activity.customer,
          customerEmail: activity.customer, // Using customer name as email for now since activity doesn't include email
          channel: activity.channel,
          status: activity.status,
          sentiment: activity.sentiment,
          lastUpdated: activity.time,
          messages: [],
          messagePreview: activity.message.substring(0, 60) + (activity.message.length > 60 ? '...' : ''), // Preview of first message
          messageCount: 0, // Will be updated when detailed view is loaded
        }));

        setConversations(conversations);
        if (conversations.length > 0) {
          setSelectedConversation(conversations[0]);
        }
      } catch (error) {
        console.error("Failed to fetch conversations:", error);
        setConversations([]);
      } finally {
        setLoading(false);
      }
    };

    fetchConversations();
  }, []);

  // Fetch detailed messages when a conversation is selected
  useEffect(() => {
    const fetchConversationDetail = async () => {
      if (selectedConversation && selectedConversation.messages.length === 0) { // Only fetch if not already loaded
        setLoadingDetail(true);
        try {
          const response = await apiClient.getConversation(selectedConversation.id);
          const ticketDetail: ConversationDetail = response.data;

          // Map the ticket detail to our conversation format
          // Filter out consecutive duplicate messages if needed
          let filteredMessages = ticketDetail.messages || [];

          // Remove consecutive duplicate messages
          filteredMessages = filteredMessages.filter((msg, index) => {
            if (index === 0) return true;
            const prevMsg = filteredMessages[index - 1];
            return !(msg.sender === prevMsg.sender && msg.content.trim() === prevMsg.content.trim());
          });

          const updatedConversation = {
            ...selectedConversation,
            customer: ticketDetail.customer || selectedConversation.customer,
            customerEmail: ticketDetail.customer_email || selectedConversation.customerEmail,
            messages: filteredMessages,
            subject: ticketDetail.subject,
            createdAt: ticketDetail.created_at,
            status: ticketDetail.status,
            messageCount: filteredMessages.length, // Update the count based on filtered messages
            messagePreview: filteredMessages && filteredMessages.length > 0
              ? filteredMessages[0]?.content.substring(0, 60) + (filteredMessages[0]?.content.length > 60 ? '...' : '')
              : 'No messages yet'
          };

          // Update the conversations list with the detailed conversation
          const updatedConversations = conversations.map(conv =>
            conv.id === selectedConversation.id ? updatedConversation : conv
          );
          setConversations(updatedConversations);
          setSelectedConversation(updatedConversation);
        } catch (error) {
          console.error("Failed to fetch conversation details:", error);
          // Still update the state to show the selected conversation with empty messages
          setSelectedConversation({
            ...selectedConversation,
            messages: [],
            messagePreview: 'Error loading messages'
          });
        } finally {
          setLoadingDetail(false);
        }
      }
    };

    if (selectedConversation) {
      fetchConversationDetail();
    }
  }, [selectedConversation?.id]);

  const filteredConversations = conversations.filter(conv => {
    const matchesSearch = conv.customer.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         conv.customerEmail.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filter === 'all' || conv.status === filter;
    return matchesSearch && matchesFilter;
  });

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'resolved': return 'text-green-400 bg-green-500/20';
      case 'open': return 'text-blue-400 bg-blue-500/20';
      case 'escalated': return 'text-orange-400 bg-orange-500/20';
      default: return 'text-slate-400 bg-slate-600/20';
    }
  };

  const getSentimentColor = (sentiment: number) => {
    if (sentiment >= 0.5) return 'text-green-400';
    if (sentiment >= 0) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative">
      {/* Animated background */}
      <div className="absolute top-20 left-10 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl animate-pulse delay-1000"></div>

      <div className="relative z-10 p-4 sm:p-6 md:p-8">
        {/* Header */}
        <div className="mb-6 sm:mb-8 text-center">
          <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 bg-clip-text text-transparent mb-3 sm:mb-4 px-4">
            Customer Conversations
          </h1>
          <p className="text-sm sm:text-base text-slate-400 max-w-2xl mx-auto px-4">
            View complete conversation history between customers and AI support agents
          </p>
        </div>

        <div className="flex flex-col lg:flex-row gap-4 sm:gap-6">
          {/* Conversation List Sidebar */}
          <div className="lg:w-1/3">
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl sm:rounded-2xl border border-slate-700 p-4 sm:p-5 md:p-6">
              {/* Search and Filter */}
              <div className="mb-4 sm:mb-6">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-500" />
                  <input
                    type="text"
                    placeholder="Search customers..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 text-sm sm:text-base bg-slate-800/50 border border-slate-600 rounded-lg text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50"
                  />
                </div>
              </div>

              <div className="mb-4 sm:mb-6 flex flex-wrap gap-2">
                {['all', 'open', 'resolved', 'escalated'].map((status) => (
                  <button
                    key={status}
                    onClick={() => setFilter(status)}
                    className={`flex-1 min-w-[70px] px-2 sm:px-3 py-1.5 sm:py-2 rounded-lg text-xs sm:text-sm font-medium transition-all whitespace-nowrap ${
                      filter === status
                        ? status === 'resolved' ? 'bg-green-500/20 border border-green-500/50 text-green-400' :
                          status === 'open' ? 'bg-blue-500/20 border border-blue-500/50 text-blue-400' :
                          status === 'escalated' ? 'bg-orange-500/20 border border-orange-500/50 text-orange-400' :
                          'bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-blue-500/50 text-blue-400'
                        : 'bg-slate-800/50 border border-slate-600 text-slate-400 hover:border-slate-500'
                    }`}
                  >
                    {status.charAt(0).toUpperCase() + status.slice(1)}
                  </button>
                ))}
              </div>

              {/* Conversation List */}
              <div className="space-y-2 sm:space-y-3 max-h-[calc(100vh-250px)] overflow-y-auto">
                {loading ? (
                  <div className="space-y-3">
                    {[1, 2, 3].map((i) => (
                      <div key={i} className="animate-pulse flex items-center gap-3 p-3 rounded-xl bg-slate-800/50">
                        <div className="w-10 h-10 bg-slate-700 rounded-full"></div>
                        <div className="flex-1 space-y-2">
                          <div className="h-4 bg-slate-700 rounded w-3/4"></div>
                          <div className="h-3 bg-slate-700 rounded w-1/2"></div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : filteredConversations.length === 0 ? (
                  <div className="text-center py-8">
                    <MessageCircle className="w-12 h-12 text-slate-600 mx-auto mb-4" />
                    {conversations.length > 0 ? (
                      <>
                        <p className="text-slate-500">No conversations match current filters</p>
                        <p className="text-xs text-slate-600 mt-2">Try changing your search or filter criteria</p>
                      </>
                    ) : (
                      <>
                        <p className="text-slate-500">No conversations found</p>
                        <p className="text-xs text-slate-600 mt-2">Customer interactions will appear here as they occur</p>
                      </>
                    )}
                  </div>
                ) : (
                  filteredConversations.map((conversation) => (
                    <div
                      key={conversation.id}
                      onClick={() => setSelectedConversation(conversation)}
                      className={`p-3 sm:p-4 rounded-xl border cursor-pointer transition-all ${
                        selectedConversation?.id === conversation.id
                          ? 'bg-slate-700/50 border-cyan-500/50 shadow-lg shadow-cyan-500/10'
                          : 'bg-slate-800/50 border-slate-700 hover:border-slate-600'
                      }`}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center gap-2 min-w-0 flex-1">
                          <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-gradient-to-r from-cyan-500/20 to-blue-500/20 flex items-center justify-center flex-shrink-0">
                            <User className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-cyan-400" />
                          </div>
                          <div className="min-w-0 flex-1">
                            <p className="font-semibold text-slate-200 text-xs sm:text-sm truncate">{conversation.customer}</p>
                            <p className="text-xs text-slate-500 truncate">{conversation.customerEmail}</p>
                          </div>
                        </div>
                        <span className={`text-xs px-2 py-1 rounded-full flex-shrink-0 ml-2 ${getStatusColor(conversation.status)}`}>
                          {conversation.status}
                        </span>
                      </div>
                      <p className="text-xs text-slate-400 mb-2 line-clamp-1">
                        {conversation.messagePreview}
                      </p>
                      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 sm:gap-2">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className={`text-xs capitalize ${getSentimentColor(conversation.sentiment)}`}>
                            {conversation.sentiment >= 0.5 ? 'Positive' : conversation.sentiment >= 0 ? 'Neutral' : 'Negative'}
                          </span>
                          <span className="text-xs text-slate-500 capitalize">{conversation.channel}</span>
                        </div>
                        <span className="text-xs text-slate-500">{formatDate(conversation.lastUpdated)}</span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Conversation Detail */}
          <div className="lg:w-2/3">
            {selectedConversation ? (
              <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl sm:rounded-2xl border border-slate-700 h-[calc(100vh-120px)] flex flex-col">
                {/* Conversation Header */}
                <div className="p-4 sm:p-5 md:p-6 border-b border-slate-700">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-0">
                    <div className="min-w-0">
                      <h2 className="text-lg sm:text-xl font-bold text-slate-200 truncate">{selectedConversation.customer}</h2>
                      <p className="text-sm text-slate-500 truncate">{selectedConversation.customerEmail}</p>
                    </div>
                    <div className="flex items-center gap-2 sm:gap-3 flex-shrink-0">
                      <span className={`px-2 sm:px-3 py-1 rounded-full text-xs font-medium capitalize ${getStatusColor(selectedConversation.status)}`}>
                        {selectedConversation.status}
                      </span>
                      <span className="text-xs sm:text-sm text-slate-500 capitalize">{selectedConversation.channel}</span>
                    </div>
                  </div>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-3 sm:p-4 md:p-6 space-y-3 sm:space-y-4">
                  {loadingDetail ? (
                    <div className="flex justify-center items-center h-full">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-500"></div>
                    </div>
                  ) : selectedConversation.messages.length === 0 ? (
                    <div className="text-center py-8">
                      <MessageCircle className="w-12 h-12 text-slate-600 mx-auto mb-4" />
                      <p className="text-slate-500">No messages in this conversation</p>
                    </div>
                  ) : (
                    selectedConversation.messages.map((message, index) => (
                      <div
                        key={`${selectedConversation.id}-${index}`}
                        className={`flex ${message.sender === 'customer' ? 'justify-start' : 'justify-end'}`}
                      >
                        <div
                          className={`max-w-[85%] sm:max-w-xs lg:max-w-md px-3 sm:px-4 py-2 sm:py-3 rounded-2xl ${
                            message.sender === 'customer'
                              ? 'bg-slate-700/50 border border-slate-600 rounded-tl-none text-slate-200'
                              : 'bg-gradient-to-r from-cyan-600/20 to-blue-600/20 border border-cyan-500/30 rounded-tr-none text-slate-200'
                          }`}
                        >
                          <p className="text-xs sm:text-sm whitespace-pre-wrap break-words">{message.content}</p>
                          <p className="text-xs mt-1 opacity-70">
                            {formatDate(message.timestamp)}
                          </p>
                        </div>
                      </div>
                    ))
                  )}
                </div>

                {/* Reply Input - Disabled for demo since this is read-only view */}
                <div className="p-3 sm:p-4 border-t border-slate-700 bg-slate-800/30">
                  <div className="flex items-center gap-2">
                    <input
                      type="text"
                      placeholder="Reply to customer (Demo mode - read only)"
                      disabled
                      className="flex-1 px-3 sm:px-4 py-2 text-sm sm:text-base bg-slate-800/50 border border-slate-600 rounded-lg text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50"
                    />
                    <button
                      disabled
                      className="p-2 rounded-lg bg-slate-700 text-slate-500 cursor-not-allowed flex-shrink-0"
                    >
                      <Send className="w-4 h-4 sm:w-5 sm:h-5" />
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl sm:rounded-2xl border border-slate-700 h-[calc(100vh-120px)] flex items-center justify-center p-4">
                <div className="text-center">
                  <MessageCircle className="w-12 h-12 sm:w-16 sm:h-16 text-slate-600 mx-auto mb-4" />
                  <h3 className="text-lg sm:text-xl font-semibold text-slate-300 mb-2">Select a conversation</h3>
                  <p className="text-sm sm:text-base text-slate-500">Choose a conversation from the list to view details</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="max-w-6xl mx-auto mt-20 pt-12 border-t border-slate-700">
          <div className="text-center">
            <div className="inline-flex items-center gap-3 mb-6 px-6 py-3 rounded-full bg-gradient-to-r from-slate-800 to-slate-900 border border-slate-600 hover:shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300">
              <div className="p-2 rounded-full bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 hover:scale-110 transition-transform duration-300">
                <MessageCircle className="w-5 h-5 text-cyan-400" />
              </div>
              <span className="text-slate-200 text-lg font-semibold hover:text-cyan-400 transition-colors">Conversation History</span>
            </div>
            <p className="text-slate-400 text-sm max-w-2xl mx-auto mb-8 hover:text-slate-300 transition-colors">
              Complete visibility into all customer interactions. Track AI agent performance and conversation outcomes.
            </p>
            <div className="border-t border-slate-700 pt-8">
              <p className="text-slate-500 text-sm hover:text-slate-400 transition-colors">
                © 2026 TaskFlow AI Conversation Tracker. Built for the CRM Digital FTE Factory Final Hackathon 5.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}