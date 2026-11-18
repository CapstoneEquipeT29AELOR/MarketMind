// Thin wrapper around the MarketMind backend described in openapi.yaml.
// Requests go to /api/* and are proxied to the backend by Vite in development.
// Set VITE_API_BASE_URL to call a backend on another origin instead.
const BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/$/, '');

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

// Turns the contract's error shapes ({"error": ...} or FastAPI's 422 {"detail": [...]}) into a message.
function errorMessage(body, status) {
  if (body?.error) return body.error;
  if (Array.isArray(body?.detail)) {
    return body.detail.map((item) => item.msg).filter(Boolean).join('; ') || 'Invalid request';
  }
  if (typeof body?.detail === 'string') return body.detail;
  return `Request failed (${status})`;
}

async function post(path, payload, { signal } = {}) {
  let response;
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal,
    });
  } catch (error) {
    if (error.name === 'AbortError') throw error;
    throw new ApiError('Unable to reach the MarketMind server', 0);
  }

  const body = await response.json().catch(() => null);
  if (!response.ok) throw new ApiError(errorMessage(body, response.status), response.status);
  return body;
}

// Chart timelines accepted by POST /api/stocks/chart.
export const TIMELINES = ['1d', '5d', '1mo', '6mo', '1y', '5y', 'ytd', 'max'];

// Returns an array of matching ticker symbols.
export async function searchStocks(query, options) {
  const result = await post('/api/stocks/search', { query }, options);
  return Array.isArray(result) ? result : [];
}

// Returns closing prices as [{ date, close }] sorted oldest to newest.
export async function getStockChart(symbol, timeline = '5d', options) {
  const result = await post('/api/stocks/chart', { symbol, timeline }, options);
  return Object.entries(result ?? {})
    .filter(([, close]) => typeof close === 'number')
    .map(([date, close]) => ({ date, close }))
    .sort((a, b) => a.date.localeCompare(b.date));
}

// Returns news items: { source, time, category, headline, summary, symbols, tone, url }.
export function getStockNews(symbol, limit = 20, options) {
  return post('/api/stocks/news', { symbol, limit }, options);
}

// Returns { sentiment, score, confidence, summary, factors: [{ label, detail, impact }] }.
export function getStockAnalysis(symbol, options) {
  return post('/api/stocks/analysis', { symbol }, options);
}
