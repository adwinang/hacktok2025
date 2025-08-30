import Link from "next/link";
import { LayoutDashboard, Settings, User, ChevronUp, Bot } from "lucide-react";

export default function Sidenav() {
  return (
    <div className="w-64 h-screen flex flex-col bg-white border-r border-gray-200 sticky top-0 left-0">
      {/* Header */}
      <div className="p-6 border-b border-gray-100">
        <h1 className="text-xl font-semibold text-gray-900">hacktok</h1>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <div className="space-y-0">
          <Link
            href="/"
            className="flex items-center gap-3 px-3 py-2.5 text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors duration-150 group"
          >
            <LayoutDashboard className="h-5 w-5 text-gray-500 group-hover:text-gray-700" />
            <span className="font-medium">Dashboard</span>
          </Link>

          <Link
            href="/sources"
            className="flex items-center gap-3 px-3 py-2.5 text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors duration-150 group"
          >
            <Settings className="h-5 w-5 text-gray-500 group-hover:text-gray-700" />
            <span className="font-medium">Sources</span>
          </Link>

          <Link
            href="http://localhost:5678"
            className="flex items-center gap-3 px-3 py-2.5 text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors duration-150 group"
          >
            <Bot className="h-5 w-5 text-gray-500 group-hover:text-gray-700" />
            <span className="font-medium">Automation</span>
          </Link>
        </div>
      </nav>

      {/* User Profile */}
      <div className="p-4 border-t border-gray-100">
        <div className="flex items-center gap-3 px-3 py-2.5 hover:bg-gray-50 rounded-lg cursor-pointer transition-colors duration-150">
          <div className="h-8 w-8 bg-gray-200 rounded-full flex items-center justify-center">
            <User className="h-4 w-4 text-gray-600" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-900">User</p>
            <p className="text-xs text-gray-500">user@example.com</p>
          </div>
          <ChevronUp className="h-4 w-4 text-gray-400" />
        </div>
      </div>
    </div>
  );
}
