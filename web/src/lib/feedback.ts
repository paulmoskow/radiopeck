export const FEEDBACK_URL = 'https://radiopeck.pavel-moskov.workers.dev';

export type FeedbackInput = { message: string; contact?: string; website?: string };

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

  if (!response.ok) throw new Error(`Feedback request failed: ${response.status}`);

}