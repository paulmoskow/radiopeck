import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import FeedbackDialog from './FeedbackDialog';
import { FeedbackError } from '../lib/feedback';

// Only sendFeedback is replaced; FeedbackError stays the real class.
const send = vi.hoisted(() => vi.fn());
vi.mock('../lib/feedback', async importOriginal => ({
  ...(await importOriginal<typeof import('../lib/feedback')>()),
  sendFeedback: send,
}));

beforeEach(() => {
  send.mockReset();
});

function renderDialog(open = true) {
  const onClose = vi.fn();
  render(<FeedbackDialog open={open} onClose={onClose} />);
  return { onClose };
}

const messageField = () => screen.getByLabelText('Your message');
const sendButton = () => screen.getByRole('button', { name: /^Send/ });

describe('FeedbackDialog', () => {
  it('opens as a modal when "open" is true', () => {
    const showModal = vi.spyOn(HTMLDialogElement.prototype, 'showModal');
    renderDialog(true);
    expect(showModal).toHaveBeenCalled();
  });

  it('stays closed when "open" is false', () => {
    const showModal = vi.spyOn(HTMLDialogElement.prototype, 'showModal');
    renderDialog(false);
    expect(showModal).not.toHaveBeenCalled();
  });

  it('disables Send while the message is empty or only spaces', async () => {
    renderDialog();
    expect(sendButton()).toBeDisabled();

    await userEvent.type(messageField(), '   ');
    expect(sendButton()).toBeDisabled();

    await userEvent.type(messageField(), 'hi');
    expect(sendButton()).toBeEnabled();
  });

  it('counts the characters typed', async () => {
    renderDialog();
    await userEvent.type(messageField(), 'abc');
    expect(screen.getByText('3 / 2000')).toBeInTheDocument();
  });

  it('sends the message and the contact', async () => {
    send.mockResolvedValue(undefined);
    renderDialog();

    await userEvent.type(messageField(), 'hello');
    await userEvent.type(screen.getByLabelText('Contact (optional)'), '@me');
    await userEvent.click(sendButton());

    expect(send).toHaveBeenCalledWith({ message: 'hello', contact: '@me', website: '' });
  });

  it('passes the hidden honeypot field along, so the Worker can drop the bot', async () => {
    send.mockResolvedValue(undefined);
    renderDialog();

    await userEvent.type(messageField(), 'hello');
    await userEvent.type(screen.getByLabelText('Website'), 'spam.example');
    await userEvent.click(sendButton());

    expect(send).toHaveBeenCalledWith(expect.objectContaining({ website: 'spam.example' }));
  });

  it('shows "Sending…" and blocks the button while the request is in flight', async () => {
    let finish!: () => void;
    send.mockReturnValue(new Promise<void>(resolve => (finish = resolve)));
    renderDialog();

    await userEvent.type(messageField(), 'hello');
    await userEvent.click(sendButton());

    expect(screen.getByRole('button', { name: 'Sending…' })).toBeDisabled();

    finish();
    expect(await screen.findByText('Thank you!')).toBeInTheDocument();
  });

  it('thanks the user after a successful send and closes on request', async () => {
    send.mockResolvedValue(undefined);
    const { onClose } = renderDialog();

    await userEvent.type(messageField(), 'hello');
    await userEvent.click(sendButton());

    expect(await screen.findByText('Thank you!')).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Close' }));
    expect(onClose).toHaveBeenCalled();
  });

  it('shows an error and keeps the text when sending fails', async () => {
    send.mockRejectedValue(new FeedbackError(500));
    renderDialog();

    await userEvent.type(messageField(), 'my long text');
    await userEvent.click(sendButton());

    expect(await screen.findByRole('alert')).toHaveTextContent('Could not send. Please try again.');
    expect(messageField()).toHaveValue('my long text');
  });

  it('asks the user to wait when the Worker answers 429', async () => {
    send.mockRejectedValue(new FeedbackError(429));
    renderDialog();

    await userEvent.type(messageField(), 'hello');
    await userEvent.click(sendButton());

    expect(await screen.findByRole('alert')).toHaveTextContent('Too many messages');
  });

  it('closes with Cancel', async () => {
    const { onClose } = renderDialog();
    await userEvent.click(screen.getByRole('button', { name: 'Cancel' }));
    expect(onClose).toHaveBeenCalled();
  });

  it('closes on a click on the backdrop, but not on a click inside', async () => {
    const { onClose } = renderDialog();

    await userEvent.click(messageField());
    expect(onClose).not.toHaveBeenCalled();

    await userEvent.click(screen.getByRole('dialog'));
    expect(onClose).toHaveBeenCalled();
  });
});