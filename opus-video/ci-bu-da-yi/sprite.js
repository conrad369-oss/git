// "我": a small warm pixel creature (blocky body, two eyes, stubby arms, four short legs).
// Drawn cell by cell so it always stays crisp pixel art, whatever the world around it looks like.
// Grid is 14 wide x 11 tall; (0,0) top-left. Each pose is a list of strings: '#' body, 'o' eye, '.' empty.
const SPRITE = {
  stand: [
    '..##########..',
    '..##########..',
    '..##o####o##..',
    '..##o####o##..',
    '##############',
    '##############',
    '..##########..',
    '..##########..',
    '...#.#..#.#...',
    '...#.#..#.#...',
    '..............'],
  walk0: [
    '..##########..',
    '..##########..',
    '..###o####o#..',
    '..###o####o#..',
    '##############',
    '##############',
    '..##########..',
    '..##########..',
    '..#..#..#..#..',
    '.#..#....#..#.',
    '..............'],
  walk1: [
    '..##########..',
    '..##########..',
    '..###o####o#..',
    '..###o####o#..',
    '##############',
    '##############',
    '..##########..',
    '..##########..',
    '...#.#..#.#...',
    '...#.#..#.#...',
    '..............'],
  reach: [ // right arm raised (touching the glass / writing)
    '..##########.#',
    '..##########.#',
    '..###o####o###',
    '..###o####o###',
    '############..',
    '############..',
    '..##########..',
    '..##########..',
    '...#.#..#.#...',
    '...#.#..#.#...',
    '..............'],
  lookup: [
    '..##o####o##..',
    '..##o####o##..',
    '..##########..',
    '..##########..',
    '##############',
    '##############',
    '..##########..',
    '..##########..',
    '...#.#..#.#...',
    '...#.#..#.#...',
    '..............'],
  lookdown: [
    '..##########..',
    '..##########..',
    '..##########..',
    '..##o####o##..',
    '####o####o####',
    '##############',
    '..##########..',
    '..##########..',
    '...#.#..#.#...',
    '...#.#..#.#...',
    '..............'],
  sleep: [
    '..............',
    '..............',
    '..............',
    '..##########..',
    '..##########..',
    '..##########..',
    '..#oo####oo#..',
    '##############',
    '##############',
    '.############.',
    '..............'],
  sit: [
    '..............',
    '..............',
    '..##########..',
    '..##########..',
    '..##o####o##..',
    '..##o####o##..',
    '##############',
    '##############',
    '..##########..',
    '.##.#....#.##.',
    '..............'],
};
const SPRITE_W = 14, SPRITE_H = 11;
// draw with feet at (x, y) bottom-centre; cell = pixel size; flip = face left
// each (pose, size, colour, glow) is rasterised once into a cache canvas: identical pixels every frame, much faster
const SPRITE_CACHE = {};
function spriteImage(pose, cell, col, eye, flip, glow) {
  const key = [pose, cell, col, eye, flip, glow].join('|'); if (SPRITE_CACHE[key]) return SPRITE_CACHE[key];
  const pad = glow * 2, cv = document.createElement('canvas'); cv.width = SPRITE_W * cell + pad * 2; cv.height = SPRITE_H * cell + pad * 2;
  const x = cv.getContext('2d'), rows = SPRITE[pose] || SPRITE.stand;
  if (glow) { x.shadowColor = 'rgba(240,170,90,.85)'; x.shadowBlur = glow; }
  for (let r = 0; r < SPRITE_H; r++) for (let c = 0; c < SPRITE_W; c++) {
    const ch = rows[r][flip ? SPRITE_W - 1 - c : c]; if (ch === '.') continue;
    x.fillStyle = ch === 'o' ? eye : col; x.fillRect(pad + c * cell, pad + r * cell, cell, cell);
  }
  return (SPRITE_CACHE[key] = { cv, pad });
}
function drawSprite(ctx, pose, x, y, cell, col = '#F0AA5A', eye = '#2A1E14', flip = false, glow = 0) {
  const im = spriteImage(pose, cell, col, eye, flip, glow), x0 = Math.round(x - SPRITE_W * cell / 2), y0 = Math.round(y - (SPRITE_H - 1) * cell);
  ctx.drawImage(im.cv, x0 - im.pad, y0 - im.pad);
}
// walking pose at 6 steps/second (quantised like real pixel animation)
const walkPose = t => (Math.floor(t * 6) % 2 ? 'walk0' : 'walk1');
