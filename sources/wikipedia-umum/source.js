const API = "https://en.wikipedia.org/w/api.php";

function fail(code, message) {
  const error = new Error(message);
  error.code = code;
  return error;
}

async function get(params) {
  const url = API + "?" + params + "&format=json&origin=*";
  let response;
  try {
    response = await fetch(url);
  } catch (e) {
    throw fail("NETWORK", "Gagal menghubungi Wikipedia: " + e);
  }
  if (!response.ok) throw fail("NETWORK", "HTTP " + response.status);
  try {
    return await response.json();
  } catch (e) {
    throw fail("PARSE", "Respons bukan JSON: " + e);
  }
}

function toEntry(page) {
  return { id: String(page.pageid || page.id || page.title), title: page.title };
}

export default {
  async search(query, page) {
    const data = await get("action=query&list=search&srsearch=" + encodeURIComponent(query) +
      "&srlimit=10&format=json");
    const results = (data.query && data.query.search) || [];
    return {
      entries: results.map(toEntry),
      hasMore: Boolean(data.continue)
    };
  },

  async latest(page) {
    const data = await get("action=query&list=random&rnnamespace=0&rnlimit=10");
    const results = (data.query && data.query.random) || [];
    return {
      entries: results.map(toEntry),
      hasMore: false
    };
  },

  async entry(entryId) {
    const data = await get("action=query&pageids=" + encodeURIComponent(entryId) +
      "&prop=extracts&exintro=1&explaintext=1");
    const pages = (data.query && data.query.pages) || {};
    const page = pages[entryId];
    if (!page) throw fail("NOT_FOUND", "Entri tidak ditemukan: " + entryId);
    return {
      id: String(page.pageid),
      title: page.title,
      status: "tamat",
      description: (page.extract || "").slice(0, 500)
    };
  },

  async units(entryId) {
    await this.entry(entryId);
    return [{ id: "unit-1", number: 1, title: "Artikel", kind: "article" }];
  },

  async open(entryId, unitId) {
    const data = await get("action=query&pageids=" + encodeURIComponent(entryId) +
      "&prop=extracts&explaintext=1");
    const pages = (data.query && data.query.pages) || {};
    const page = pages[entryId];
    if (!page) throw fail("NOT_FOUND", "Artikel tidak ditemukan: " + entryId);
    return { article: { text: page.extract || "" } };
  }
};
