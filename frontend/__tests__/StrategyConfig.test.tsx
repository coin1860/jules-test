import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { StrategyConfig } from '@/components/StrategyConfig';

describe('StrategyConfig', () => {
  it('renders initial values', () => {
    render(<StrategyConfig shortWindow={5} longWindow={20} onUpdate={jest.fn()} />);
    expect(screen.getByDisplayValue('5')).toBeInTheDocument();
    expect(screen.getByDisplayValue('20')).toBeInTheDocument();
  });

  it('calls onUpdate with new values', () => {
    const onUpdate = jest.fn();
    render(<StrategyConfig shortWindow={5} longWindow={20} onUpdate={onUpdate} />);

    fireEvent.change(screen.getByDisplayValue('5'), { target: { value: '10' } });
    fireEvent.change(screen.getByDisplayValue('20'), { target: { value: '30' } });
    fireEvent.click(screen.getByText('Update'));

    expect(onUpdate).toHaveBeenCalledWith(10, 30);
  });
});
