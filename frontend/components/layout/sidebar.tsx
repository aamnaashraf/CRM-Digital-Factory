"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Home,
  MessageSquare,
  Settings,
  BarChart3,
  Zap,
  Activity,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "Channels", href: "/", icon: Home },
  { name: "Dashboard", href: "/dashboard", icon: BarChart3 },
  { name: "Activity", href: "/activity", icon: Activity },
  { name: "Conversations", href: "/conversations", icon: MessageSquare },
  { name: "Support Form", href: "/support", icon: MessageSquare },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Reports", href: "/reports", icon: BarChart3 },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar({ isMobile = false, onToggle }: { isMobile?: boolean; onToggle?: () => void }) {
  const pathname = usePathname();

  return (
    <div className={`${isMobile ? 'w-64 h-full absolute inset-y-0 z-50' : 'w-64'} bg-slate-950 border-r border-slate-800 flex flex-col h-full`}>
      {/* Logo */}
      <div className="p-6 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-gradient-to-br from-amber-500 to-orange-600 rounded-lg flex items-center justify-center shadow-lg shadow-amber-500/30">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-slate-100">TaskFlow AI</h1>
            <p className="text-xs text-slate-400">Customer Success</p>
          </div>
        </div>

        {/* Close button for mobile */}
        {isMobile && (
          <button
            onClick={onToggle}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors"
          >
            <svg className="w-6 h-6 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              onClick={() => isMobile && onToggle && onToggle()} // Close sidebar on mobile when clicking a link
              className={cn(
                "flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200",
                isActive
                  ? "bg-gradient-to-r from-amber-600 to-orange-600 text-white shadow-lg shadow-amber-500/30"
                  : "text-slate-400 hover:bg-slate-800 hover:text-amber-400 hover:shadow-md hover:shadow-amber-500/10"
              )}
            >
              <item.icon className="w-5 h-5" />
              <span className="font-medium">{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-slate-800">
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-lg p-4 border border-slate-700">
          <h3 className="text-sm font-semibold text-slate-200 mb-1">
            AI Agent Status
          </h3>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-amber-500 rounded-full animate-pulse shadow-lg shadow-amber-500/50"></div>
            <span className="text-xs text-slate-300">Online & Active</span>
          </div>
          <p className="text-xs text-slate-400 mt-2">
            Response time: &lt;3s
          </p>
        </div>
      </div>
    </div>
  );
}
