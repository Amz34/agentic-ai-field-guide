// AZ Notion Lead Proxy — silently appends website lead emails to the master Notion DB.
// POST /lead  {email, source?, page?}   ->  201 created | 200 ok | 400 invalid | 503 not configured
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const cors = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    if (request.method === 'OPTIONS') return new Response('ok', { headers: cors });

    if (request.method !== 'POST' || url.pathname !== '/lead') {
      return json({ ok: false, reason: 'not-found' }, 404, cors);
    }

    let body;
    try { body = await request.json(); } catch { return json({ ok: false, reason: 'bad-json' }, 400, cors); }

    const email = String(body.email || '').trim().toLowerCase();
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      return json({ ok: false, reason: 'bad-email' }, 400, cors);
    }
    const source = String(body.source || 'website').slice(0, 80);
    const page = String(body.page || '').slice(0, 120);

    if (!env.NOTION_TOKEN || !env.NOTION_DB_ID) {
      return json({ ok: false, reason: 'not-configured' }, 503, cors); // silent — email flow unaffected
    }

    const resp = await fetch('https://api.notion.com/v1/pages', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + env.NOTION_TOKEN,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        parent: { database_id: env.NOTION_DB_ID },
        properties: {
          'Email': { title: [{ text: { content: email } }] },
          'Source': source ? { select: { name: source } } : undefined,
          'Page': page ? { select: { name: page } } : undefined,
          'Status': { select: { name: 'New' } },
        },
      }),
    });
    if (!resp.ok) {
      const t = await resp.text();
      return json({ ok: false, reason: 'notion-error', detail: t.slice(0, 200) }, 502, cors);
    }
    return json({ ok: true }, 201, cors);
  },
};

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json', ...cors },
  });
}
