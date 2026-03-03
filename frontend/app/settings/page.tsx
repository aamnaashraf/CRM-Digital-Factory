"use client";

import { useState, useEffect } from "react";
import { Settings as SettingsIcon, Database, Zap, Save, Shield } from "lucide-react";
import { apiClient } from "@/lib/api";

// Simple toast implementation since we don't have a toast library configured in this project
const toast = {
  success: (msg: string) => console.log('Success:', msg),
  error: (msg: string) => console.error('Error:', msg),
};

export default function SettingsPage() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [settings, setSettings] = useState({
    autoResponse: true,
    sentimentAnalysis: true,
    escalationAlerts: true,
    dailyReports: false,
    openai_api_key: "",
    openai_model: "llama3-70b-8192",
  });

  // Load initial settings
  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const response = await apiClient.getSettings();
        setSettings({
          autoResponse: response.data.auto_response,
          sentimentAnalysis: response.data.sentiment_analysis,
          escalationAlerts: response.data.escalation_alerts,
          dailyReports: response.data.daily_reports,
          openai_api_key: response.data.openai_api_key,
          openai_model: response.data.openai_model,
        });
      } catch (error) {
        console.error("Failed to fetch settings:", error);
        // Use defaults if there's an error
        toast.error("Failed to load settings. Using default values.");
      } finally {
        setLoading(false);
      }
    };

    fetchSettings();
  }, []);

  const handleToggle = (key: string) => {
    setSettings(prev => ({ ...prev, [key]: !prev[key as keyof typeof prev] }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await apiClient.updateSettings({
        auto_response: settings.autoResponse,
        sentiment_analysis: settings.sentimentAnalysis,
        escalation_alerts: settings.escalationAlerts,
        daily_reports: settings.dailyReports,
        openai_api_key: settings.openai_api_key,
        openai_model: settings.openai_model,
      });
      toast.success("Settings saved successfully!");
    } catch (error) {
      console.error("Failed to save settings:", error);
      toast.error("Failed to save settings. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  const handleApiKeyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSettings(prev => ({ ...prev, openai_api_key: e.target.value }));
  };

  const handleModelChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSettings(prev => ({ ...prev, openai_model: e.target.value }));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-500 mx-auto"></div>
          <p className="mt-4 text-slate-400">Loading settings...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Animated background elements */}
      <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-20 right-20 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      <div className="absolute top-1/2 right-1/3 w-64 h-64 bg-amber-500/10 rounded-full blur-3xl animate-pulse delay-500"></div>

      <div className="relative z-10 p-8">
        <div className="mb-10 text-center">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent mb-4">
            Settings
          </h1>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Configure your AI agent and system preferences
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-7xl mx-auto">
          {/* Main Settings */}
          <div className="lg:col-span-2 space-y-6">
            {/* General Settings */}
            <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-6 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 relative overflow-hidden">
              <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-blue-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
              <div className="relative z-10">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-3 rounded-full bg-blue-500/20 backdrop-blur-sm border border-blue-500/30">
                    <SettingsIcon className="w-6 h-6 text-blue-400" />
                  </div>
                  <h2 className="text-xl font-semibold text-slate-200">General Settings</h2>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700">
                    <div>
                      <p className="text-slate-200 font-medium">Auto Response</p>
                      <p className="text-sm text-slate-500">Automatically respond to customer inquiries</p>
                    </div>
                    <button
                      onClick={() => handleToggle('autoResponse')}
                      className={`relative w-12 h-6 rounded-full transition-colors ${
                        settings.autoResponse ? 'bg-blue-500' : 'bg-slate-600'
                      }`}
                      disabled={saving}
                    >
                      <span
                        className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${
                          settings.autoResponse ? 'translate-x-6' : ''
                        }`}
                      />
                    </button>
                  </div>

                  <div className="flex items-center justify-between p-4 bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700">
                    <div>
                      <p className="text-slate-200 font-medium">Sentiment Analysis</p>
                      <p className="text-sm text-slate-500">Analyze customer sentiment in real-time</p>
                    </div>
                    <button
                      onClick={() => handleToggle('sentimentAnalysis')}
                      className={`relative w-12 h-6 rounded-full transition-colors ${
                        settings.sentimentAnalysis ? 'bg-blue-500' : 'bg-slate-600'
                      }`}
                      disabled={saving}
                    >
                      <span
                        className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${
                          settings.sentimentAnalysis ? 'translate-x-6' : ''
                        }`}
                      />
                    </button>
                  </div>

                  <div className="flex items-center justify-between p-4 bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700">
                    <div>
                      <p className="text-slate-200 font-medium">Escalation Alerts</p>
                      <p className="text-sm text-slate-500">Get notified when tickets are escalated</p>
                    </div>
                    <button
                      onClick={() => handleToggle('escalationAlerts')}
                      className={`relative w-12 h-6 rounded-full transition-colors ${
                        settings.escalationAlerts ? 'bg-blue-500' : 'bg-slate-600'
                      }`}
                      disabled={saving}
                    >
                      <span
                        className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${
                          settings.escalationAlerts ? 'translate-x-6' : ''
                        }`}
                      />
                    </button>
                  </div>

                  <div className="flex items-center justify-between p-4 bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700">
                    <div>
                      <p className="text-slate-200 font-medium">Daily Reports</p>
                      <p className="text-sm text-slate-500">Receive daily performance reports via email</p>
                    </div>
                    <button
                      onClick={() => handleToggle('dailyReports')}
                      className={`relative w-12 h-6 rounded-full transition-colors ${
                        settings.dailyReports ? 'bg-blue-500' : 'bg-slate-600'
                      }`}
                      disabled={saving}
                    >
                      <span
                        className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${
                          settings.dailyReports ? 'translate-x-6' : ''
                        }`}
                      />
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* API Configuration */}
            <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-6 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 relative overflow-hidden">
              <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-orange-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
              <div className="relative z-10">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-3 rounded-full bg-orange-500/20 backdrop-blur-sm border border-orange-500/30">
                    <Database className="w-6 h-6 text-orange-400" />
                  </div>
                  <h2 className="text-xl font-semibold text-slate-200">API Configuration</h2>
                </div>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      OpenAI API Key
                    </label>
                    <input
                      type="password"
                      value={settings.openai_api_key}
                      onChange={handleApiKeyChange}
                      className="w-full px-4 py-3 bg-slate-900/80 backdrop-blur-sm border border-slate-700 rounded-xl text-slate-200"
                      placeholder="Enter your API key"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Model
                    </label>
                    <select
                      value={settings.openai_model}
                      onChange={handleModelChange}
                      className="w-full px-4 py-3 bg-slate-900/80 backdrop-blur-sm border border-slate-700 rounded-xl text-slate-200"
                    >
                      <option value="llama3-70b-8192">Llama 3 70B</option>
                      <option value="gpt-4-turbo">GPT-4 Turbo</option>
                      <option value="gpt-4">GPT-4</option>
                      <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            <button
              onClick={handleSave}
              disabled={saving}
              className={`w-full group bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg shadow-blue-500/20 hover:shadow-2xl hover:scale-[1.02] flex items-center justify-center gap-2 ${
                saving ? 'opacity-75 cursor-not-allowed' : ''
              }`}
            >
              {saving ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Saving...
                </>
              ) : (
                <>
                  <Save className="w-5 h-5" />
                  Save Changes
                </>
              )}
            </button>
          </div>

          {/* Sidebar Info */}
          <div className="space-y-6">
            <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-6 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 relative overflow-hidden">
              <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-amber-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
              <div className="relative z-10">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-3 rounded-full bg-amber-500/20 backdrop-blur-sm border border-amber-500/30">
                    <Zap className="w-6 h-6 text-amber-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-slate-200">System Status</h3>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 text-sm">AI Agent</span>
                    <span className="text-green-400 text-sm font-medium">Online</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 text-sm">Database</span>
                    <span className="text-green-400 text-sm font-medium">Connected</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 text-sm">API</span>
                    <span className="text-green-400 text-sm font-medium">Active</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 p-6 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 relative overflow-hidden">
              <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-red-500/10 group-hover:scale-150 group-hover:opacity-20 transition-all duration-1000"></div>
              <div className="relative z-10">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-3 rounded-full bg-red-500/20 backdrop-blur-sm border border-red-500/30">
                    <Shield className="w-6 h-6 text-red-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-slate-200">Security</h3>
                </div>
                <p className="text-slate-400 text-sm mb-4">
                  All data is encrypted and stored securely. API keys are never exposed.
                </p>
                <button className="w-full group-hover:bg-slate-700/80 bg-slate-700/60 backdrop-blur-sm border border-slate-600 text-slate-200 py-2 px-4 rounded-xl text-sm transition-all">
                  View Security Settings
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Beautiful Footer */}
        <div className="max-w-6xl mx-auto mt-20 pt-12 border-t border-slate-700">
          <div className="text-center">
            <div className="inline-flex items-center gap-3 mb-6 px-6 py-3 rounded-full bg-gradient-to-r from-slate-800 to-slate-900 border border-slate-600 hover:shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300">
              <div className="p-2 rounded-full bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 hover:scale-110 transition-transform duration-300">
                <SettingsIcon className="w-5 h-5 text-cyan-400" />
              </div>
              <span className="text-slate-200 text-lg font-semibold hover:text-cyan-400 transition-colors">System Configuration</span>
            </div>

            <p className="text-slate-400 text-sm max-w-2xl mx-auto mb-8 hover:text-slate-300 transition-colors">
              Secure configuration for your AI-powered customer success platform. Customize features and preferences.
            </p>

            <div className="flex flex-wrap justify-center gap-8 text-xs text-slate-500 mb-8">
              <span className="hover:text-cyan-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-cyan-400/50 pb-1">AI Settings</span>
              <span className="hover:text-blue-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-blue-400/50 pb-1">Security</span>
              <span className="hover:text-purple-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-purple-400/50 pb-1">API Configuration</span>
              <span className="hover:text-emerald-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-emerald-400/50 pb-1">Automation</span>
              <span className="hover:text-amber-400 hover:scale-110 transition-all duration-300 cursor-pointer border-b border-transparent hover:border-amber-400/50 pb-1">Preferences</span>
            </div>

            <div className="border-t border-slate-700 pt-8">
              <p className="text-slate-500 text-sm hover:text-slate-400 transition-colors">
                © 2026 TaskFlow AI Configuration Panel. Built for the CRM Digital FTE Factory Final Hackathon 5.
              </p>
              <p className="text-slate-600 text-xs mt-2 hover:text-slate-500 transition-colors">
                Secure and customizable AI agent configuration.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
