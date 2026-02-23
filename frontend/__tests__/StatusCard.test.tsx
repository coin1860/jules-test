import React from 'react';
import { render, screen } from '@testing-library/react';
import { StatusCard } from '@/components/StatusCard';

describe('StatusCard', () => {
  it('renders label and value', () => {
    render(<StatusCard label="Price" value={100} />);
    expect(screen.getByText('Price')).toBeInTheDocument();
    expect(screen.getByText('100')).toBeInTheDocument();
  });
});
