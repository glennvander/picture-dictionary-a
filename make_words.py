#!/usr/bin/env python3
"""
Build prompts/words.json from "Revised List.md".

The markdown file is the single source of truth for WHICH words are in the book;
sentences live in the SENTENCES table below and are matched by word. If the list
is revised, re-run this: it reports any word that has no sentence yet and any
sentence left over for a word that has been dropped, so the two can never
silently drift apart.

Run:  python3 make_words.py
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts"))
from scenes import SCENES, NEEDS_TEXT  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Revised List.md")
OUT = os.path.join(HERE, "prompts", "words.json")

# Sentences are short, concrete, and show the word doing real work. A few lean
# deliberately into the school's own context (hearing aids, signing) rather than
# pretending the audience is generic.
SENTENCES = {
    # A
    "accident": "It was an accident. The paint spilled.",
    "add": "Add two and three to get five.",
    "airplane": "The airplane flies above the clouds.",
    "airport": "We waited for our plane at the airport.",
    "angry": "He felt angry when he lost the game.",
    "animal": "A dog is my favorite animal.",
    "apple": "I packed an apple for lunch.",
    "arm": "I raised my arm to answer.",
    "art": "Art class is on Tuesday.",
    "astronaut": "The astronaut floated in space.",
    # B
    "backpack": "I carry my backpack to school.",
    "bake": "We bake bread on Sundays.",
    "balloon": "The red balloon floated away.",
    "baseball": "He hit the baseball over the fence.",
    "basketball": "She plays basketball after school.",
    "beach": "We swam at the beach all day.",
    "bear": "A brown bear walked through the trees.",
    "bike": "I ride my bike to school.",
    "bird": "A small bird landed on the fence.",
    "birthday": "My birthday is in October.",
    "blanket": "I pulled the blanket over my feet.",
    "boat": "The boat crossed the lake.",
    "book": "This book has three hundred pages.",
    "box": "Put the shoes back in the box.",
    "breakfast": "I eat breakfast before school.",
    "brother": "My brother is older than me.",
    # C
    "cake": "She put candles on the cake.",
    "camera": "I took a picture with my camera.",
    "candy": "The candy was too sweet.",
    "chair": "Pull your chair up to the desk.",
    "cheese": "I put cheese on my sandwich.",
    "chicken": "We had chicken for dinner.",
    "chocolate": "Chocolate is my favorite flavor.",
    "city": "The city has tall buildings.",
    "clean": "I clean my room on Saturday.",
    "climb": "We climb the rope in gym.",
    "clock": "The clock says three o'clock.",
    "cloud": "One white cloud crossed the sky.",
    "clown": "The clown made everyone laugh.",
    "coat": "Wear your coat. It is cold.",
    "computer": "I typed my report on the computer.",
    "cook": "My father can cook rice.",
    "cookie": "May I have one cookie?",
    # D
    "dance": "We dance at the school party.",
    "dark": "The hallway was dark at night.",
    "dentist": "The dentist checked my teeth.",
    "desk": "My books are on my desk.",
    "dessert": "We had ice cream for dessert.",
    "dinosaur": "This dinosaur lived long ago.",
    "dirt": "My shoes were covered in dirt.",
    "dish": "I washed every dish.",
    "doctor": "The doctor checked my ears.",
    "doll": "She kept the doll on her shelf.",
    "dollar": "The pencil cost one dollar.",
    "door": "Please close the door.",
    "dragon": "The dragon in the story breathed fire.",
    "draw": "I like to draw animals.",
    "dress": "She wore a blue dress.",
    "drink": "I drink water after I run.",
    "drive": "My mother will drive us home.",
    "drum": "He plays the drum in band.",
    "duck": "A duck swam across the pond.",
    # E
    "ear": "My ear is on the side of my head.",
    "earth": "Earth is the planet we live on.",
    "egg": "I ate one egg for breakfast.",
    "elephant": "The elephant has a long trunk.",
    "exercise": "We exercise in gym class.",
    "eye": "Something got in my eye.",
    # F
    "face": "A big smile filled her face.",
    "family": "My family eats dinner together.",
    "farm": "Cows live on the farm.",
    "farmer": "The farmer drove the tractor.",
    "feet": "My feet hurt after the hike.",
    "fence": "The ball went over the fence.",
    "field": "We played soccer on the field.",
    "finger": "I pointed with one finger.",
    "fire": "The fire kept us warm.",
    "fish": "A silver fish swam past.",
    "flag": "The flag waved in the wind.",
    "floor": "Keep your backpack off the floor.",
    "flower": "One yellow flower opened today.",
    "food": "We packed food for the trip.",
    "forest": "Tall trees filled the forest.",
    # G
    "game": "We won the game by two points.",
    "garden": "Tomatoes grow in our garden.",
    "ghost": "The ghost in the story was friendly.",
    "giant": "The giant was taller than the trees.",
    "gift": "I wrapped the gift in blue paper.",
    "glass": "Pour the milk into a glass.",
    "gold": "The ring is made of gold.",
    "grandfather": "My grandfather taught me to fish.",
    "grandmother": "My grandmother makes the best soup.",
    "grass": "The grass is wet this morning.",
    "gym": "We run laps in the gym.",
    # H
    "hair": "She tied her hair back.",
    "halloween": "We wear costumes on Halloween.",
    "hand": "Raise your hand to answer.",
    "head": "I wore a hat on my head.",
    "heart": "My heart beat fast after running.",
    "help": "Can you help me carry this?",
    "hide": "We hide behind the door.",
    "hill": "We rode our bikes down the hill.",
    "hole": "There is a hole in my sock.",
    "home": "I walk home after school.",
    "horse": "The horse ran across the field.",
    "hospital": "The nurse works at the hospital.",
    "house": "Our house has a red door.",
    "hungry": "I was hungry before lunch.",
    # I
    "ice": "The ice melted in my drink.",
    "ice cream": "We ate ice cream at the park.",
    "island": "The island is surrounded by water.",
    # J
    "jar": "The cookies are in the jar.",
    "juice": "I drink orange juice with breakfast.",
    "jump": "I can jump over the puddle.",
    # K
    "kick": "Kick the ball to me.",
    "king": "The king wore a gold crown.",
    "kiss": "She gave the baby a kiss.",
    "kitchen": "We cook in the kitchen.",
    "kite": "My kite flew above the trees.",
    "kitten": "The kitten fell asleep in my lap.",
    "knee": "I scraped my knee on the sidewalk.",
    "knife": "Cut the bread with a knife.",
    # L
    "ladder": "He climbed the ladder to the roof.",
    "lake": "We swam across the lake.",
    "lamp": "Turn on the lamp so you can read.",
    "laugh": "That joke made me laugh.",
    "leg": "I hurt my leg playing soccer.",
    "letter": "I mailed a letter to my cousin.",
    "library": "I borrowed two books from the library.",
    "light": "The light is too bright.",
    "lion": "The lion has a thick mane.",
    "lock": "Remember to lock your locker.",
    "lunch": "We eat lunch at noon.",
    # M
    "magic": "The card trick looked like magic.",
    "mailman": "The mailman brought a package.",
    "mall": "We met our friends at the mall.",
    "math": "Math is my first class.",
    "meat": "He does not eat meat.",
    "medicine": "I took medicine for my cold.",
    "milk": "I poured milk on my cereal.",
    "money": "I saved money for a new game.",
    "monkey": "The monkey hung from a branch.",
    "monster": "The monster in the movie was not real.",
    "moon": "The moon was full last night.",
    "mother": "My mother drives me to practice.",
    "mountain": "Snow covered the top of the mountain.",
    "mouse": "A small mouse ran under the shelf.",
    "mouth": "Cover your mouth when you cough.",
    "movie": "We watched a movie on Friday.",
    "mud": "My boots were thick with mud.",
    "music": "The band played music at the assembly.",
    # N
    "name": "Write your name at the top.",
    "neck": "I wore a scarf around my neck.",
    "neighbor": "Our neighbor helped us move.",
    "nest": "Three eggs sat in the nest.",
    "night": "The stars come out at night.",
    "nose": "My nose was cold outside.",
    "nurse": "The nurse checked my ear.",
    "nut": "A squirrel buried the nut.",
    # O
    "ocean": "We saw whales in the ocean.",
    "office": "The principal works in the office.",
    "open": "Please open the window.",
    "orange": "I peeled an orange for lunch.",
    "oven": "The bread is in the oven.",
    "outside": "We ate lunch outside today.",
    # P
    "paint": "We paint in art class.",
    "pants": "My pants have deep pockets.",
    "paper": "I need one sheet of paper.",
    "park": "We play basketball at the park.",
    "party": "The party starts at four.",
    "pen": "Sign your name with a pen.",
    "pencil": "My pencil needs sharpening.",
    "phone": "I texted her from my phone.",
    "piano": "She plays the piano every day.",
    "picture": "I drew a picture of my dog.",
    "plant": "The plant needs water.",
    "play": "We play soccer after school.",
    "police": "The police officer helped us cross.",
    "potato": "We baked a potato for dinner.",
    "present": "I opened my present first.",
    "pumpkin": "We carved a pumpkin in October.",
    "puppy": "The puppy chewed my shoe.",
    # Q
    "queen": "The queen waved to the crowd.",
    "quiet": "The library is a quiet place.",
    # R
    "rabbit": "A rabbit hopped across the yard.",
    "rain": "The rain stopped before recess.",
    "rainbow": "A rainbow appeared after the storm.",
    "read": "I read two chapters last night.",
    "rice": "We ate rice with dinner.",
    "ride": "I ride the bus to school.",
    "ring": "She wore a silver ring.",
    "river": "The river runs past our town.",
    "road": "The road turns left at the light.",
    "robot": "Our team built a robot for science class.",
    "rock": "I found a smooth rock by the water.",
    "rocket": "The rocket lifted off.",
    "roof": "Snow covered the roof.",
    "room": "My room is upstairs.",
    "rope": "We climbed the rope in gym.",
    "run": "I run a mile every morning.",
    # S
    "sandwich": "I made a cheese sandwich.",
    "scared": "The dark hallway made me scared.",
    "school": "Our school starts at eight.",
    "science": "We did an experiment in science.",
    "scissors": "Cut the paper with scissors.",
    "shirt": "My shirt has blue stripes.",
    "shoe": "There is a hole in my shoe.",
    "shop": "We shop for groceries on Saturday.",
    "sidewalk": "We walked along the sidewalk.",
    "sing": "We sing at the winter concert.",
    "sister": "My sister is in third grade.",
    "skate": "I skate on the frozen pond.",
    "sleep": "I sleep eight hours a night.",
    "slide": "The little kids went down the slide.",
    "smell": "I smell bread baking.",
    "smile": "A big smile crossed her face.",
    "soap": "Wash your hands with soap.",
    "soccer": "We won our soccer game.",
    "spider": "A spider built a web in the corner.",
    "sport": "Basketball is my favorite sport.",
    "stairs": "We ran up the stairs.",
    "stand": "Please stand for the flag.",
    "star": "One bright star appeared first.",
    "stomach": "My stomach hurt after lunch.",
    "store": "The store closes at nine.",
    "storm": "The storm knocked down a tree.",
    "stove": "The pot is on the stove.",
    "street": "Look both ways before crossing the street.",
    "swim": "I swim laps at the pool.",
    "swing": "She pushed me on the swing.",
    # T
    "table": "We set the table for dinner.",
    "tail": "The dog wagged its tail.",
    "teacher": "My teacher signs very clearly.",
    "teeth": "I brush my teeth twice a day.",
    "tiger": "The tiger has orange stripes.",
    "time": "What time does the bus come?",
    "tired": "I was tired after practice.",
    "tissue": "I need a tissue for my nose.",
    "tongue": "I burned my tongue on the soup.",
    "touch": "Do not touch the wet paint.",
    "town": "Our town has one movie theater.",
    "train": "The train arrives at six.",
    "tree": "We planted a tree at school.",
    "truck": "The truck carried our furniture.",
    "turkey": "We eat turkey in November.",
    "turtle": "The turtle moved slowly.",
    # U
    "uncle": "My uncle taught me to ride.",
    # V
    "vacation": "We go to the beach on vacation.",
    "vegetable": "A carrot is my favorite vegetable.",
    # W
    "walk": "I walk to school with my sister.",
    "wash": "Wash your hands before lunch.",
    "watch": "My watch stopped last night.",
    "water": "I drink water after gym.",
    "wave": "A big wave splashed my legs.",
    "weather": "The weather is warm today.",
    "wet": "My jacket is wet from the rain.",
    "window": "Open the window for fresh air.",
    "winter": "It snows here in winter.",
    "witch": "The witch in the story flew away.",
    "woman": "The woman next door is a nurse.",
    "wood": "The table is made of wood.",
    "work": "My parents work downtown.",
    "write": "Write your answer on the line.",
    # X
    "x-ray": "The x-ray showed a broken bone.",
    "xylophone": "She played the xylophone in music class.",
    # Y
    "yard": "We raked leaves in the yard.",
    "yawn": "A long yawn made my eyes water.",
    "yellow": "The school bus is yellow.",
    "young": "My cousin is too young for school.",
    # Z
    "zoo": "We saw elephants at the zoo.",
}


def parse(path):
    """Read the markdown list into {letter: [words]} preserving her order."""
    letters, cur = {}, None
    for raw in open(path, encoding="utf-8"):
        t = raw.strip().lstrip("#").strip().strip("*").strip()
        if not t:
            continue
        m = re.fullmatch(r"Letter ([A-Z])", t)
        if m:
            cur = m.group(1)
            letters[cur] = []
            continue
        if cur is None:
            continue
        if t.lower().startswith("(optional"):
            inner = re.search(r":(.*)\)", t)
            if inner:
                t = inner.group(1)
            else:
                continue
        for w in t.split(","):
            w = w.strip().rstrip(".").strip()
            if w:
                letters[cur].append(w)
    return letters


def main():
    letters = parse(SRC)
    entries, missing = [], []
    for L in sorted(letters):
        for w in letters[L]:
            key = w.lower()
            s = SENTENCES.get(key)
            if not s:
                missing.append(w)
                s = ""
            entries.append({"word": w.lower(), "letter": L, "sentence": s,
                            "scene": SCENES.get(key, ""),
                            "needs_text": key in NEEDS_TEXT})

    used = {e["word"] for e in entries}
    orphans = sorted(set(SENTENCES) - used)
    no_scene = [e["word"] for e in entries if not e["scene"]]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({
            "_meta": {
                "source": "Revised List.md (teacher-selected list)",
                "count": len(entries),
                "letters": {L: len(v) for L, v in sorted(letters.items())},
                "audience": "Middle school, Lake Drive School",
            },
            "words": entries,
        }, f, indent=1, ensure_ascii=False)

    print(f"{len(entries)} words across {len(letters)} letters -> {OUT}")
    print(f"missing sentences: {len(missing)}"
          + (f" -> {', '.join(missing)}" if missing else " (none)"))
    print(f"orphaned sentences: {len(orphans)}"
          + (f" -> {', '.join(orphans)}" if orphans else " (none)"))
    print(f"missing scenes: {len(no_scene)}"
          + (f" -> {', '.join(no_scene)}" if no_scene else " (none)"))


if __name__ == "__main__":
    main()
