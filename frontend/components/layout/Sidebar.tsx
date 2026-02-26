// components/layout/Sidebar.tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect } from 'react';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export const Sidebar = ({ isOpen, onClose }: SidebarProps) => {
  const pathname = usePathname();

  useEffect(() => {
    // Close sidebar on route change on mobile
    if (window.innerWidth < 1024) {
      onClose();
    }
  }, [pathname, onClose]);

  
const menuItems = [
  { href: '/dashboard', icon: '📊', label: 'Dashboard' },
  { href: '/datasets', icon: '📚', label: 'Datasets' }, // Already there
  { href: '/evaluations', icon: '📋', label: 'Evaluations' },
  { href: '/models', icon: '🤖', label: 'Models' },
  { href: '/models/compare', icon: '⚖️', label: 'Compare Models' },
  { href: '/playground', icon: '💻', label: 'Playground' },
  { href: '/finetuning', icon: '🎯', label: 'Fine-tuning' },
  { href: '/reports', icon: '📈', label: 'Reports' },
  { href: '/settings', icon: '⚙️', label: 'Settings' },
];

  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-gray-600 bg-opacity-75 transition-opacity z-20 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 transform ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:relative lg:translate-x-0 transition duration-200 ease-in-out z-30 w-64 bg-white shadow-lg`}
      >
        <div className="h-full flex flex-col">
          {/* Sidebar header */}
          <div className="flex items-center justify-between h-16 px-4 border-b lg:hidden">
            <span className="text-xl font-bold text-blue-600">Menu</span>
            <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Sidebar content */}
          <div className="flex-1 overflow-y-auto py-4">
            <nav className="px-2 space-y-1">
              {menuItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center px-4 py-2 text-sm font-medium rounded-md ${
                    pathname === item.href
                      ? 'bg-blue-50 text-blue-700'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <span className="mr-3 text-lg">{item.icon}</span>
                  {item.label}
                </Link>
              ))}
            </nav>

            {/* System info */}
            <div className="absolute bottom-0 left-0 right-0 p-4 border-t">
              <div className="text-xs text-gray-500">
                <p>System Status</p>
                <div className="flex items-center mt-1">
                  <div className="h-2 w-2 bg-green-500 rounded-full mr-2"></div>
                  <span>Connected</span>
                </div>
                <p className="mt-1">Ollama: Active</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};