"""
What each word's picture actually shows.

One concrete scene per word. These are deliberately specific: a generic prompt
like "a picture of a bike" produces a generic picture, and the whole point of
the locked style is that 255 images look like one book rather than 255 separate
guesses.

Rules followed throughout, from prompts/STYLE.md:
  - one subject, centred, readable in a single glance
  - people are middle-school aged unless the word requires an adult
  - hands and faces visible, never mid-sign — no ASL, no fingerspelling
  - no text in the image except where the word cannot be shown without it
"""

# Words whose meaning genuinely needs legible text or symbols in the picture.
NEEDS_TEXT = {"name", "math", "time", "dollar"}

SCENES = {
    # A
    "accident": "a tipped-over paint can spreading a blue puddle on the floor, a student beside it with both hands raised in surprise",
    "add": "a student at a whiteboard writing the equation 2 + 3 = 5, pointing at the plus sign",
    "airplane": "a passenger airplane in flight, side three-quarter view, a few rounded clouds below",
    "airport": "an airport terminal with tall windows, two airplanes at the gates outside, a traveller with a rolling suitcase",
    "angry": "a teenager with arms tightly crossed, eyebrows down, two small flat steam puffs at the sides of the head",
    "animal": "four friendly animals together on grass: a dog, a rabbit, a turtle and a small bird",
    "apple": "a single bright red apple with a green leaf on its stem, on a wooden desktop",
    # Now an isolated limb, like `ear`, `head` and `leg`. The hand must stay
    # loose and shapeless: a deliberate handshape here would read as a sign.
    "arm": "one single arm by itself from shoulder to fingertips, held out straight across the picture, the hand relaxed with fingers loosely apart and making no deliberate shape, no body and no head",
    "art": "a wooden easel holding a colourful painting, with a paint palette and brushes in a jar beside it",
    "astronaut": "an astronaut in a white spacesuit with a round helmet, floating, a few flat stars and a blue planet arc behind",
    # B
    "backpack": "a single school backpack standing upright and zipped, one side pocket holding a water bottle",
    "bake": "a teenager in oven mitts sliding a tray of bread rolls into an open oven",
    "balloon": "a single bright red balloon on a string, floating upward",
    "baseball": "a white baseball with red stitching resting beside a wooden bat",
    "basketball": "a teenager mid-jump shooting an orange basketball toward a hoop",
    "beach": "a sandy beach with gentle blue waves, a beach ball and a bucket on the sand",
    "bear": "a large brown bear standing on all fours among a few pine trees",
    "bike": "a single bicycle standing upright in side view, wheels frame and handlebars clearly shown",
    "bird": "a small blue bird perched on a thin branch",
    "birthday": "a birthday cake with lit candles, a party hat and streamers beside it",
    # Draped over a chair, the chair took over and the blanket read as a small cloth.
    "blanket": "a thick folded blanket resting by itself, its soft folds and stitched edge clearly visible, no furniture and no person in the picture",
    "boat": "a small wooden rowboat with oars, on calm blue water",
    "box": "a cardboard box with its four flaps open, empty",
    "breakfast": "a breakfast plate with a fried egg and toast, a glass of juice beside it",
    "brother": "two teenage brothers standing side by side with arms around each other's shoulders, smiling",
    # C
    "camera": "a single camera with a large round lens, three-quarter view",
    "candy": "a small pile of colourful wrapped candies",
    "chair": "a single wooden chair, three-quarter view",
    "cheese": "a wedge of yellow cheese with holes, on a wooden board",
    "chicken": "a white and brown chicken standing on grass",
    "chocolate": "a bar of dark chocolate with two squares broken off beside it",
    "city": "a row of tall city buildings with lit windows, seen from street level",
    "clean": "a teenager wiping a table with a cloth, a spray bottle beside them",
    "climb": "a teenager climbing a knotted rope upward in a gym",
    "clock": "a round wall clock showing three o'clock",
    "cloud": "one white fluffy cloud in a plain pale sky",
    "clown": "a friendly clown with a red nose, colourful hat and wide smile",
    "coat": "a single warm winter coat on a hanger, zipped up",
    "computer": "an open laptop computer on a desk, screen facing the viewer",
    "cook": "a teenager stirring a pot on a stove with a wooden spoon",
    # D
    "dance": "two teenagers dancing together, arms raised, caught mid-movement",
    "dark": "a bedroom at night lit only by moonlight through the window",
    "dentist": "a dentist in a white coat holding a small round mirror beside a dental chair",
    "desk": "a school desk with a notebook and a pencil on top",
    "dessert": "a bowl of ice cream with a spoon and a cherry on top",
    "dinosaur": "a friendly green long-necked dinosaur standing among ferns",
    "dirt": "a mound of brown dirt with a small shovel standing in it",
    "dish": "a neat stack of clean white plates",
    "doctor": "a doctor in a white coat with a stethoscope around their neck",
    "dollar": "a single folded one dollar bill",
    "door": "a single closed wooden door with a round handle",
    "dragon": "a friendly green dragon with small wings, breathing one puff of flame",
    "draw": "a teenager drawing an animal on paper with a pencil",
    "dress": "a single blue dress on a hanger",
    "drink": "a teenager drinking water from a tall glass",
    "drive": "an adult driving a car, both hands on the steering wheel, seen from inside",
    "drum": "a single drum with two drumsticks crossed on top",
    "duck": "a duck with a yellow bill swimming on blue water",
    # E
    # The ear came back far larger than a real ear relative to the head.
    # The hearing aid was removed at Brooke's request — the sentence in
    # make_words.py was changed to match, since it used to mention one.
    # Shown on a head, the head kept stealing the picture. Fully detached, like
    # `arm` — the isolated-limb treatment is what actually reads here.
    "ear": "one single human ear entirely on its own, drawn as one simple flat shape centred against the plain background, with no head, no face, no hair, no neck and no skin around it, and no hearing aid or earring",
    "earth": "the planet Earth seen from space, blue oceans and green continents",
    "egg": "a single white egg lying on its side by itself, with no egg cup, no bowl and nothing else in the picture",
    "elephant": "a grey elephant standing side-on with its trunk curled",
    "exercise": "a teenager in gym clothes doing a jumping jack, arms and legs out",
    "eye": "a close view of one open eye",
    # F
    "face": "a teenager's smiling face seen straight on",
    "family": "a family of four standing together: two adults and two teenagers",
    "farm": "a red barn with a wooden fence and a green field behind it",
    "farmer": "a farmer in overalls and a straw hat holding a pitchfork",
    "feet": "a pair of bare feet standing on the floor, seen from above",
    "fence": "a wooden picket fence running across the frame",
    "field": "a wide green grass field with a goal at the far end",
    # An index finger raised on a closed fist is the ASL number 1 — an isolated
    # handshape reads as a sign to this audience. Keep the finger in context,
    # doing something, so it reads as anatomy rather than as language.
    "finger": "a hand resting on an open book, one index finger pointing down at a picture on the page, the pointing finger the clear focus",
    "fire": "a campfire with orange flames over stacked logs",
    "fish": "a single silver and orange fish swimming",
    # Left unspecified this came back as a rainbow flag, so it was first pinned to
    # an invented neutral design. Brooke then asked for the US flag by name, which
    # settles it — but the design must still be stated outright, never left open.
    "flag": "the flag of the United States of America on a tall pole waving in the wind, thirteen red and white stripes with a blue rectangle of white stars in the upper corner",
    "floor": "a wooden floor seen at an angle with a broom resting on it",
    "flower": "a single yellow flower with a green stem and two leaves",
    "forest": "a group of tall green trees standing close together",
    # G
    "game": "a board game on a table with dice and coloured playing pieces",
    "garden": "a garden bed with tomato plants and a watering can",
    "ghost": "a friendly white cartoon ghost floating, with a wavy lower edge",
    # Scale needs a human reference, not a tree — a person beside a shrub just
    # reads as someone gardening.
    "giant": "an enormous friendly giant filling the frame, with two tiny ordinary people standing at his feet reaching only to his ankle",
    "gift": "a wrapped gift box with a large ribbon bow",
    "glass": "a single clear drinking glass filled with water",
    "gold": "a small pile of shiny gold coins",
    "grandfather": "an older man with grey hair and glasses, smiling warmly",
    "grandmother": "an older woman with grey hair, smiling warmly",
    # Left open, the model adds a child among the blades and the scale goes
    # surreal — grass taller than a person. Say plainly that nothing else is in it.
    "grass": "a close view of a patch of green grass blades and nothing else, no people and no animals",
    "gym": "a school gymnasium with a basketball hoop and a polished wooden floor",
    # H
    # Came back with three arms: one holding hair, one brushing, one hanging spare.
    "hair": "a teenager with long hair seen from the side, holding a hairbrush in one hand and brushing their hair, with exactly two arms and two hands in the picture",
    "halloween": "a carved orange pumpkin glowing, with a small bat above it",
    # A spread open palm facing the viewer is the ASL 5 handshape. Anchor the
    # hand to an arm and a surface so it reads as anatomy, not language.
    "hand": "a teenager's hand and forearm resting palm-up and relaxed on a table top, the open hand the clear focus",
    # "head and shoulders straight on" is the same picture as `face`. The hat
    # gives the head a top and a shape of its own.
    # Showed the whole body, so the head was not the subject.
    # The hat was here to stop this colliding with `face`; Brooke asked for it
    # gone, so side profile against `face`'s front view is now the only thing
    # keeping the two pictures apart.
    "head": "a close view of a teenager's whole head and neck in side profile, hair visible and nothing covering the head, no hat, cropped at the shoulders with no body below",
    "heart": "a simple red heart shape",
    "hide": "a teenager crouching behind a door, peeking around its edge",
    "hill": "a green rounded hill with a path winding up it",
    "hole": "a round hole in the ground with loose soil around the edge",
    "horse": "a brown horse standing side-on",
    "hospital": "a hospital building with a red cross sign and an ambulance outside",
    "hungry": "a teenager holding their stomach and looking at an empty plate",
    # I
    "ice": "three clear ice cubes stacked together",
    "ice cream": "an ice cream cone with two round scoops",
    "island": "a small green island with one palm tree, surrounded by blue water",
    # J
    # jar / milk / scissors all came back giant because the style block asks the
    # subject to fill ~70% of the frame — with a person in shot the *object*
    # took the 70%. Dropping the person removes the conflict entirely.
    "jar": "a single glass jar with a lid, filled with round biscuits, standing by itself with no person in the picture",
    "juice": "a tall glass of orange juice with a straw",
    "jump": "a teenager bouncing high in the air above a round trampoline, knees bent and arms out for balance, clearly airborne well above the trampoline mat",
    # K
    "kick": "a teenager kicking a soccer ball, leg extended",
    "king": "a king wearing a gold crown and a red robe",
    "kiss": "a parent kissing a small child on the cheek",
    "kitchen": "a kitchen with a counter, a sink and cupboards",
    "kite": "a red diamond kite with a tail flying in the sky",
    "knee": "a teenager's bent knee with a small bandage on it",
    # The board dominated the square and the blade looked embedded in it.
    "knife": "a single kitchen knife lying by itself on a plain surface, its blade and handle clearly visible, with no cutting board",
    # L
    "ladder": "a wooden ladder leaning against a wall",
    "lake": "a calm blue lake with trees along the far shore",
    "lamp": "a table lamp switched on and glowing",
    "laugh": "a teenager laughing with their head tilted back",
    # Cropping at the waist left a headless torso.
    # A whole standing figure is the picture for `stand`. Crop to the limb.
    "leg": "a close view of one single bare leg by itself from hip down to the foot, wearing a trainer, the leg filling the picture, no body above the hip",
    "letter": "a sealed white envelope with a stamp in the corner",
    "library": "tall bookshelves full of books with a reading table in front",
    "light": "a glowing light bulb",
    "lion": "a male lion with a thick mane, standing side-on",
    "lock": "a closed metal padlock with a keyhole",
    "lunch": "a school lunch tray holding a sandwich, an apple and a carton of milk",
    # M
    "magic": "a magician's top hat with a rabbit coming out of it and a wand beside it",
    "mailman": "a mail carrier in uniform holding letters beside a mailbox",
    "mall": "a shopping mall interior with shop fronts along a walkway",
    "math": "a chalkboard covered with plus, minus, multiply and divide symbols and simple numbers",
    "meat": "a cooked steak on a white plate",
    "medicine": "a medicine bottle with a measuring spoon beside it",
    "milk": "a single tall glass of white milk standing by itself, no person in the picture",
    "money": "a small stack of bills with a few coins beside it",
    "monkey": "a brown monkey hanging from a branch by one arm",
    "monster": "a friendly purple cartoon monster with big round eyes, smiling",
    "moon": "a full moon in a dark sky with a few small stars",
    "mother": "a smiling adult woman standing with her arm around a teenager",
    "mountain": "a tall mountain with a snow-capped peak",
    "mouse": "a small grey mouse with a long tail",
    # `face`, `mouth` and `nose` all came back as the same head-and-shoulders
    # portrait. Body-part words need the crop stated outright, or the model
    # defaults to drawing the whole person.
    "mouth": "an extreme close-up of only the lower part of a face, filling the whole frame: lips open in a smile showing the teeth, chin below, no eyes and no hair in view",
    "movie": "a cinema screen showing a bright picture, two seats in front seen from behind",
    # Left as "brown", the restricted palette pushes this to bright orange and
    # it stops reading as mud. Name the dark brown explicitly.
    "mud": "a puddle of thick dark chocolate-brown mud on the ground with a deep boot print pressed into it",
    "music": "musical notes floating above a guitar and a drum",
    # N
    "name": "a teenager smiling and pointing at a rectangular name tag on their shirt reading MAYA",
    "neck": "a teenager's neck and shoulders with a scarf around the neck",
    "neighbor": "two people waving to each other over a garden fence",
    "nest": "a round bird nest with three pale eggs in it, on a branch",
    "night": "a dark night sky full of stars above a quiet house",
    "nose": "an extreme close-up of only the middle of a face in three-quarter view, filling the whole frame: the nose large and central with both nostrils clear, no whole head in view",
    "nurse": "a nurse in scrubs holding a clipboard",
    "nut": "a walnut and an acorn side by side",
    # O
    # Without this it draws a beach with people and duplicates `beach`.
    "ocean": "open blue ocean water filling the frame with rolling waves and a flat empty horizon, no beach, no land and no people",
    "office": "an office with a desk, a chair and a computer",
    "orange": "a single orange fruit with one green leaf on top",
    "oven": "an oven with its door closed and the inside light glowing",
    # The doorway slab dominated and the stride read as off balance.
    "outside": "a teenager standing on green grass in bright sunshine with a house and its open front door behind them, arms relaxed, clearly out of doors",
    # P
    "paint": "a paintbrush resting across an open tin of blue paint",
    "pants": "a pair of blue jeans, neatly folded",
    # Unstated, the restricted palette colours plain objects orange. White has
    # to be asked for by name.
    "paper": "a single blank sheet of plain white paper, pure white with one corner curling",
    "park": "a park with a bench, a tree and a winding path",
    "party": "a party scene with balloons, streamers and a cake on a table",
    "pencil": "a single sharpened yellow pencil",
    "phone": "a mobile phone held in one hand, screen facing the viewer",
    "piano": "an upright piano with the lid open showing the keys",
    "picture": "a framed picture of a dog hanging on a wall",
    "plant": "a green potted plant on a windowsill",
    "police": "a police officer in uniform standing beside a patrol car",
    "potato": "a single brown potato",
    "present": "two wrapped presents stacked, each with a ribbon",
    "pumpkin": "a large round orange pumpkin with a curling green stem",
    "puppy": "a small brown puppy sitting with its tail wagging",
    # Q
    "queen": "a queen wearing a crown and a blue gown, waving",
    "quiet": "a library reading room with a student holding one finger to their lips",
    # R
    "rabbit": "a white rabbit sitting on grass with its ears up",
    "rain": "rain falling from one grey cloud onto the ground",
    "rainbow": "a colourful rainbow arcing across the sky",
    "read": "a teenager sitting and reading an open book",
    "rice": "a white bowl filled with cooked white rice",
    "ride": "a teenager riding a bicycle along a path",
    # The hand was malformed — wrong digit count and the ring finger cut off at the band.
    "ring": "a single gold ring with a small blue stone, standing upright by itself, with no hand and no person in the picture",
    "river": "a blue river winding between green banks",
    "road": "a grey road with a dashed centre line stretching to the horizon",
    "robot": "a friendly silver robot standing upright with round eyes",
    "rock": "a large grey rock resting on the ground",
    "rocket": "a white and red rocket lifting off with flame beneath it",
    "roof": "a house roof with red tiles, seen from outside",
    "room": "a bedroom with a bed, a window and a rug",
    "rope": "a neatly coiled length of thick rope",
    # S
    "sandwich": "a sandwich cut in half showing cheese filling, on a plate",
    # Raised open palms read as the ASL 5 handshape. Show the fear in the body
    # and face instead of in the hands.
    "scared": "a teenager shrinking backwards with shoulders hunched and both hands clasped tightly together at their chest, eyes wide and eyebrows raised in fright",
    "school": "a school building with a flag and steps up to the door",
    "science": "a science beaker of coloured liquid beside a microscope",
    "scissors": "a single pair of open scissors lying by itself, no person in the picture",
    "shirt": "a single striped shirt on a hanger",
    "shoe": "a single sneaker, side view",
    "shop": "a small shop front with a striped awning and a window display",
    "sidewalk": "a concrete sidewalk running beside a street, paving lines visible",
    "sing": "a teenager standing and singing with their mouth open, musical notes floating nearby",
    "sister": "two teenage sisters standing together, smiling",
    "skate": "a teenager ice skating on a frozen pond",
    # The floating Zs contradicted the no-letters rule in the same prompt.
    "sleep": "a teenager asleep in bed under a blanket with eyes closed and head on the pillow, a crescent moon visible through the window",
    "slide": "a playground slide with a child sliding down it",
    "smell": "a teenager leaning toward a flower and smelling it, with wavy scent lines",
    # A single smiling portrait is already `face`. Make this one about the act
    # of smiling at someone.
    "smile": "two teenage friends facing each other and grinning broadly, both smiles clearly visible",
    "soap": "a bar of soap with bubbles around it",
    "soccer": "a black and white soccer ball resting on grass",
    "spider": "a spider sitting on its web",
    # All three came back nearly the same size, so the scale taught the wrong thing.
    "sport": "a soccer ball, a basketball and a baseball resting side by side on the ground at their true relative sizes: the basketball clearly the biggest, the soccer ball a little smaller, and the baseball much smaller than both",
    "stairs": "a flight of stairs going upward",
    "stand": "a teenager standing upright with arms relaxed at their sides",
    "star": "a single bright yellow five-pointed star",
    "stomach": "a teenager pointing at their stomach",
    "store": "a grocery store aisle with shelves of food on both sides",
    "storm": "dark storm clouds with a lightning bolt and falling rain",
    "stove": "a stove top with a pot sitting on one burner",
    "street": "a street with buildings on both sides and a crosswalk",
    "swim": "a teenager swimming in a pool, arms mid-stroke",
    "swing": "a playground swing with a child swinging on it",
    # T
    "table": "a wooden table with four legs",
    # A rear view of a dog's backside is not a readable picture of a tail; a
    # whole dog makes the tail too small. Crop to the back half, side on.
    # Told to fill the frame the tail swallowed the dog and read as a flame.
    # The dog has to stay recognisable for the tail to mean anything.
    # Cropping and scaling both failed to single out the tail, so the picture
    # now points at it outright. This is the only arrow in the book.
    "tail": "a golden-brown dog standing side-on with natural tan and brown fur, its long fluffy tail raised and curling upward, and one bold charcoal arrow in clear space beside the dog with its tip touching the tail",
    "teacher": "a teacher standing beside a whiteboard, facing the class",
    # Would otherwise be the same crop as `mouth`. The action distinguishes it.
    "teeth": "a teenager brushing their front teeth with a toothbrush, mouth open so the white teeth are the clear focus",
    "tiger": "an orange tiger with black stripes, standing side-on",
    # "showing a clear time" was vague enough that the text exception let a
    # caption through. Name exactly which characters are allowed.
    "time": "a close view of a wristwatch worn on a wrist, its round dial carrying the numerals 1 to 12 and the hands pointing to three o'clock, and no other writing anywhere",
    "tired": "a teenager yawning with drooping eyes, resting their head on one hand",
    "tissue": "a tissue box with one tissue pulled up out of it",
    "tongue": "a close view of a teenager's face straight on, mouth open and tongue stuck well out, the tongue the clear focus",
    "touch": "a hand reaching out with one fingertip touching a surface",
    "town": "a small town with a few buildings, a road and trees",
    "train": "a train on tracks, side view",
    "tree": "a single green leafy tree with a brown trunk",
    "truck": "a delivery truck, three-quarter front view",
    "turkey": "a brown turkey with its tail feathers fanned out",
    "turtle": "a green turtle with a patterned shell",
    # U
    "uncle": "a smiling adult man standing beside a teenager",
    # V
    "vacation": "a suitcase, a sun hat and a beach ball grouped together",
    "vegetable": "a carrot, a head of broccoli and a tomato grouped together",
    # W
    "wash": "a pair of hands under running water with soap suds",
    # `time` is already a watch on a wrist. Show this one as the object itself.
    "watch": "a single wristwatch lying flat on a table seen from above, its strap unbuckled and stretched out straight, buckle clearly visible",
    "wave": "a large blue ocean wave curling over",
    "weather": "a bright sun beside a cloud with rain falling from it",
    "wet": "a teenager in a raincoat with water dripping off them",
    "window": "a single window with curtains, seen from inside",
    "winter": "a snowy scene with a bare tree and snow falling",
    "witch": "a friendly witch in a pointed hat riding a broom",
    "woman": "an adult woman standing and smiling",
    "wood": "a stack of cut logs",
    # A desk and a computer is already `office`.
    "work": "an adult in a tool belt working at a workbench with both hands, concentrating on the job",
    "write": "a hand writing on a sheet of paper with a pencil",
    # X
    "x-ray": "an x-ray image of a hand showing the bones",
    "xylophone": "a colourful xylophone with two mallets resting on it",
    # Y
    "yard": "a house yard with grass, a tree and a rake leaning against the fence",
    # `tired` is already a yawn with a hand at the mouth. The stretch separates them.
    "yawn": "a teenager yawning wide with both arms stretched straight up above their head in a big morning stretch",
    "yellow": "a lemon, a banana and a yellow flower grouped together, all clearly yellow",
    "young": "a small child standing next to a teenager, showing the difference in age",
    # Z
    "zoo": "a zoo entrance gate with an elephant and a giraffe visible behind it",
}
