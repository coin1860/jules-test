import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Controls } from '@/components/Controls';

describe('Controls', () => {
  it('calls onStart when Start is clicked', () => {
    const onStart = jest.fn();
    const onStop = jest.fn();
    render(<Controls isRunning={false} onStart={onStart} onStop={onStop} />);

    fireEvent.click(screen.getByText('Start'));
    expect(onStart).toHaveBeenCalled();
  });

  it('calls onStop when Stop is clicked', () => {
    const onStart = jest.fn();
    const onStop = jest.fn();
    render(<Controls isRunning={true} onStart={onStart} onStop={onStop} />);

    fireEvent.click(screen.getByText('Stop'));
    expect(onStop).toHaveBeenCalled();
  });

  it('disables Start when running', () => {
    render(<Controls isRunning={true} onStart={jest.fn()} onStop={jest.fn()} />);
    expect(screen.getByText('Start')).toBeDisabled();
  });
});
