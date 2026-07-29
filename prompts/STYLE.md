# Locked illustration style — Lake Drive Picture Dictionary (Letter A)

Derived from research on visual design for Deaf and hard-of-hearing learners.
Every image in the book uses the identical style block so the set reads as one
system. Do not edit these strings mid-run — consistency depends on them being
byte-identical across all 73 generations.

## Why this style

- DHH students are **sequential, single-channel** visual processors: they cannot
  watch a signer and study an image at the same time. Every picture must be
  readable in one glance, so: one subject, no visual search, no clutter.
- Mayer's **coherence principle** — extraneous detail measurably reduces
  learning (23/23 experiments, median effect size 0.86). Decorative background
  is not neutral; it is a cost.
- **DeafSpace "Light and Color"**: matte, high-contrast, glare-free surfaces;
  colour chosen to contrast against skin tone so faces and hands read clearly.
- **Anti-infantilization.** Picture-supported vocabulary material is
  overwhelmingly authored for K-4. Middle schoolers handed babyish materials
  disengage. Realistic teen proportions, contemporary clothing, restrained
  palette — an editorial register, not a storybook one.
- **Flat vector is also the most reproducible style** run-to-run, which is the
  practical constraint across 73 generations.

## Hard rule: no AI-generated signs

No image may depict ASL signs or fingerspelling. AI renders handshapes
unreliably and omits non-manual markers, which carry grammar. An inaccurate
handshape in a dictionary published under a Deaf school's name is a wrong
definition, not a cosmetic flaw. Characters appear in natural postures with
hands visible; pointing and hand-raising are fine, signing is not.

## STYLE BLOCK — appended verbatim to every prompt

> Flat modern vector cartoon illustration, clean editorial style for middle
> school students. Uniform charcoal #1F2933 outlines of even weight, flat fills
> with one darker flat shade step; no gradients, no texture, no cast shadows.
> Colorblind-safe palette only: #0072B2 blue, #56B4E9 sky blue, #009E73 green,
> #E69F00 orange, #D55E00 vermillion, #CC79A7 pink, maximum five hues plus
> natural skin and hair tones. Plain flat #EAF0F6 pale blue-gray background,
> no scenery, no extra props, no borders. Single clear subject centered in a
> square frame at eye level filling about 70 percent of the frame with clear
> margins. Realistic teen proportions, not chibi. Faces and both hands fully
> visible, natural expression, high figure-ground contrast.

## NEGATIVE BLOCK — appended verbatim to every prompt

> Do not include any written words, letters, numbers, labels, captions,
> watermarks or signatures anywhere in the image. No gradients, glows, drop
> shadows, 3D rendering, watercolor or pencil texture. No busy or detailed
> background. No chibi or big-head proportions. No sign language or
> fingerspelling handshapes. No deformed hands or extra fingers. No cropped or
> hidden hands. No exaggerated shocked or goofy expressions. No clip-art
> borders or frames.

## Text exception

Seven words cannot be defined without legible text or symbols on an object in
the scene: **add, addition, address, am, April, August, arithmetic**. For these
the negative block's first sentence is replaced with:

> The only text in the image is the specific text described above, rendered
> clearly and correctly spelled. No other words, labels, watermarks or
> signatures anywhere.

Plain symbols (+ − × ÷ = ✓ ✗ ? and location pins) are permitted in any image;
they are not text.

## Generation settings

- Model: `nano_banana_2` (Higgsfield MCP)
- Aspect ratio: `1:1`
- Resolution: `2k`
- Cost: 2 credits per image

## Page palette (school brand, page furniture only — never inside artwork)

| Role | Hex | Source |
|---|---|---|
| Primary royal blue | `#1338BE` | `--primary-color`, ld.mlschools.org |
| Accent orange | `#FF6831` | `--secondary-color` |
| Body ink | `#242424` | theme neutral |
| Secondary text | `#636363` | theme neutral |
| Illustration field | `#EAF0F6` | matches image background |

Tagline: *Individual Child, Individual Potential*
