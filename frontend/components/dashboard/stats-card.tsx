import { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface StatsCardProps {
  title: string;
  value: string;
  icon: ReactNode;
  trend: string;
  color: "amber" | "orange" | "yellow" | "green" | "purple" | "pink" | "blue" | "indigo";
}

const colorClasses = {
  amber: "bg-gradient-to-br from-amber-500/20 to-amber-600/20 text-amber-300 border-amber-500/30",
  orange: "bg-gradient-to-br from-orange-500/20 to-orange-600/20 text-orange-300 border-orange-500/30",
  yellow: "bg-gradient-to-br from-yellow-500/20 to-yellow-600/20 text-yellow-300 border-yellow-500/30",
  green: "bg-gradient-to-br from-green-500/20 to-green-600/20 text-green-300 border-green-500/30",
  purple: "bg-gradient-to-br from-purple-500/20 to-purple-600/20 text-purple-300 border-purple-500/30",
  pink: "bg-gradient-to-br from-pink-500/20 to-pink-600/20 text-pink-300 border-pink-500/30",
  blue: "bg-gradient-to-br from-blue-500/20 to-blue-600/20 text-blue-300 border-blue-500/30",
  indigo: "bg-gradient-to-br from-indigo-500/20 to-indigo-600/20 text-indigo-300 border-indigo-500/30",
};

const hoverColors = {
  amber: "hover:border-amber-400/50 hover:shadow-lg hover:shadow-amber-500/25",
  orange: "hover:border-orange-400/50 hover:shadow-lg hover:shadow-orange-500/25",
  yellow: "hover:border-yellow-400/50 hover:shadow-lg hover:shadow-yellow-500/25",
  green: "hover:border-green-400/50 hover:shadow-lg hover:shadow-green-500/25",
  purple: "hover:border-purple-400/50 hover:shadow-lg hover:shadow-purple-500/25",
  pink: "hover:border-pink-400/50 hover:shadow-lg hover:shadow-pink-500/25",
  blue: "hover:border-blue-400/50 hover:shadow-lg hover:shadow-blue-500/25",
  indigo: "hover:border-indigo-400/50 hover:shadow-lg hover:shadow-indigo-500/25",
};

export function StatsCard({ title, value, icon, trend, color }: StatsCardProps) {
  return (
    <div className={cn(
      "bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-6 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 group relative overflow-hidden",
      colorClasses[color],
      hoverColors[color]
    )}>
      {/* Animated background elements */}
      <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-white/5 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
      <div className="absolute -bottom-20 -left-20 w-32 h-32 rounded-full bg-white/5 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>

      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-medium text-slate-300">{title}</h3>
          <div className={cn(
            "p-3 rounded-full bg-white/10 backdrop-blur-sm border-2",
            color === "amber" ? "border-amber-500/30" :
            color === "orange" ? "border-orange-500/30" :
            color === "yellow" ? "border-yellow-500/30" :
            color === "green" ? "border-green-500/30" :
            color === "purple" ? "border-purple-500/30" :
            color === "pink" ? "border-pink-500/30" :
            color === "blue" ? "border-blue-500/30" : "border-indigo-500/30"
          )}>
            {icon}
          </div>
        </div>
        <div className="space-y-1">
          <p className="text-4xl font-bold bg-gradient-to-r from-slate-100 to-slate-300 bg-clip-text text-transparent">
            {value}
          </p>
          <p className="text-sm text-slate-400 font-medium">{trend}</p>
        </div>
      </div>
    </div>
  );
}
