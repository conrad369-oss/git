// Shared, time-only helpers. Nothing here keeps state between frames.
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, k) => a + (b - a) * k;
const smooth = (a, b, x) => { const k = clamp((x - a) / (b - a)); return k * k * (3 - 2 * k); };
const easeInOut = k => (k = clamp(k), k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
const easeOut = k => 1 - Math.pow(1 - clamp(k), 3);
function spring(x, w = 15, z = 0.72) {
  if (x <= 0) return 0;
  const wd = w * Math.sqrt(1 - z * z);
  return 1 - Math.exp(-z * w * x) * (Math.cos(wd * x) + (z * w / wd) * Math.sin(wd * x));
}
// spring tiers (craft-rules): ui = fast, card = default, type = heavy, toy = bouncy
const SP = { ui: [24, 0.8], card: [15, 0.72], type: [10, 0.9], toy: [18, 0.45] };
const sp = (x, tier = 'card') => spring(x, ...SP[tier]);
function rnd(seed) { const s = Math.sin(seed * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); }
const $ = id => document.getElementById(id);
function css(el, o) { for (const k in o) el.style[k] = o[k]; }
// Wait for every font face the page uses, for the given text, then render frame 0.
function boot(faces, text) {
  window.ready = false;
  Promise.all(faces.map(f => document.fonts.load(f, text))).then(() => document.fonts.ready)
    .then(() => { window.render(0); window.ready = true; });
}
