export const FEEDBACK_URL = 'https://radiopeck.pavel-moskov.workers.dev';

export type FeedbackInput = { message: string; contact?: string; website?: string };

export class FeedbackError extends Error {
  status: number;

  constructor(status: number) {
    super(`Feedback request failed: ${status}`);
    this.name = 'FeedbackError';
    this.status = status;
  }
}

export async function sendFeedback(input: FeedbackInput): Promise<void> {
  const response = await fetch(FEEDBACK_URL, { 
    method: 'POST', 
    headers: { 'Content-Type': 'application/json' }, 
    body: JSON.stringify({
      message: input.message.trim(),
      contact: input.contact?.trim() ?? '',
      website: input.website ?? '',
    }) 
  });

  if (!response.ok) throw new FeedbackError(response.status);

}