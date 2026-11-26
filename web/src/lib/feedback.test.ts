import { describe, expect, it, vi, afterEach } from 'vitest';
import { FEEDBACK_URL, sendFeedback } from './feedback';

//prevent  fetch stub leaks into the next test
afterEach(() => {
  vi.restoreAllMocks();
});

describe('sendFeedback', () => {
  it('posts the trimmed message as JSON', async () => {
    const fetchMock = vi
      .spyOn(globalThis, 'fetch')
      .mockResolvedValue(new Response('{"ok":true}', { status: 200 }));

    await sendFeedback({ message: ' hello ', contact: ' tel 000666 '});
    
    const [url, options] = fetchMock.mock.calls[0];

    expect(url).toBe(FEEDBACK_URL);
    expect(options?.method).toBe('POST');
    expect(JSON.parse(options?.body as string)).toEqual({
      message: 'hello',
      contact: 'tel 000666',
      website: '',
    });
  })

  it('sends an empty contact when none is given', async () => {
    const fetchMock = vi
      .spyOn(globalThis, 'fetch')
      .mockResolvedValue(new Response('{"ok":true}', { status: 200 }));

    await sendFeedback({ message: 'hello' });

    const [, options] = fetchMock.mock.calls[0];
    expect(JSON.parse(options?.body as string).contact).toBe('');
  });

  it('resolves quietly when the server answers 200', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response('{"ok":true}', { status: 200 }),
    );

    await expect(sendFeedback({ message: 'hello' })).resolves.toBeUndefined();
  });

  it('throws with the status code when the server answers with an error', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response('', { status: 500 }));

    await expect(sendFeedback({ message: 'hello' })).rejects.toThrow('500');
  });

  it('passes a network error on to the caller', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new TypeError('Failed to fetch'));

    await expect(sendFeedback({ message: 'hello' })).rejects.toThrow('Failed to fetch');
  });

});

