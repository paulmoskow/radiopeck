import { useState } from 'react';
import FeedbackDialog from './FeedbackDialog';

export default function FeedbackButton() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        type="button"
        className="feedback-btn"
        aria-label="Send feedback"
        title="Send feedback"
        onClick={() => setOpen(true)}
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"
             strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z" />
          <path d="M8.5 11.5h7M8.5 14.5h4" />
        </svg>
      </button>
      <FeedbackDialog open={open} onClose={() => setOpen(false)} />
    </>
  );
}