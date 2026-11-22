// Loka Source Plugin template (apiVersion 1). See docs/SOURCE_PLUGIN_SPEC.md.
const BASE = 'https://komik.example.org';

class SourceError extends Error {
  constructor(code, message) {
    super(message);
    this.name = 'SourceError';
    this.code = code;
  }
}

async function getHtml(path) {
  let res;
  try {
    res = await fetch(BASE + path, { credentials: 'include' });
  } catch (err) {
    throw new SourceError('NETWORK', String(err));
  }
  if (res.status === 404) throw new SourceError('NOT_FOUND', path);
  if (res.status === 401) throw new SourceError('NEEDS_LOGIN', path);
  if (res.status === 403 || res.status === 503) {
    // Challenge page: never bypass. The user completes it in a browser tab.
    throw new SourceError('NEEDS_VERIFICATION', path);
  }
  if (!res.ok) throw new SourceError('NETWORK', `HTTP ${res.status}`);
  return res.text();
}

function parseOrFail(value, what) {
  if (value == null) throw new SourceError('PARSE', `missing ${what}`);
  return value;
}

export default {
  async search(query, page = 1) {
    const html = await getHtml(`/search?q=${encodeURIComponent(query)}&page=${page}`);
    const entries = []; // TODO: parse `html` into [{ id, title, cover, status }]
    return { entries, hasMore: false };
  },

  async entry(entryId) {
    const html = await getHtml(`/title/${encodeURIComponent(entryId)}`);
    return {
      id: entryId,
      title: parseOrFail(null, 'title'), // TODO: parse from `html`
      status: 'berlangsung', // or 'tamat'
    };
  },

  async units(entryId) {
    const html = await getHtml(`/title/${encodeURIComponent(entryId)}/chapters`);
    // The unit id must be stable (e.g. the site's chapter slug), never an index or a timestamp.
    return []; // TODO: [{ id, number, title, date, kind: 'pages' }]
  },

  async open(entryId, unitId) {
    const html = await getHtml(`/read/${encodeURIComponent(entryId)}/${encodeURIComponent(unitId)}`);
    return { pages: [] }; // TODO: absolute image URLs under `hosts`
  },
};
