'use client';

import React, { useState, useEffect } from 'react';

interface StrategyConfigProps {
  shortWindow: number;
  longWindow: number;
  onUpdate: (short: number, long: number) => void;
}

export const StrategyConfig: React.FC<StrategyConfigProps> = ({ shortWindow, longWindow, onUpdate }) => {
  const [localShort, setLocalShort] = useState(shortWindow);
  const [localLong, setLocalLong] = useState(longWindow);

  useEffect(() => {
    setLocalShort(shortWindow);
    setLocalLong(longWindow);
  }, [shortWindow, longWindow]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onUpdate(localShort, localLong);
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 bg-white rounded shadow-md border border-gray-200">
      <h3 className="text-lg font-semibold mb-4">Strategy Parameters</h3>
      <div className="flex gap-4 items-end">
        <div>
          <label className="block text-sm font-medium text-gray-700">Short Window</label>
          <input
            type="number"
            value={localShort}
            onChange={(e) => setLocalShort(parseInt(e.target.value))}
            className="mt-1 block w-24 border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Long Window</label>
          <input
            type="number"
            value={localLong}
            onChange={(e) => setLocalLong(parseInt(e.target.value))}
            className="mt-1 block w-24 border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
          />
        </div>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 h-10"
        >
          Update
        </button>
      </div>
    </form>
  );
};
