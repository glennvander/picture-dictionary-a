(function(root){
'use strict';
/* ---------------------------------------------------------------------------
   Paper-peel page turn.

   The previous version rotated each page as a rigid plane on a hinge, which
   reads as a card flipping rather than paper moving. Real paper folds: when
   you drag a corner, the sheet creases along the perpendicular bisector of the
   line from the corner's home position to your finger, and everything past
   that crease reflects over and shows the reverse of the sheet.

   That is what this implements, in page-local coordinates:

       S = spine-side corner        C0 = grabbed corner's home position
       P = where the corner is now  M  = midpoint of C0->P
       n = unit vector along C0->P  (the fold line's normal)

   fold line  : points p where (p - M)·n = 0
   still flat : (p - M)·n >= 0      -> front of the sheet, unmoved
   folded flap: (p - M)·n <= 0      -> reflected across the fold, shows the back

   Paper does not stretch, so P is constrained to |P - S| <= W.
--------------------------------------------------------------------------- */

function reflection(M, n){
  // p' = p - 2((p-M)·n) n   as a CSS matrix(a,b,c,d,e,f)
  const k = 2*(M.x*n.x + M.y*n.y);
  return {
    a: 1 - 2*n.x*n.x, b: -2*n.x*n.y,
    c: -2*n.x*n.y,    d: 1 - 2*n.y*n.y,
    e: k*n.x,         f: k*n.y
  };
}

const css = m => `matrix(${m.a},${m.b},${m.c},${m.d},${m.e},${m.f})`;

/* Sutherland-Hodgman: clip a polygon to the half-plane (p - M)·n >= 0 */
function clipHalfPlane(poly, M, n){
  const side = p => (p.x - M.x)*n.x + (p.y - M.y)*n.y;
  const out = [];
  for (let i=0;i<poly.length;i++){
    const A = poly[i], B = poly[(i+1)%poly.length];
    const sa = side(A), sb = side(B);
    if (sa >= 0) out.push(A);
    if ((sa >= 0) !== (sb >= 0)){
      const t = sa / (sa - sb);
      out.push({ x: A.x + t*(B.x - A.x), y: A.y + t*(B.y - A.y) });
    }
  }
  return out;
}

const polyToClip = pts =>
  pts.length < 3 ? 'polygon(0 0,0 0,0 0)'
  : 'polygon(' + pts.map(p=>`${p.x.toFixed(2)}px ${p.y.toFixed(2)}px`).join(',') + ')';

/* Constrain the dragged corner so the sheet cannot stretch. */
function constrain(P, S, W){
  const dx = P.x - S.x, dy = P.y - S.y;
  const len = Math.hypot(dx, dy);
  if (len <= W || len === 0) return P;
  return { x: S.x + dx*W/len, y: S.y + dy*W/len };
}

/* Full geometry for one frame of a peel. */
function foldGeometry(P, C0, S, W, H){
  P = constrain(P, S, W);
  const d = { x: P.x - C0.x, y: P.y - C0.y };
  const len = Math.hypot(d.x, d.y) || 1e-6;
  const n = { x: d.x/len, y: d.y/len };
  const M = { x: (C0.x + P.x)/2, y: (C0.y + P.y)/2 };

  const sheet = [{x:0,y:0},{x:W,y:0},{x:W,y:H},{x:0,y:H}];
  const flat  = clipHalfPlane(sheet, M, n);
  const flap  = clipHalfPlane(sheet, M, {x:-n.x, y:-n.y});

  // The flap element spans the sheet in page coordinates and mirrors only its
  // *content* (an inner wrapper flips the image, so the reverse of the sheet
  // reads correctly). The clip therefore stays in plain page coordinates —
  // mirroring it too clips the wrong half and throws the flap off the page.
  return {
    P, M, n,
    flatClip: polyToClip(flat),
    flapClip: polyToClip(flap),
    matrix: css(reflection(M, n)),
    // 0 = untouched, 1 = fully turned
    progress: Math.min(1, Math.max(0, (C0.x - P.x) / (2*W))),
    foldAngle: Math.atan2(n.y, n.x)
  };
}

  const Peel = { reflection, css, clipHalfPlane, polyToClip, constrain, foldGeometry };
  root.Peel = Peel;
  if (typeof module !== 'undefined' && module.exports) module.exports = Peel;
})(typeof self !== 'undefined' ? self : globalThis);
