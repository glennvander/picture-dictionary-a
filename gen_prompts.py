#!/usr/bin/env python3
"""
Emit ready-to-send image prompts for words that have no illustration yet.

    python3 gen_prompts.py [batch_size]

Prints JSON so the prompts are copied verbatim into the generation call rather
than retyped — consistency across 255 images depends on the style block being
byte-identical every time, and retyping it is how drift creeps in.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(HERE, "images")

# Style is described in full on every prompt rather than anchored to a
# reference image. A reference was tried and reverted: on a single test it
# matched beautifully, but across a batch the exemplar's *content* bled through
# — four of eleven images inherited the wooden board the reference apple was
# sitting on, and the palette drifted to black on one. Verbose prompts cost
# tokens; a contaminated reference costs the whole set.
STYLE = (
    "Flat modern vector cartoon for a school picture dictionary. BOLD uniform "
    "charcoal #1F2933 outlines of even weight on every shape. Flat fills plus "
    "one darker flat step; no gradients, texture or cast shadows. "
    "Colorblind-safe palette only: #0072B2 blue, #56B4E9 sky blue, #009E73 "
    "green, #E69F00 orange, #D55E00 vermillion, #CC79A7 pink, plus natural "
    "skin and hair tones. Plain flat #EAF0F6 pale blue-gray background filling "
    "the whole square edge to edge — never a smaller framed panel or border "
    "inside the square. Subject centered at eye level filling about 70 percent "
    "of the frame. Realistic teen proportions, not chibi. Faces and hands fully "
    "visible, natural expression, high figure-ground contrast."
)

NEG_COMMON = (
    "No gradients, glow, drop shadow, 3D render or watercolor texture. No busy "
    "background. No chibi or big-head proportions. No sign language or "
    "fingerspelling handshapes. No deformed hands or extra fingers. No "
    "exaggerated shocked or goofy expressions. No clip-art borders. Do not "
    "place the subject on a wooden board or tray unless described."
)
NEG_NO_TEXT = ("No text, letters, numbers, labels, watermarks or signatures "
               "anywhere in the image. " + NEG_COMMON)
NEG_WITH_TEXT = ("The only text is the specific text described above, spelled "
                 "correctly. No other words, labels, watermarks or signatures. "
                 + NEG_COMMON)


def slugify(w):
    return w.replace(" ", "_").replace("'", "").lower()


def has_image(slug):
    return any(os.path.exists(os.path.join(IMG_DIR, slug + e))
               for e in (".png", ".jpg"))


def prompt_for(entry):
    neg = NEG_WITH_TEXT if entry.get("needs_text") else NEG_NO_TEXT
    return (f'Educational picture-dictionary illustration for the word '
            f'"{entry["word"]}". {entry["scene"]}. {STYLE} {neg}')


def request_for(i, entry):
    return {"index": i, "word": entry["word"], "params": {
        "model": "nano_banana_2", "aspect_ratio": "1:1", "resolution": "1k",
        "prompt": prompt_for(entry)}}


def main():
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    entries = json.load(open(os.path.join(HERE, "prompts", "words.json")))["words"]
    todo = [e for e in entries if not has_image(slugify(e["word"]))]

    batch = todo[:size]
    out = [request_for(i, e) for i, e in enumerate(batch)]
    print(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"\n# {len(todo)} words still need an image; showing {len(batch)}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
