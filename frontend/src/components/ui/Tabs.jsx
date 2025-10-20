// frontend/src/components/ui/Tabs.jsx

import React from 'react';
import clsx from 'clsx';

export default function Tabs({ tabs, activeTab, onTabClick }) {
  return (
    <div>
      <div className="sm:hidden">
        <label htmlFor="tabs" className="sr-only">
          Selecione uma aba
        </label>
        <select
          id="tabs"
          name="tabs"
          className="block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
          value={activeTab}
          onChange={(e) => onTabClick(e.target.value)}
        >
          {tabs.map((tab) => (
            <option key={tab.id} value={tab.id}>{tab.name}</option>
          ))}
        </select>
      </div>
      <div className="hidden sm:block">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8" aria-label="Tabs">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => onTabClick(tab.id)}
                className={clsx(
                  'whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors',
                  activeTab === tab.id
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                )}
              >
                {tab.name}
              </button>
            ))}
          </nav>
        </div>
      </div>
    </div>
  );
}
