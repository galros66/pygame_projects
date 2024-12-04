from utils.colors import Color

_EMOJI_RANGES = [
    (0x1F600, 0x1F64F),  # Emoticons
    (0x1F300, 0x1F5FF),  # Symbols & Pictographs
    (0x1F680, 0x1F6FF),  # Transport & Map
    (0x1F900, 0x1F9FF),  # Supplemental Symbols & Pictographs
    (0x1F1E6, 0x1F1FF),  # Flags
    (0x2600, 0x26FF),  # Miscellaneous Symbols
    (0x2700, 0x27BF),  # Dingbats
    (0x1FA70, 0x1FAFF),  # Extended Pictographs
]

# Loop through all emoji ranges and print them
ALL_EMOJIS = []
for start, end in _EMOJI_RANGES:
    ALL_EMOJIS.extend(chr(code) for code in range(start, end + 1))

color_emoji_mapping = {
    Color.BLACK: "🖤",  # Black Heart
    Color.GRAY: "🩶",  # Gray Heart
    Color.RED: "❤️",  # Red Heart
    Color.GREEN: "💚",  # Green Heart
    Color.YELLOW: "💛",  # Yellow Heart
    Color.DARK_PURPLE: "🍆",  # Eggplant (Purple)
    Color.ORANGE: "🧡",  # Orange Heart
    Color.PURPLE: "💜",  # Purple Heart
    Color.PINK: "💖",  # Sparkling Heart
    Color.BLUE: "💙",  # Blue Heart
    Color.LIGHT_BLUE: "💙",  # Light Blue Heart
    Color.BROWN: "🤎",  # Brown Heart
    Color.PEACH: "🍑",  # Peach
    Color.WHITE: "🤍",  # White Heart
    Color.BANANA: "🍌",  # Banana
    Color.LIGHT_PEACH: "🍑",  # Light Peach
    Color.NAVY: "💙",  # Navy Blue Heart
    Color.LIGHT_PURPLE: "💜",  # Light Purple Heart
    Color.LIGHT_PINK: "🌸",  # Cherry Blossom (Light Pink)
    Color.LIGHT_ORANGE: "🍊",  # Orange (Light)
    Color.YELLOW_LIME: "🍋",  # Lime
    Color.TURQUOISE: "💎",  # Gem (Turquoise)
    Color.DARK_GREEN: "💚",  # Dark Green Heart
    Color.BORDON: "🍷",  # Wine (Burgundy Color)
    Color.LIGHT_BROWN: "🍂",  # Falling Leaves (Light Brown)
    Color.OLIVE: "🍈",  # Melon (Olive)
    Color.UNIQUE_PURPLE: "💜",  # Unique Purple Heart
    Color.UNIQUE_PINK: "🌷",  # Tulip (Unique Pink)
    Color.LIGHT_YELLOW: "🌼",  # Daisy (Light Yellow)
    Color.OCEAN: "🌊",  # Ocean Wave
    Color.DARK_BLUE: "🌌",  # Milky Way (Dark Blue)
    Color.GRAY2: "🖤",  # Dark Gray Heart
    Color.BANANA2: "🍌",  # Banana
    Color.GREEN2: "🥒",  # Cucumber (Green)
    Color.PURPLE2: "🍆",  # Eggplant (Purple)
}
