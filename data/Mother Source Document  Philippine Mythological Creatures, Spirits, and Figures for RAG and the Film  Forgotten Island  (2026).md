# Mother Source Document: Philippine Mythological Creatures, Spirits, and Figures for RAG and the Film "Forgotten Island" (2026)

## 0. Purpose and Scope

This document is designed as a **primary knowledge base for a Retrieval-Augmented Generation (RAG) chatbot** focused on Philippine mythology and as a **reference backbone for mythological creatures and figures likely to inform the worldbuilding of the film *Forgotten Island* (2026)**, a DreamWorks Animation feature described as a magical island rooted in Philippine mythology.[^1][^2][^3]

It integrates:

- A taxonomy of major **creature brackets**, spirits, and divine/heroic figures across the archipelago.[^4][^5]
- Per‑entity reference entries structured for machine consumption (names, classification, domains, regions, behavior, symbolism, relations to daily Filipino life, and media hooks).
- Notes on **how to structure and tag this content for RAG**, including fields you can turn into embedding chunks or metadata.

Plot and character details for *Forgotten Island* remain largely under wraps as of 2026, but public information confirms that the story centers on an island inspired by Philippine mythology and on best friends Jo and Raissa trapped in the mystical world of Nakali. The film is therefore expected to draw from widely recognizable mythological motifs (e.g., aswang, diwata, forest spirits, sea beings) rather than a single epic.[^6][^7][^1]

***

## 1. High-Level Taxonomy for RAG

### 1.1 Top-Level Brackets

For RAG, index creatures and figures under the following top-level **brackets** (each bracket can be a facet filter or metadata field):[^5][^4]

1. **Shape‑shifters and Night Predators**  
   Aswang in its many aspects, manananggal/anananggal, tiktik, wakwak, sigbin, amalanhig, busaw, bal‑bal, berbalang, etc.[^8][^4]

2. **Forest, Tree, and Mountain Spirits**  
   Kapre, agta, tikbalang, nuno sa punso, various dwarfs (duwende, ansisit, bonḡan), mountain diwata like Maria Makiling and Maria Sinukuan.[^9][^4]

3. **Earth Dwellers and Household Little Folk**  
   Duwende, nuno sa punso, ansisit, aghoy, annani, household spirits and lamán‑lupa (earth spirits).[^4][^9]

4. **Water and Weather Beings**  
   Bakunawa, sirena/kataw/siyokoy, nāga, magindara, berberoka, buwaya as spiritual crocodile, river and lake monsters (ugkoy, etc.).[^5][^4]

5. **Sky, Celestial, and Omen Beings**  
   Minokawa, galura, Arimaonga, santelmo/allawig, tigmamanukan and bird omens, lightning/thunder spirits like Anit/Anitan.[^4][^5]

6. **Divine, Semi‑Divine, and Culture Heroes**  
   Diwata and deities; mountain goddesses (Mariang Makiling, Sinukuan, Cacao); culture heroes and giants like Bernardo Carpio, as well as regional gods in the *List of Philippine mythological figures*.[^10][^11]

7. **Healers, Witches, and Sorcerers**  
   Albularyo, babaylan, mangkukulam, mambabarang, banwaanon witches, barang, etc., who mediate or weaponize relations with spirits.[^8][^4]

8. **Ghosts, Ancestors, and Urban Legends**  
   Multo, anito, tiyanak as a child‑spirit demon, white ladies, bangungot demons, and modern urban spirits.[^12][^9]

For each entity, store **multiple bracket tags** as needed (e.g., manananggal ⟶ bracket: shape‑shifter, bracket: night predator, bracket: aswang‑type).

### 1.2 Core Field Schema (Per Entity)

Each creature/figure entry below is written in natural language, but can map to the following suggested structured fields:

- `name_primary` – Main name in English/Tagalog.
- `name_variants` – Spelling variants, regional names, etymology.
- `classification` – Bracket(s): e.g., "aswang-type viscera-sucker", "forest giant", "river spirit".
- `domain` – Forest, mountain, house, graveyard, sea, river, sky, etc.
- `regions_ethnic_groups` – Named ethnolinguistic groups and locations.
- `description` – Physical form and behavior.
- `powers_abilities` – What it can do.
- `weaknesses_protections` – Folk methods for avoiding/defeating it.
- `symbolism_themes` – Social, moral, or psychological meanings.
- `daily_life_links` – Concrete practices, taboos, or superstitions it informs.
- `narrative_roles` – Typical story functions (villain, guardian, trickster, psychopomp, etc.).
- `modern_media_notes` – Appearance or likely appearance in modern films, comics, games, including *Forgotten Island* relevance where appropriate.

***

## 2. Aswang and Shape‑Shifters

### 2.1 Aswang (Umbrella Category)

**Names and Variants**  
- Aswang, asuwang, asuáng; regional subtypes include blood‑sucking vampires, viscera‑suckers, weredogs, witches, and ghouls.[^4]

**Classification / Domain / Regions**  
- Classification: Umbrella term for malevolent shape‑shifters and witches.[^4]
- Domain: Villages, outskirts of towns, trees, cemeteries, night roads.  
- Regions: Especially Visayas (Iloilo, Capiz, Antique, Negros), Bicol, Tagalog areas, parts of Mindanao; also Mandaya/Bagobo variants (asuáng) as tree‑dwelling malevolent spirits.[^5][^4]

**Core Description and Powers**  
- Aswang is best understood as a **cluster** of five main aspects: blood‑sucking vampire, self‑segmenting viscera‑sucker, man‑eating weredog or other beast, vindictive witch, and corpse‑eating ghoul.[^4]
- Can appear human by day but transform at night; senses scent of sickness and death from afar.[^4]

**Weaknesses and Protections**  
- Common prophylactics: garlic, salt, sharp or pungent items, loud noise, blessed objects, keeping wakes well‑attended.[^9][^8]

**Symbolism and Themes**  
- Encodes anxieties around illness, infant mortality, and social deviance (e.g., midwives or reclusive neighbors cast as hidden monsters).[^13][^4]

**Daily Life Links**  
- Explains sudden deaths, miscarriages, wasting illnesses, and corpse mutilation.[^14][^9]
- Spawns behavior such as **group night vigils**, beliefs about checking shadows/reflections, and community rumor cycles about suspected aswang families.[^14][^8]

**Modern Media Notes**  
- Central monster in Philippine horror films and TV; likely among the first creatures global audiences will expect when hearing "Philippine mythology" in contexts like *Forgotten Island*.[^15][^14]

***

### 2.2 Manananggal / Anananggal

**Names and Variants**  
- Manananggal (Tagalog, Visayan); anananggal (Bicol); from *tanggal* (to remove, detach).[^4]

**Classification / Domain / Regions**  
- Classification: Aswang‑type viscera‑sucker and flying torso.[^5][^4]
- Domain: Night skies above rural houses, especially of pregnant women; rooftops, coconut groves.  
- Regions: Tagalog provinces (Batangas, Quezon), Bicol, Visayas (Capiz, Antique, Iloilo).[^5][^4]

**Core Description and Powers**  
- Upper torso separates from lower body at night, grows bat‑like wings, and flies with trailing viscera; uses long, thread‑like tongue to suck fetuses and viscera through roof cracks or windows.[^9][^4]

**Weaknesses and Protections**  
- Folk method: sprinkling salt, garlic, ash, or sand on the abandoned lower torso so the creature cannot reattach and dies at sunrise.[^4]
- Protective measures: keeping lights on, closing windows, placing sharp or pungent items near doors/windows, staying in groups at night.[^16][^9]

**Symbolism and Themes**  
- Encodes tension around **female bodies, sexuality, pregnancy, and midwifery**, often demonizing independent women.[^13][^8]

**Daily Life Links**  
- Pregnant women may follow extra taboos at night; strange noises on the roof, bird cries like *tiktik*/*kikik*, or animals on roofs can be interpreted through manananggal lore.[^12][^9]

**Modern Media Notes**  
- Staple of Filipino horror cinema and comics; visually striking flying torso may inspire cinematic creatures in *Forgotten Island* even if not named explicitly.

***

### 2.3 Tiktik, Wakwak, and Asuwang na Layog

**Names and Variants**  
- Tiktik, kikik, wakwak; asuwang na layog ("flying aswang") in Bicol.[^4]

**Classification / Domain / Regions**  
- Classification: Bird‑like aswang aspects, harbingers or agents of viscera‑suckers.[^4]
- Domain: Night sky above villages; roofs and trees.  
- Regions: Bicol, Visayas, many Tagalog areas.[^9][^4]

**Core Description and Powers**  
- Often described as birds or flying beings whose cries mislead people: they sound far when the creature is near and vice versa.[^4]
- Sometimes identified with or accompanying manananggal to locate victims.[^8]

**Daily Life Links**  
- Night bird calls near homes with pregnant or sick people can trigger anxiety and protective rituals; children are taught to stay indoors when such cries are heard.[^12][^9]

***

### 2.4 Sigbin

**Names and Variants**  
- Sigbin, sigben; sometimes linked in modern narratives to Easter or Holy Week.

**Classification / Domain / Regions**  
- Classification: Night‑stalking cryptid/monster; sometimes folded into aswang lore.[^15][^4]
- Domain: Village outskirts, fields, and cemeteries at night.  
- Regions: Especially Visayas (Bohol and nearby areas).[^15]

**Core Description and Powers**  
- Described as a small, kangaroo‑ or goat‑like creature that walks backwards with head lowered between hind legs, long ears, whip‑like tail, and glowing eyes.[^15]
- Said to suck blood or eat hearts of victims, sometimes specifically targeting children during Holy Week.[^15]

**Symbolism and Daily Life**  
- Used to frighten children from wandering at dusk or violating Holy Week solemnity; ties monsters to the Christian liturgical calendar.[^15]

***

### 2.5 Amalanhig / Maranhig (Hiligaynon Vampire)

**Names and Variants**  
- Amalanhig, maranhig (Hiligaynon, Western Visayas).[^4]

**Classification / Domain / Regions**  
- Classification: Vampire‑like revenant, a failed transfer of aswang powers.[^4]
- Domain: Forests, village outskirts, rivers; night roads.  
- Regions: Western Visayas, especially Hiligaynon‑speaking areas.[^4]

**Core Description and Powers**  
- A dead aswang whose vampiric power was not inherited; rises from the grave to suck blood of sleeping villagers.[^4]

**Weaknesses and Protections**  
- Joints are stiff; cannot negotiate crooked paths or crooked trees. Victims can escape via winding paths, crooked trees, or crossing bodies of water.[^4]

**Daily Life Links**  
- Explains certain nightmares and nocturnal terrors; reinforces the need to guard wakes and treat the dead carefully.[^16]

***

### 2.6 Busaw, Bal‑bal, Berbalang, and Other Ghouls

**Classification and Regions**  
- Busaw / busau / buso: corpse‑eaters and battlefield ghouls in Bagobo, Mandaya, and other Mindanao traditions.[^4]
- Bal‑bal: ghoul in Tagbanua and Maranao lore that flies like a squirrel and devours corpses or fetuses.[^4]
- Berbalang: Sulu ghoul that sends out astral bodies to feast on corpses and can be repelled by coconut pearls.[^4]

**Daily Life Links**  
- Justify communal wakes, night vigils, graveyard taboos, and swift, careful burial practices to protect the dead from desecration.[^16][^9]

***

## 3. Forest, Tree, Earth, and Mountain Spirits

### 3.1 Kapre and Agta (Tree Giants)

**Names and Variants**  
- Kapre (Tagalog, national); agta in Eastern Visayas and some Visayan sources; multiple tall, dark, tree‑dwelling giants.[^9][^4]

**Classification / Domain / Regions**  
- Classification: Forest/tree giant or spirit; sometimes a class of lamán‑lupa.[^4]
- Domain: Large trees (balete, santol, mango, acacia), mangroves, swamp forests.  
- Regions: Throughout lowland Philippines, particularly Tagalog and Visayan areas.[^9][^4]

**Core Description and Powers**  
- Very tall, dark, hairy humanoid, often smoking a large cigar or pipe; may carry a cane in some Visayan descriptions.[^4]
- Can frighten or mislead people, occasionally blocking paths or giving commands; often more mischievous than outright murderous.[^9][^4]

**Daily Life Links**  
- Fear of large trees at night; warnings to children not to climb or disturb certain trees; persistent practice of saying **"tabi‑tabi po"** near old trees.[^9]
- Folk rules against cutting prominent trees without offerings or prayers to avoid misfortune, illness, or accidents.[^5][^9]

***

### 3.2 Tikbalang

**Names and Variants**  
- Tikbalang, tigbalang;

**Classification / Domain / Regions**  
- Classification: Forest trickster, part‑horse, part‑human.
- Domain: Mountain passes, forest paths, often at crossroads.  
- Regions: Tagalog, Ilocano, and other lowland areas.[^5][^9]

**Core Description and Powers**  
- Tall, emaciated humanoid with horse’s head and hooves, long limbs, sometimes with backward hooves; can confuse travelers, making them walk in circles.[^9]

**Protections and Daily Life**  
- Counter‑rituals include turning clothes inside‑out, politely asking for directions, or acknowledging the spirit; these reflect an ethic of respect for unseen owners of places.[^9]
- Explains why hikers get lost or why paths feel "enchanted," and appears frequently in school materials and pop culture.

***

### 3.3 Nuno sa Punso and Ansisit (Mound Dwellers)

**Names and Variants**  
- Nuno sa punso (Tagalog), ansisit (Ilokano), various dwarf elders dwelling in mounds and anthills.[^9][^4]

**Classification / Domain / Regions**  
- Classification: Earth/household spirits, lamán‑lupa, dwarfs.  
- Domain: Mounds, anthills, underground spaces, roots.  
- Regions: Widespread in lowland Philippines.[^9]

**Core Description and Powers**  
- Small elder with large head and joints; can inflict swelling, fever, or deformities when offended.[^4]

**Daily Life Links**  
- Strict rule: do not kick, sit on, or urinate on mounds; always say "tabi‑tabi po" when passing.[^9]
- Unexplained swelling, fevers, or skin conditions may be diagnosed as **"natapakan ang nuno"** and treated via albularyo rituals.[^16][^9]

***

### 3.4 Duwende, Aghoy, Annani, and Other Little Folk

**Names and Regions**  
- Duwende (Tagalog, national), aghoy (Waray), annani (Ibanag), various regional dwarf spirits.[^5][^4]

**Classification / Domain**  
- Classification: Little folk, household or yard spirits; can be benevolent (white duwende), malevolent (black duwende), or ambivalent.[^5]

**Behavior and Daily Life**  
- Can bestow luck, food, or gold on respectful humans (e.g., aghoy gifting magic pots and purses), or punish disrespect with illness or misfortune.[^4]
- Families may leave small offerings (food, rice, sweets) or verbally acknowledge them when cleaning yards or moving furniture.[^9]

***

### 3.5 Mountain Diwata: Maria Makiling, Maria Sinukuan, Maria Cacao

#### Maria Makiling

- **Classification**: Mountain diwata / nature spirit of Mount Makiling, Laguna.[^11][^17]
- **Traits**: Beautiful, ageless woman with long hair; guardian of animals, forests, and weather on her mountain.[^11]
- **Themes**: Fertility, generosity, and punishment of greed; widely interpreted as a hispanized survival of a pre‑colonial Tagalog goddess.[^18][^11]
- **Daily Life Links**: Used in environmental education, tourism branding, and local stories about why Makiling’s forest should be protected; locals note that the mountain profile resembles a reclining woman.[^17][^11]

#### Maria Sinukuan

- **Classification**: Diwata of Mount Arayat, Pampanga.[^19][^20]
- **Traits**: Provider of abundant fruits and animals, but punishes those who greedily exploit the mountain.[^19]
- **Daily Life Links**: Teaches respect toward Mount Arayat and its resources; appears in Kapampangan folktales and contemporary cultural materials.[^19]

#### Maria Cacao

- **Classification**: Diwata of Mount Lantoy (Argao, Cebu), associated with cacao cultivation and a golden ship.[^21][^22]
- **Traits**: Sails a golden boat along rivers to transport cacao beans; sometimes merged with psychopomp motifs, ferrying souls or causing floods.
- **Daily Life Links**: Links local agriculture and flood events to mythic explanations; used in heritage tourism and in modern marketing (e.g., chocolate brands telling her story).[^22][^21]

***

### 3.6 Bernardo Carpio and Giants

- **Bernardo Carpio**: Legendary strongman or giant trapped between mountains in Montalban (Rodriguez, Rizal), whose struggles cause earthquakes.[^23][^24]
- **Origins**: Probably a fusion of pre‑Hispanic earthquake deity with Spanish chivalric hero Bernardo del Carpio; later re‑interpreted as a symbol of resistance against colonial and political oppression.[^25][^23]
- **Daily Life Links**: Earth tremors humorously or poetically attributed to him; local tourism in Rizal uses his legend; also appears in political speeches and essays as a metaphor for the Filipino people.[^23][^25]

***

## 4. Water and Sea Beings

### 4.1 Bakunawa

**Classification / Regions**  
- Serpentine dragon or giant sea serpent associated with eclipses and the disappearance of multiple moons in Visayan and Bicolano lore.[^5][^4]

**Description and Role**  
- Sometimes depicted with multiple wings and whiskers; said to have devoured six of seven moons, causing people to bang pots and gongs to make it release the last moon.[^5][^4]

**Daily Life Links**  
- Traditional explanation for eclipses and lunar anomalies; noise‑making rituals during eclipses and festivals like **Halia** in Bicol commemorate the struggle with Bakunawa.[^5]

**Modern Media Notes**  
- Frequently appears in children’s books and recent illustrated anthologies; natural candidate for a cinematic set‑piece creature in Philippine‑themed fantasy like *Forgotten Island*.[^3][^26]

***

### 4.2 Sirena, Kataw, Siyokoy, Magindara, Nāga

**Names and Classification**  
- Sirena: mermaid with human torso and fish tail, often seductive.[^5]
- Kataw: Visayan term for merfolk, sometimes high‑ranking sea spirits.[^5]
- Siyokoy: amphibious, scaled male sea being with fins and sometimes more monstrous than sirena.[^27][^5]
- Magindara: beautiful but dangerous sea beings that lure men and then drown or devour them.[^5]
- Nāga: freshwater serpent‑mermaids controlling rain and floods.[^5]

**Daily Life Links**  
- Folkloric explanations for drownings, storms, and treacherous currents; children are warned not to swim in deep or "enchanted" waters.[^28][^5]
- Offerings at rivers and seas, as well as rituals before sailing or fishing, can be related to appeasing such beings.

***

### 4.3 Berberoka, Buwaya, and Local River Monsters

- **Berberoka (Apayao)**: Water ogre that removes water from ponds to expose fish, then drowns humans when the water suddenly returns.[^4]
- **Buwaya**: Ordinary crocodiles can be seen as spiritually charged beings that punish or reward; in some tales, anthropomorphic crocodile spirits carry boxes of treasure or souls.[^4]
- **Ugkoy and Others**: Crocodile‑like or serpentine river monsters in Samar and elsewhere that grab victims by the feet.[^5]

**Daily Life Links**  
- Promote safety in wetlands and respect toward crocodiles; the insult "buwaya" for corrupt people builds metaphors of devouring greed onto the animal’s fearsome image.

***

## 5. Sky, Fire, and Omen Beings

### 5.1 Santelmo / Allawig

- **Santelmo / Allawig (Ilokano)**: Ball of fire seen moving over fields or water at night; may represent Saint Elmo’s fire, marsh gas, or other luminescent phenomena in folk understanding.[^4]
- **Behavior**: Can lead travelers astray, cause them to circle endlessly, or lure them toward swamps.[^4]
- **Daily Life Links**: Justifies prohibitions on night travel through swamps and unlit fields; sometimes linked to souls of the drowned.

***

### 5.2 Minokawa, Arimaonga, Galura, Tigmamanukan

- **Minokawa**: Giant bird that can devour sun, moon, and earth; associated with cosmic danger and renewal.[^5]
- **Arimaonga (Maranao)**: Sky lion that occasionally swallows the moon, causing eclipses, and spits it out when people make noise.[^4]
- **Galura**: Massive bird in some highland and Kapampangan traditions that carries away enemies or holds up the sky.[^5]
- **Tigmamanukan**: Omen bird in pre‑colonial Tagalog divination; flight direction interpreted as sign of success or failure.[^24][^5]

**Daily Life Links**  
- Integrate celestial events into ritual (noise‑making during eclipses); bird omens reflect a broader pattern of reading nature as a guide before travel or warfare.

***

## 6. Healers, Witches, and Ritual Specialists

### 6.1 Albularyo and Babaylan

- **Albularyo**: Folk healer using herbs, orasyon (prayers), divination like *tawas*, and spirit negotiations to treat illnesses attributed to offended spirits or witchcraft.[^8][^9]
- **Babaylan**: Pre‑colonial priest‑healer (often female or gender‑variant) in many Visayan and other societies; leads rituals for deities and spirits.[^10]

**Daily Life and Mythical Ecology**  
- Serve as **interfaces** between humans and lower mythological creatures; diagnose whether a sickness is from nuno, duwende, aswang, engkanto, or natural causes, then prescribe appeasement or counter‑magic.[^8][^9]
- Even in the 21st century, many Filipinos consult albularyo alongside biomedical doctors, especially for illnesses believed to have spiritual causation.[^9]

***

### 6.2 Mangkukulam, Mambabarang, Barang, Banwaanon Witches

- **Mangkukulam**: Sorcerer who harms via effigies, candles, and sympathetic magic.[^8]
- **Mambabarang / Barang / Balbalan**: Witches using insects or spirit allies to enter victims’ bodies, causing pain or madness; analogous figures in Samar, Leyte, and Sulu.[^4]
- **Banwaanon (Cebu)**: Jungle spirits or witches; some serve as familiars or patrons of human sorcerers.[^4]

**Daily Life Links**  
- Provide supernatural explanations for hard‑to‑treat or psychosomatic illnesses, social conflict, and envy; villagers may avoid provoking suspected witches, and rumors can strongly shape community dynamics.[^16][^8]

***

## 7. Ghosts, Ancestors, and Urban Legends

### 7.1 Multo, Anito, and Ancestor Relations

- **Multo**: Generic term for ghosts; may be tied to specific places, deaths, or unresolved grievances.[^9]
- **Anito**: Indigenous term for ancestral or nature spirits, including deified ancestors or local gods.[^10]

**Daily Life Practices**  
- *Pagpag* (not going straight home after a wake), offerings to the dead, and avoidance of certain night activities are ways of managing relationships with the dead and unseen beings.[^12][^9]

***

### 7.2 Tiyanak, Bangungot, White Ladies

- **Tiyanak**: Demonic child or goblin that imitates a crying baby to lure people in and then attacks; sometimes linked to souls of aborted or unbaptized infants.[^9][^4]
- **Bangungot**: Nightmare demon tied to sudden death in sleep after a heavy meal; described as a heavy being sitting on the chest or suffocating the sleeper.[^4]
- **White Lady**: Modern archetype of a vengeful female ghost in white, haunting roads, bridges, or schools.[^27][^12]

**Daily Life Links**  
- These figures connect to anxieties about morality (abortion, betrayal), sudden unexplained deaths, and dangerous locations; they are widely used to caution against reckless behavior and appear prominently in Filipino horror media.[^12][^8]

***

## 8. Divine and Mythological Figures (Diwata, Deities, Culture Heroes)

Beyond lower creatures, RAG may need coverage of **deities and divine figures** compiled in the *List of Philippine mythological figures*.[^10]

Examples:

- **Bathala / Mahal na Makaako** (Tagalog supreme deity), creator and life‑giver.[^10]
- **Apo Sandawa / Apo Namalyari / Kabunian** and many other highland sky gods.[^10]
- **Regional diwata** associated with winds, rivers, agriculture, and war.

For each, mirror the same field schema, but add a `worship_practices` field (rituals, offerings, priesthood) and note their relation to creatures (e.g., some creatures serve as messengers or pets of gods).

***

## 9. RAG Design: How to Use This Document

### 9.1 Chunking Strategy

For a RAG chatbot, break this document into chunks such as:

- **Entity‑centric chunks**: Each creature/figure subsection (e.g., "Manananggal", "Bakunawa") as one or several chunks containing all its fields.
- **Bracket overviews**: Sections like "Aswang and Shape‑Shifters", "Water and Sea Beings" as high‑level conceptual chunks.
- **Practice‑centric chunks**: Segments focused on daily life and superstition (e.g., all uses of "tabi‑tabi po", wakes, pagpag, sea taboos).[^12][^9]

Attach metadata such as:

- `type`: creature, deity, spirit, human hero, ritual specialist.
- `brackets`: array of bracket terms (aswang, diwata, engkanto, duwende, sirena, higante, etc.).
- `regions`: list of ethnolinguistic groups and locations.
- `domains`: forest, sea, mountain, house, graveyard, sky, etc.
- `danger_level`: low/medium/high (optional heuristic for UX).

### 9.2 Film Integration: *Forgotten Island* (2026)

Public sources indicate:[^2][^1][^6][^3]

- Title: *Forgotten Island* (DreamWorks Animation).  
- Release: September 25, 2026 (U.S.).  
- Logline: Two lifelong best friends become stranded on the mystical world of **Nakali**, where their only escape may cost them their shared lifetime of memories.
- Setting: A long‑forgotten magical island "rooted in Philippine mythology" and described as a "broad party comedy adventure".[^2][^3]
- Focus: Friendship, memory, and a magical island inspired by Philippine myths rather than a single specific epic.

**Implications for This Mother Document**  

- Because the studio has **not publicly confirmed exact creatures or deities** as of 2026, this document should function as a **broad reference pool** of motifs that Nakali could draw from—forest giants and dwarfs, merfolk, aswang, diwata, and culture heroes.[^7][^3]
- When extending the RAG with film‑specific data later (once trailers, tie‑in books, or press notes reveal named creatures), map each film creature to the **closest real mythological analogue in this document** (e.g., a cigar‑smoking tree giant ⟶ kapre/agta; eclipse serpent ⟶ bakunawa; laughing one‑eyed giant ⟶ bungisngis).[^5][^4]

### 9.3 Core External Reference Sources

When enriching this base text, prioritize these as upstream authorities:

- **Aswang Project – Compendium of Creatures**: Alphabetical list of hundreds of beings with regions, descriptions, and sources.[^4]
- **Maximo D. Ramos – *Creatures of Philippine Lower Mythology* and *The Aswang Complex in Philippine Folklore***: Classic taxonomies and demonological analyses.[^29][^4]
- **Damiana Eugenio – *Philippine Folk Literature* series**: Canonical collections of myths, tales, and legends; includes detailed narratives for many beings.[^26][^30]
- **Wikipedia Lists of Creatures and Mythological Figures**: Useful for inventory and cross‑linking of basic facts and names.[^10][^5]
- **Contemporary press on *Forgotten Island*** (Cartoon Brew, Philippine Star, Manila Bulletin, etc.) to track confirmed mythology links and newly invented creatures.[^6][^3][^2]

By treating this document as the **mother source** and layering new film‑specific and regional details on top of it, a RAG chatbot can answer questions ranging from "What is a kapre and how might it appear in *Forgotten Island*?" to "Why do Filipinos say 'tabi‑tabi po' near mounds and trees?", always grounded in the broader landscape of Philippine myth and everyday practice.[^9][^4]

---

## References

1. [Forgotten Island (2026) - IMDb](https://www.imdb.com/title/tt36583977/) - Follows two best friends who become stranded on the mystical world of Nakali, where their only escap...

2. [DreamWorks Animation sets 2026 date for film featuring Philippine mythology](https://www.philstar.com/movies/2025/04/16/2436513/dreamworks-animation-sets-2026-date-film-featuring-philippine-mythology) - The next movie by Hollywood studio DreamWorks Animation will center around Philippine mythology.

3. [Dreamworks Announces Original Filipino-Themed Film 'Forgotten ...](https://www.cartoonbrew.com/feature-film/dreamworks-announces-original-filipino-themed-film-forgotten-island-246811.html) - Directed by Joel Crawford and Januel Mercado, the film will debut theatrically in 2026.

4. [A Compendium of Creatures from Philippine Folklore & Mythology](https://www.aswangproject.com/creatures-mythical-beings-philippine-folklore-mythology/) - This list includes 'creatures,' 'monsters,' spirits, folkloric beings, 'witches,' and mythical beast...

5. [List of Philippine mythological creatures - Wikipedia](https://en.wikipedia.org/wiki/List_of_Philippine_mythological_creatures)

6. [DreamWorks Animation to release film inspired by Philippine ...](https://mb.com.ph/2025/06/25/dreamworks-animation-to-release-film-inspired-by-philippine-mythology) - DreamWorks Animation has announced its original film, Forgotten Island, inspired by Philippine mytho...

7. [Forgotten Island (2026) - News - IMDb](https://www.imdb.com/title/tt36583977/news/) - Focusing on an island rooted in Philippine mythology, Forgotten Island centers on lifelong best frie...

8. [A Crash Course on Philippine Lower Mythological Creatures](http://www.horror.org/private/newsletter/october-2015/183-creatures.html)

9. [Superstition in the Philippines - Wikipedia](https://en.wikipedia.org/wiki/Superstition_in_the_Philippines)

10. [List of Philippine mythological figures - Wikipedia](https://en.wikipedia.org/wiki/List_of_Philippine_mythological_figures) - Mahal na Makaako: the supreme deity who gave life to all human beings merely by gazing at them · Bin...

11. [Maria Makiling - Wikipedia](https://en.wikipedia.org/wiki/Maria_Makiling) - She is the most widely known diwatà or lambana (fairy) in Philippine mythology and was venerated in ...

12. [Supernatural Creatures in Philippine Folklore](https://www.scribd.com/document/200281060/Supernatural-Creatures-in-Philippine-Folklore) - The document summarizes several supernatural creatures from Philippine folklore including the aswang...

13. [The Creatures of Philippine Lower Mythology (Realms of Myths and ...](https://www.abebooks.com/9781713295938/Creatures-Philippine-Lower-Mythology-Realms-1713295938/plp) - Synopsis. IMAGINARY CREATURES depicted in a people's lower mythology are one of the most important p...

14. [Exploring Philippine Mythology: The Aswang and Other Folklore Creatures](https://storiesphilippines.com/exploring-philippine-mythology-the-aswang-and-other-folklore-creatures/) - Exploring Philippine Mythology: Unveiling the Mysteries of Aswang and Other Mythological Creatures W...

15. [13 Philippines Mythical Creatures Travelers Should Look Out For](https://www.traveloka.com/en-ph/explore/tips/philippine-mythical-creatures/63711) - Uncover 13 mythical creatures in Philippine folklore that travellers might encounter. Explore their ...

16. [Lesson 3 Philippine Folk Literature.docx - LESSON 3 Philippine Folk Literature Philippine Mythology Philippine mythical creatures Filipinos believe in | Course Hero](https://www.coursehero.com/file/83324202/Lesson-3-Philippine-Folk-Literaturedocx/) - View Lesson 3 Philippine Folk Literature.docx from EDUCATION 120 at Benguet State University. LESSON...

17. [Maria Makiling - Monster Wiki - Fandom](https://monster.fandom.com/wiki/Maria_Makiling) - Maria Makiling, sometimes spelled Mariang Makiling, in Philippine Mythology, is a diwata or lambana ...

18. [Philippine Mythology - Maria Makiling - Wattpad](https://www.wattpad.com/587186877-philippine-mythology-maria-makiling) - Maria Makiling, in Philippine mythology, is a diwata or lambana (goddess, fairy or forest nymph) ass...

19. [Mariang Sinukuan, the Diwata of Mt. Arayat in Pampanga](https://www.aswangproject.com/mariang-sinukuan/) - Mariang Sinukuan is the diwata, or mountain goddess, associated with Mount Arayat in Pampanga, Phili...

20. [Maria Sinukuan - Wikipedia](https://en.wikipedia.org/wiki/Maria_Sinukuan) - Maria Sinukuan is a fairy or goddess (called a diwata) in the oral stories of Pampanga. She is conne...

21. [Sailing the Golden Ship with Maria Cacao, the Diwata of Filipino ...](https://aurochocolate.com/blogs/community-programs/sailing-the-golden-ship-with-maria-cacao-the-diwata-of-filipino-cacao-culture) - There is a diwata (fairy or goddess) that is associated with cacao. Her name is Maria Cacao or Kakaw...

22. [Maria Cacao - Wikipedia](https://en.wikipedia.org/wiki/Maria_Cacao) - Maria Cacao is the diwata or mountain goddess associated with Mount Lantoy in Argao, Cebu, Philippin...

23. [Bernardo Carpio - Wikipedia](https://en.wikipedia.org/wiki/Bernardo_Carpio)

24. [Bernardo Carpio - Wikiwand](https://www.wikiwand.com/en/articles/Bernardo_Carpio) - Bernardo Carpio is a legendary figure in Philippine mythology who is said to be the cause of earthqu...

25. [Bernardo Carpio : The Mountain Stopper](https://mythlok.com/bernardo-carpio/) - Discover the legend of Bernardo Carpio, the mighty giant of Philippine mythology, whose strength pre...

26. [The Folktales by Damiana L. Eugenio gathers fictional folk ...](https://www.facebook.com/fullybooked/posts/these-are-the-stories-we-grew-up-hearing-but-maybe-never-realized-how-much-they-/1361896449309752/) - The book's introduction of the Bakunawa, a legendary creature in Filipino folklore, is one of its be...

27. [(Aswang, Tikbalang, Kapre, White Lady, and Manananggal)](https://fr.scribd.com/document/465108161/English-MythicalCreatures-Sept-27-2011-docx) - The document provides summaries of 5 mythical creatures from Philippine folklore: 1) The Aswang is a...

28. [Creatures and Monsters of Filipino Folklore](https://www.youtube.com/watch?v=i9HE9HMPnCk) - In this video, we explore mythical creatures and monsters from the Philippines, uncovering legends f...

29. [Creatures of Philippine Lower Mythology - Maximo D. Ramos](https://books.google.com/books/about/Creatures_of_Philippine_Lower_Mythology.html?id=lO-AAAAAMAAJ) - Creatures of Philippine Lower Mythology. Front Cover. Maximo D. Ramos. University of the Philippines...

30. [Creatures & Spirits](https://www.aswangproject.com/creatures/)

