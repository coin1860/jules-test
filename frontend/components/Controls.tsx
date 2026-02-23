'use client';

import React from 'react';

interface ControlsProps {
  isRunning: boolean;
  onStart: () => void;
  onStop: () => void;
}

export const Controls: React.FC<ControlsProps> = ({ isRunning, onStart, onStop }) => {
  return (
    <div className="flex gap-4">
      <button
        onClick={onStart}
        disabled={isRunning}
        className={`px-4 py-2 font-bold text-white rounded ${
          isRunning ? 'bg-gray-400 cursor-not-allowed' : 'bg-green-500 hover:bg-green-700'
        }`}
      >
        Start
      </button>
      <button
        onClick={onStop}
        disabled={!isRunning}
        className={`px-4 py-2 font-bold text-white rounded ${
          !isRunning ? 'bg-gray-400 cursor-not-allowed' : 'bg-red-500 hover:bg-red-700'
        }`}
      >
        Stop
      </button>
    </div>
  );
};
