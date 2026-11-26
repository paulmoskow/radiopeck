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
        <svg viewBox="0 0 48 46" aria-hidden="true">
          <path d="M15 31c-5 0-9-3.6-9-8.2 0-4 3-7.2 7-8C14 9.6 18.5 6 24 6c5.6 0 10 3.6 11 8.6 4.3.4 7 3.6 7 7.6 0 4.6-3.8 8.8-9 8.8z" />
          <circle cx="11" cy="37" r="2.6" />
          <circle cx="6" cy="42.5" r="1.5" />
          <g className="feedback-btn__dots">
            <circle cx="17" cy="19" r="1.3" />
            <circle cx="24" cy="19" r="1.3" />
            <circle cx="31" cy="19" r="1.3" />
          </g>
        </svg>
      </button>
      <FeedbackDialog open={open} onClose={() => setOpen(false)} />
    </>
  );
}