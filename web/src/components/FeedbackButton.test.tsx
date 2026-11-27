import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import FeedbackButton from './FeedbackButton';

const dialog = () => document.querySelector('dialog')!;

describe('FeedbackButton', () => {
  it('keeps the dialog closed until the button is clicked', () => {
    render(<FeedbackButton />);
    expect(dialog()).not.toHaveAttribute('open');
  });

  it('opens the dialog when the button is clicked', async () => {
    render(<FeedbackButton />);

    await userEvent.click(screen.getByRole('button', { name: 'Send feedback' }));

    expect(dialog()).toHaveAttribute('open');
  });

  it('closes the dialog again with Cancel', async () => {
    render(<FeedbackButton />);
    await userEvent.click(screen.getByRole('button', { name: 'Send feedback' }));

    await userEvent.click(screen.getByRole('button', { name: 'Cancel' }));

    expect(dialog()).not.toHaveAttribute('open');
  });
});
