'use client';

import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface ChartDataPoint {
  time: string;
  price: number;
}

interface PriceChartProps {
  data: ChartDataPoint[];
}

export const PriceChart: React.FC<PriceChartProps> = ({ data }) => {
  return (
    <div className="h-64 w-full bg-white p-4 rounded shadow">
      <h3 className="text-lg font-semibold mb-2">Price History</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis domain={['auto', 'auto']} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="price" stroke="#8884d8" activeDot={{ r: 8 }} isAnimationActive={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
