import { useEffect, useRef, useState } from 'react';
import type { SyntheticEvent } from 'react';
import { FeedbackError, sendFeedback } from '../lib/feedback';

const MAX_MESSAGE = 2000;

type Status = 'idle' | 'sending' | 'sent' | 'error';

type FeedbackDialogProps = {
  open: boolean;
  onClose: () => void;
};

export default function FeedbackDialog({ open, onClose }: FeedbackDialogProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const [message, setMessage] = useState('');
  const [contact, setContact] = useState('');
  const [website, setWebsite] = useState(''); // trap for bots as users don't see this field
  const [status, setStatus] = useState<Status>('idle');
  const [errorText, setErrorText] = useState('');

  // The browser owns the dialog's open state; keep it in step with the prop
  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (open && !dialog.open) dialog.showModal();
    if (!open && dialog.open) dialog.close();
  }, [open]);

  // Fires on Esc and on dialog.close(): tell the parent and forget the "thank you" view
  function handleClosed() {
    setStatus(s => (s === 'sent' ? 'idle' : s));
    onClose();
  }

  const canSend = message.trim().length > 0 && status !== 'sending';

  async function handleSubmit(e: SyntheticEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!canSend) return;
    setStatus('sending');
    try {
      await sendFeedback({ message, contact, website });
      setMessage('');
      setContact('');
      setStatus('sent');
    } catch (err) {
      setErrorText(
        err instanceof FeedbackError && err.status === 429
          ? 'Too many messages. Please wait a minute and try again.'
          : 'Could not send. Please try again.',
      );
      setStatus('error');
    }
  }

  return (
    <dialog
      ref={dialogRef}
      className="feedback"
      aria-labelledby="feedback-title"
      onClose={handleClosed}
      onClick={e => {
        // A click on the dimmed backdrop lands on the <dialog> itself
        if (e.target === e.currentTarget) onClose();
      }}
    >
      {status === 'sent' ? (
        <div className="feedback__form">
          <h2 id="feedback-title" className="feedback__title">
            Thank you!
          </h2>
          <p className="feedback__status" role="status">
            Your message was sent.
          </p>
          <div className="feedback__actions">
            <button type="button" className="feedback__btn feedback__btn--primary" onClick={onClose}>
              Close
            </button>
          </div>
        </div>
      ) : (
        <form className="feedback__form" onSubmit={handleSubmit}>
          <h2 id="feedback-title" className="feedback__title">
            Feedback
          </h2>

          <div className="feedback__field">
            <label htmlFor="feedback-message">Your message</label>
            <textarea
              id="feedback-message"
              className="feedback__textarea"
              value={message}
              maxLength={MAX_MESSAGE}
              placeholder="Suggestions, complaints, anything you want to tell"
              onChange={e => setMessage(e.target.value)}
            />
            <span className="feedback__count">
              {message.length} / {MAX_MESSAGE}
            </span>
          </div>

          <div className="feedback__field">
            <label htmlFor="feedback-contact">Contact (optional)</label>
            <input
              id="feedback-contact"
              className="feedback__input"
              type="text"
              value={contact}
              maxLength={200}
              placeholder="Email or Telegram, if you want an answer"
              onChange={e => setContact(e.target.value)}
            />
          </div>

          {/* hidden from people, filled in by simple bots */}
          <div className="sr-only" aria-hidden="true">
            <label htmlFor="feedback-website">Website</label>
            <input
              id="feedback-website"
              type="text"
              tabIndex={-1}
              autoComplete="off"
              value={website}
              onChange={e => setWebsite(e.target.value)}
            />
          </div>

          <p
            className={status === 'error' ? 'feedback__status feedback__status--error' : 'feedback__status'}
            role={status === 'error' ? 'alert' : undefined}
          >
            {status === 'error' && errorText}
          </p>

          <div className="feedback__actions">
            <button type="button" className="feedback__btn" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="feedback__btn feedback__btn--primary" disabled={!canSend}>
              {status === 'sending' ? 'Sending…' : 'Send'}
            </button>
          </div>
        </form>
      )}
    </dialog>
  );
}