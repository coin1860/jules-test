'use client';

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { StatusCard } from '@/components/StatusCard';
import { Controls } from '@/components/Controls';
import { StrategyConfig } from '@/components/StrategyConfig';
import { TradeHistory } from '@/components/TradeHistory';
import { PriceChart } from '@/components/PriceChart';

const API_URL = 'http://localhost:8000';

export default function Dashboard() {
  const [status, setStatus] = useState<any>(null);
  const [trades, setTrades] = useState<any[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchStatus = async () => {
    try {
      const res = await axios.get(`${API_URL}/status`);
      setStatus(res.data);

      if (res.data.price > 0) {
        setChartData(prev => {
          const newItem = { time: new Date().toLocaleTimeString(), price: res.data.price };
          // Keep last 50 points
          const newData = [...prev, newItem];
          if (newData.length > 50) return newData.slice(newData.length - 50);
          return newData;
        });
      }
    } catch (err) {
      console.error("Error fetching status", err);
    }
  };

  const fetchHistory = async () => {
    try {
      const res = await axios.get(`${API_URL}/history`);
      setTrades(res.data.reverse()); // Show newest first
    } catch (err) {
      console.error("Error fetching history", err);
    }
  };

  useEffect(() => {
    fetchStatus();
    fetchHistory();
    setLoading(false);

    const interval = setInterval(() => {
      fetchStatus();
      fetchHistory();
    }, 2000); // Poll every 2 seconds

    return () => clearInterval(interval);
  }, []);

  const handleStart = async () => {
    await axios.post(`${API_URL}/start`);
    fetchStatus();
  };

  const handleStop = async () => {
    await axios.post(`${API_URL}/stop`);
    fetchStatus();
  };

  const handleConfigUpdate = async (short: number, long: number) => {
    try {
      await axios.post(`${API_URL}/config`, { short_window: short, long_window: long });
      alert("Configuration Updated");
      fetchStatus();
    } catch (err) {
      alert("Failed to update config");
    }
  };

  if (loading || !status) return <div className="p-10">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        <header className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">FX Quant POC (USD/CNY)</h1>
          <Controls isRunning={status.running} onStart={handleStart} onStop={handleStop} />
        </header>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <StatusCard label="Current Price" value={status.price.toFixed(4)} />
          <StatusCard label="Total Equity (CNY)" value={status.equity_cny.toFixed(2)} highlight />
          <StatusCard label="USD Balance" value={status.balances.usd.toFixed(2)} />
          <StatusCard label="CNY Balance" value={status.balances.cny.toFixed(2)} />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
             <div className="md:col-span-2 space-y-6">
                 <PriceChart data={chartData} />
                 <TradeHistory trades={trades} />
             </div>
             <div className="space-y-6">
                 <div className="bg-white p-4 rounded shadow">
                    <h3 className="text-lg font-semibold mb-2">Current Signal</h3>
                    <div className={`text-4xl font-bold ${status.signal === 'BUY' ? 'text-green-600' : status.signal === 'SELL' ? 'text-red-600' : 'text-gray-500'}`}>
                        {status.signal}
                    </div>
                 </div>
                 <StrategyConfig
                    shortWindow={status.strategy.short_window}
                    longWindow={status.strategy.long_window}
                    onUpdate={handleConfigUpdate}
                 />
             </div>
        </div>
      </div>
    </div>
  );
}
