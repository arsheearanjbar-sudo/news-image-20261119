// news-image-20261119: the entry is a single image, entry.png, drawn by
// code (see make_image.py). This program copies it to the output directory.
// Node 22, standard library only. No TypeScript-only syntax is used, so the
// file also runs as plain JavaScript.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
