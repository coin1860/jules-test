import React from 'react';
import { render, screen } from '@testing-library/react';
import { TradeHistory } from '@/components/TradeHistory';

describe('TradeHistory', () => {
  const trades = [
    {
      timestamp: '2023-01-01T10:00:00',
      action: 'BUY',
      currency: 'USD',
      amount: 100,
      price: 7.0,
      balance_cny: 9300,
      balance_usd: 100
    }
  ];

  it('renders table headers', () => {
    render(<TradeHistory trades={[]} />);
    expect(screen.getByText('Time')).toBeInTheDocument();
    expect(screen.getByText('Action')).toBeInTheDocument();
  });

  it('renders trade row', () => {
    render(<TradeHistory trades={trades} />);
    expect(screen.getByText('BUY')).toBeInTheDocument();
    expect(screen.getByText('7.0000')).toBeInTheDocument();
  });
});
