import Link from "next/link";
import { ReactNode } from "react";
import { ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";

interface ChannelCardProps {
  icon: ReactNode;
  title: string;
  description: string;
  status: string;
  color: "amber" | "orange" | "yellow" | "cyan" | "purple" | "pink" | "green" | "blue";
  href: string;
}

const colorClasses = {
  amber: {
    bg: "bg-gradient-to-br from-amber-500/20 to-orange-500/20",
    icon: "text-amber-400",
    badge: "bg-amber-500/20 text-amber-300 border-amber-500/30",
    hover: "hover:border-amber-500/40 hover:shadow-lg hover:shadow-amber-500/25",
    glow: "hover:shadow-2xl",
  },
  orange: {
    bg: "bg-gradient-to-br from-orange-500/20 to-red-500/20",
    icon: "text-orange-400",
    badge: "bg-orange-500/20 text-orange-300 border-orange-500/30",
    hover: "hover:border-orange-500/40 hover:shadow-lg hover:shadow-orange-500/25",
    glow: "hover:shadow-2xl",
  },
  yellow: {
    bg: "bg-gradient-to-br from-yellow-500/20 to-amber-500/20",
    icon: "text-yellow-400",
    badge: "bg-yellow-500/20 text-yellow-300 border-yellow-500/30",
    hover: "hover:border-yellow-500/40 hover:shadow-lg hover:shadow-yellow-500/25",
    glow: "hover:shadow-2xl",
  },
  cyan: {
    bg: "bg-gradient-to-br from-cyan-500/20 to-blue-500/20",
    icon: "text-cyan-400",
    badge: "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
    hover: "hover:border-cyan-500/40 hover:shadow-lg hover:shadow-cyan-500/25",
    glow: "hover:shadow-2xl",
  },
  purple: {
    bg: "bg-gradient-to-br from-purple-500/20 to-pink-500/20",
    icon: "text-purple-400",
    badge: "bg-purple-500/20 text-purple-300 border-purple-500/30",
    hover: "hover:border-purple-500/40 hover:shadow-lg hover:shadow-purple-500/25",
    glow: "hover:shadow-2xl",
  },
  pink: {
    bg: "bg-gradient-to-br from-pink-500/20 to-rose-500/20",
    icon: "text-pink-400",
    badge: "bg-pink-500/20 text-pink-300 border-pink-500/30",
    hover: "hover:border-pink-500/40 hover:shadow-lg hover:shadow-pink-500/25",
    glow: "hover:shadow-2xl",
  },
  green: {
    bg: "bg-gradient-to-br from-green-500/20 to-emerald-500/20",
    icon: "text-green-400",
    badge: "bg-green-500/20 text-green-300 border-green-500/30",
    hover: "hover:border-green-500/40 hover:shadow-lg hover:shadow-green-500/25",
    glow: "hover:shadow-2xl",
  },
  blue: {
    bg: "bg-gradient-to-br from-blue-500/20 to-indigo-500/20",
    icon: "text-blue-400",
    badge: "bg-blue-500/20 text-blue-300 border-blue-500/30",
    hover: "hover:border-blue-500/40 hover:shadow-lg hover:shadow-blue-500/25",
    glow: "hover:shadow-2xl",
  },
};

export function ChannelCard({
  icon,
  title,
  description,
  status,
  color,
  href,
}: ChannelCardProps) {
  const colors = colorClasses[color];

  return (
    <Link href={href}>
      <div className={cn(
        "group relative bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-6 hover:scale-[1.03] transition-all duration-300 cursor-pointer overflow-hidden",
        colors.hover,
        colors.glow
      )}>
        {/* Animated background elements */}
        <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-white/5 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
        <div className="absolute -bottom-20 -left-20 w-32 h-32 rounded-full bg-white/5 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>

        <div className="relative z-10">
          <div className="flex items-start justify-between mb-4">
            {/* Circular icon container */}
            <div className={cn(
              "p-4 rounded-full bg-white/10 backdrop-blur-sm border-2",
              color === "amber" ? "border-amber-500/30" :
              color === "orange" ? "border-orange-500/30" :
              color === "yellow" ? "border-yellow-500/30" :
              color === "cyan" ? "border-cyan-500/30" :
              color === "purple" ? "border-purple-500/30" :
              color === "pink" ? "border-pink-500/30" :
              color === "green" ? "border-green-500/30" : "border-blue-500/30"
            )}>
              <div className={cn("transition-transform duration-300 group-hover:scale-110", colors.icon)}>
                {icon}
              </div>
            </div>
            <span
              className={cn(
                "text-xs font-medium px-3 py-1.5 rounded-full border backdrop-blur-sm",
                colors.badge
              )}
            >
              {status}
            </span>
          </div>

          <h3 className={cn(
            "text-xl font-bold bg-gradient-to-r from-slate-100 to-slate-300 bg-clip-text text-transparent mb-3 group-hover:",
            color === "amber" ? "text-amber-400 from-amber-400 to-orange-400" :
            color === "orange" ? "text-orange-400 from-orange-400 to-red-400" :
            color === "yellow" ? "text-yellow-400 from-yellow-400 to-amber-400" :
            color === "cyan" ? "text-cyan-400 from-cyan-400 to-blue-400" :
            color === "purple" ? "text-purple-400 from-purple-400 to-pink-400" :
            color === "pink" ? "text-pink-400 from-pink-400 to-rose-400" :
            color === "green" ? "text-green-400 from-green-400 to-emerald-400" : "text-blue-400 from-blue-400 to-indigo-400"
          )}>
            {title}
          </h3>
          <p className="text-slate-400 mb-5 line-clamp-2">
            {description}
          </p>

          <div className="flex items-center gap-2 text-slate-400 group-hover:text-slate-300 transition-colors">
            <span className="text-sm font-medium">Get Started</span>
            <div className={cn(
              "p-1.5 rounded-full bg-white/10 transition-all duration-300 group-hover:bg-current group-hover:text-slate-100",
              color === "amber" ? "text-amber-400 group-hover:bg-amber-500" :
              color === "orange" ? "text-orange-400 group-hover:bg-orange-500" :
              color === "yellow" ? "text-yellow-400 group-hover:bg-yellow-500" :
              color === "cyan" ? "text-cyan-400 group-hover:bg-cyan-500" :
              color === "purple" ? "text-purple-400 group-hover:bg-purple-500" :
              color === "pink" ? "text-pink-400 group-hover:bg-pink-500" :
              color === "green" ? "text-green-400 group-hover:bg-green-500" : "text-blue-400 group-hover:bg-blue-500"
            )}>
              <ArrowRight className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" />
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
}
