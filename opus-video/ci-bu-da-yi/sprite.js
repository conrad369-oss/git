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
function drawSprite(ctx, pose, x, y, cell, col = '#F0AA5A', eye = '#2A1E14', flip = false, glow = 0) {
  const rows = SPRITE[pose] || SPRITE.stand, x0 = Math.round(x - SPRITE_W * cell / 2), y0 = Math.round(y - (SPRITE_H - 1) * cell);
  ctx.save();
  if (glow) { ctx.shadowColor = 'rgba(240,170,90,.85)'; ctx.shadowBlur = glow; }
  for (let r = 0; r < SPRITE_H; r++) for (let c = 0; c < SPRITE_W; c++) {
    const ch = rows[r][flip ? SPRITE_W - 1 - c : c]; if (ch === '.') continue;
    ctx.fillStyle = ch === 'o' ? eye : col; ctx.fillRect(x0 + c * cell, y0 + r * cell, cell, cell);
  }
  ctx.restore();
}
// walking pose at 6 steps/second (quantised like real pixel animation)
const walkPose = t => (Math.floor(t * 6) % 2 ? 'walk0' : 'walk1');
