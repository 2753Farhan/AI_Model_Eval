// app/settings/page.tsx
'use client';

import { useState } from 'react';
import { Card } from '@/components/common/Card';

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    apiUrl: 'http://localhost:5001/api',
    autoRefresh: true,
    refreshInterval: 30,
    theme: 'light',
    defaultModels: ['codellama:7b'],
    exportFormat: 'html',
  });

  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    // In a real app, save to localStorage or API
    localStorage.setItem('settings', JSON.stringify(settings));
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Settings</h1>

      {saved && (
        <div className="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
          Settings saved successfully!
        </div>
      )}

      <div className="space-y-6">
        {/* API Configuration */}
        <Card title="API Configuration">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                API URL
              </label>
              <input
                type="text"
                value={settings.apiUrl}
                onChange={(e) => setSettings({ ...settings, apiUrl: e.target.value })}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </Card>

        {/* Dashboard Settings */}
        <Card title="Dashboard">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Auto Refresh</span>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.autoRefresh}
                  onChange={(e) =>
                    setSettings({ ...settings, autoRefresh: e.target.checked })
                  }
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>

            {settings.autoRefresh && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Refresh Interval (seconds)
                </label>
                <input
                  type="number"
                  value={settings.refreshInterval}
                  onChange={(e) =>
                    setSettings({
                      ...settings,
                      refreshInterval: parseInt(e.target.value),
                    })
                  }
                  min={5}
                  max={300}
                  className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            )}
          </div>
        </Card>

        {/* Export Settings */}
        <Card title="Export">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Default Export Format
            </label>
            <select
              value={settings.exportFormat}
              onChange={(e) => setSettings({ ...settings, exportFormat: e.target.value })}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="html">HTML</option>
              <option value="pdf">PDF</option>
              <option value="csv">CSV</option>
              <option value="json">JSON</option>
            </select>
          </div>
        </Card>

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            onClick={handleSave}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
}