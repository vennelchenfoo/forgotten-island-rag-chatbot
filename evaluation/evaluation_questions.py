# Philippine mythology evaluation questions with ground-truth answers.
# Derived directly from the source documents in data/.
# Keep this list short during cost-sensitive runs; comment out questions
# you don't need and uncomment them for a full evaluation.

EVALUATION_DATA: list[dict[str, str]] = [
    {
        "question": "What is the Manananggal and how does it attack its victims?",
        "ground_truth": (
            "The Manananggal is an aswang-type viscera-sucker and flying torso "
            "found in Tagalog provinces, Bicol, and the Visayas. At night its "
            "upper torso separates from its lower body, grows bat-like wings, "
            "and flies above houses. It uses a long thread-like tongue to suck "
            "the fetuses or viscera of pregnant women through roof cracks or "
            "windows."
        ),
    },
    {
        "question": "How can you defeat or ward off the Manananggal?",
        "ground_truth": (
            "The most effective folk method is to find the Manananggal's "
            "abandoned lower torso and sprinkle it with salt, garlic, ash, or "
            "sand so the creature cannot reattach at sunrise and dies. "
            "Protective measures include keeping lights on, closing windows, "
            "and placing sharp or pungent items near doors and windows."
        ),
    },
    {
        "question": "What is the Tikbalang and what powers does it have?",
        "ground_truth": (
            "The Tikbalang is a forest trickster found in mountain passes and "
            "forest paths across Tagalog, Ilocano, and other lowland areas. "
            "It is a tall, emaciated humanoid with a horse's head, hooves, and "
            "long limbs. It can confuse travelers and make them walk in circles. "
            "Counter-rituals include turning clothes inside-out or politely "
            "asking it for directions."
        ),
    },
    {
        "question": "What role does the Bakunawa play in Philippine mythology?",
        "ground_truth": (
            "The Bakunawa is a giant sea serpent or serpentine dragon in "
            "Visayan and Bicolano lore associated with eclipses. It is said to "
            "have devoured six of the original seven moons. People would bang "
            "pots and gongs to make it release the last remaining moon. "
            "It provides a mythological explanation for lunar eclipses and "
            "inspired noise-making rituals and festivals like Halia in Bicol."
        ),
    },
    {
        "question": "Who is Maria Makiling and what is her domain?",
        "ground_truth": (
            "Maria Makiling is a mountain diwata or nature spirit who guards "
            "Mount Makiling in Laguna. She is described as a beautiful, ageless "
            "woman with long hair who protects the animals, forests, and weather "
            "of her mountain. Her themes include fertility, generosity, and the "
            "punishment of greed. She is widely interpreted as a pre-colonial "
            "Tagalog goddess that survived the Hispanic period."
        ),
    },
    {
        "question": "What are the five main aspects of the Aswang?",
        "ground_truth": (
            "The Aswang is an umbrella term for malevolent shape-shifters "
            "encompassing five main aspects: a blood-sucking vampire, a "
            "self-segmenting viscera-sucker, a man-eating weredog or other "
            "beast, a vindictive witch, and a corpse-eating ghoul. It can "
            "appear human by day but transforms at night and can sense the "
            "scent of sickness and death from afar."
        ),
    },
    {
        "question": "What is the daily-life significance of the Nuno sa Punso?",
        "ground_truth": (
            "The Nuno sa Punso is a small elder spirit with a large head that "
            "dwells in mounds and anthills. It can inflict swelling, fever, or "
            "deformities on anyone who disturbs its home. The strict daily-life "
            "rule is to never kick, sit on, or urinate near mounds, and to "
            "always say 'tabi-tabi po' when passing. Unexplained swelling or "
            "skin conditions may be diagnosed as 'natapakan ang nuno' and "
            "treated through an albularyo's rituals."
        ),
    },
    {
        "question": (
            "What is the Forgotten Island film about and how does it connect "
            "to Philippine mythology?"
        ),
        "ground_truth": (
            "Forgotten Island is a 2026 DreamWorks Animation film releasing "
            "September 25, 2026. It follows two lifelong best friends, Jo and "
            "Raissa, who become stranded on the mystical world of Nakali, where "
            "their only escape may cost them their shared lifetime of memories. "
            "The film is described as a broad party comedy adventure set on a "
            "magical island rooted in Philippine mythology, drawing on motifs "
            "such as forest giants, dwarfs, merfolk, aswang, and diwata."
        ),
    },
]
