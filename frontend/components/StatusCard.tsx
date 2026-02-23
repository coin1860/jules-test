import React from 'react';

interface StatusCardProps {
  label: string;
  value: string | number;
  highlight?: boolean;
}

export const StatusCard: React.FC<StatusCardProps> = ({ label, value, highlight }) => {
  return (
    <div className={`p-4 rounded-lg shadow-md border ${highlight ? 'bg-blue-50 border-blue-200' : 'bg-white border-gray-200'}`}>
      <h3 className="text-sm font-medium text-gray-500">{label}</h3>
      <p className="mt-1 text-2xl font-semibold text-gray-900">{value}</p>
    </div>
  );
};
