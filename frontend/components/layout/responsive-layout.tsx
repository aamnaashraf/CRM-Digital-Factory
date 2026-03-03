"use client";

import { useState, useEffect } from "react";
import { usePathname } from "next/navigation";
import { Sidebar } from "./sidebar";

export function ResponsiveLayout({ children }: { children: React.ReactNode }) {
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const pathname = usePathname();

  // Close mobile sidebar when route changes
  useEffect(() => {
    setIsMobileSidebarOpen(false);
  }, [pathname]);

  return (
    <div className="flex h-screen bg-slate-950">
      {/* Desktop Sidebar - Always visible on md and larger, hidden on smaller screens */}
      <div className="hidden md:block">
        <Sidebar />
      </div>

      {/* Mobile Sidebar - Overlay when open */}
      {isMobileSidebarOpen && (
        <div className="fixed inset-0 z-40 md:hidden">
          <div className="absolute inset-0 bg-black/50" onClick={() => setIsMobileSidebarOpen(false)} />
          <div className="relative w-64 h-full bg-slate-950">
            <Sidebar isMobile={true} onToggle={() => setIsMobileSidebarOpen(false)} />
          </div>
        </div>
      )}

      {/* Mobile Menu Button - Only visible on small screens */}
      <div className="fixed top-4 left-4 z-30 md:hidden">
        <button
          onClick={() => setIsMobileSidebarOpen(true)}
          className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors"
        >
          <svg className="w-6 h-6 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
        </button>
      </div>

      <main className="flex-1 overflow-y-auto bg-slate-900 md:ml-0 transition-all duration-300">
        {/* Add top padding only on mobile to account for the mobile menu button */}
        <div className="md:ml-0">
          {children}
        </div>
      </main>
    </div>
  );
}