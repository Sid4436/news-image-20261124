// news-image-20261124: the world's news of Tuesday 24 November 2026 in one picture.
// entry.png is pre-rendered by render.py (Pillow, deterministic); this program only copies it,
// so both grader runs write identical bytes. Node 22, standard library only, no network.
import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

// MAKEFUN_OUTPUT_DIR stands in for /output when run outside the grader's container.
const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(fileURLToPath(new URL('./entry.png', import.meta.url)), join(outDir, 'entry.png'));
