import { Mail, MessageCircle, Globe, Clock, User, Smile, Frown, Meh } from "lucide-react";
import { cn } from "@/lib/utils";

interface ActivityItem {
  id: string;
  customer: string;
  message: string;
  channel: string;
  time: string;
  sentiment: number;
  status: string;
}

interface RecentActivityProps {
  activities: ActivityItem[];
  loading: boolean;
}

const channelIcons = {
  email: Mail,
  whatsapp: MessageCircle,
  web: Globe,
};

const channelColors = {
  email: "bg-gradient-to-br from-amber-500/20 to-orange-500/20 text-amber-400 border-amber-500/30",
  whatsapp: "bg-gradient-to-br from-green-500/20 to-emerald-500/20 text-green-400 border-green-500/30",
  web: "bg-gradient-to-br from-blue-500/20 to-indigo-500/20 text-blue-400 border-blue-500/30",
};

export function RecentActivity({ activities, loading }: RecentActivityProps) {
  const getSentimentColor = (sentiment: number) => {
    if (sentiment >= 0.5) return "bg-gradient-to-r from-green-500/20 to-emerald-500/20 text-green-400 border-green-500/30";
    if (sentiment >= 0) return "bg-gradient-to-r from-yellow-500/20 to-amber-500/20 text-yellow-400 border-yellow-500/30";
    return "bg-gradient-to-r from-red-500/20 to-pink-500/20 text-red-400 border-red-500/30";
  };

  const getSentimentLabel = (sentiment: number) => {
    if (sentiment >= 0.5) return "Positive";
    if (sentiment >= 0) return "Neutral";
    return "Negative";
  };

  const getSentimentIcon = (sentiment: number) => {
    if (sentiment >= 0.5) return <Smile className="w-4 h-4" />;
    if (sentiment >= 0) return <Meh className="w-4 h-4" />;
    return <Frown className="w-4 h-4" />;
  };

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-full bg-slate-700">
            <Clock className="w-5 h-5 text-slate-400" />
          </div>
          <h3 className="text-lg font-semibold text-slate-200">Recent Activity</h3>
        </div>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse flex items-center gap-4 p-4 rounded-xl bg-slate-800/50">
              <div className="w-12 h-12 bg-slate-700 rounded-full"></div>
              <div className="flex-1 space-y-2">
                <div className="h-4 bg-slate-700 rounded w-1/4"></div>
                <div className="h-3 bg-slate-700 rounded w-1/2"></div>
                <div className="h-3 bg-slate-700 rounded w-1/3"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (activities.length === 0) {
    return (
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-12 text-center relative overflow-hidden">
        <div className="absolute top-0 right-0 w-32 h-32 bg-slate-700/20 rounded-full -translate-y-16 translate-x-16"></div>
        <div className="absolute bottom-0 left-0 w-24 h-24 bg-slate-700/20 rounded-full translate-y-12 -translate-x-12"></div>
        <div className="relative z-10">
          <Clock className="w-12 h-12 text-slate-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-slate-300 mb-2">No Recent Activity</h3>
          <p className="text-slate-500">When customers interact with your support, they'll appear here.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-full bg-gradient-to-r from-blue-500/20 to-purple-500/20 backdrop-blur-sm border border-blue-500/30">
          <Clock className="w-5 h-5 text-blue-400" />
        </div>
        <h3 className="text-xl font-bold bg-gradient-to-r from-slate-100 to-slate-300 bg-clip-text text-transparent">
          Recent Activity
        </h3>
      </div>

      <div className="space-y-4">
        {activities.map((activity, index) => {
          const Icon = channelIcons[activity.channel as keyof typeof channelIcons] || Globe;
          const channelColor = channelColors[activity.channel as keyof typeof channelColors] || "bg-slate-700 text-slate-400 border-slate-600";

          return (
            <div
              key={`${activity.id}-${index}`}
              className="group p-3 sm:p-4 rounded-xl bg-slate-800/50 border border-slate-700 hover:border-slate-600 hover:shadow-lg hover:shadow-slate-800/50 transition-all duration-300"
            >
              <div className="flex items-start gap-3 sm:gap-4">
                {/* Circular channel indicator */}
                <div className={cn(
                  "p-2 sm:p-3 rounded-full backdrop-blur-sm border-2 flex-shrink-0",
                  channelColor
                )}>
                  <Icon className="w-4 h-4 sm:w-5 sm:h-5" />
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 sm:gap-2 mb-2">
                    <div className="flex items-center gap-2 min-w-0">
                      <User className="w-4 h-4 text-slate-500 flex-shrink-0" />
                      <p className="text-sm font-semibold text-slate-200 truncate">
                        {activity.customer}
                      </p>
                    </div>
                    <span className="text-xs text-slate-500 flex-shrink-0">{activity.time}</span>
                  </div>

                  <p className="text-sm text-slate-300 mb-3 line-clamp-2">
                    {activity.message}
                  </p>

                  <div className="flex flex-wrap items-center gap-2">
                    {/* Sentiment indicator */}
                    <div className={cn(
                      "flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border backdrop-blur-sm",
                      getSentimentColor(activity.sentiment)
                    )}>
                      {getSentimentIcon(activity.sentiment)}
                      <span className="hidden sm:inline">{getSentimentLabel(activity.sentiment)}</span>
                    </div>

                    {/* Channel indicator */}
                    <span className="text-xs text-slate-500 capitalize">
                      via {activity.channel}
                    </span>

                    {/* Status indicator */}
                    <span className={cn(
                      "text-xs px-2 py-1 rounded-full capitalize",
                      activity.status === 'open' ? 'text-blue-400 bg-blue-500/20' :
                      activity.status === 'resolved' ? 'text-green-400 bg-green-500/20' :
                      activity.status === 'escalated' ? 'text-orange-400 bg-orange-500/20' :
                      'text-slate-400 bg-slate-600/20'
                    )}>
                      {activity.status}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
