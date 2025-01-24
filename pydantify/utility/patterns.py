translation_map = {
    # https://www.w3.org/TR/2004/REC-xmlschema-2-20041028/#nt-charProp
    r"\p{L}": r"\w",  # All Letters
    r"\P{L}": r"\W",  # All Letters
    r"\p{Lu}": r"[A-Z]",  # uppercase
    r"\P{Lu}": r"[^A-Z]",  # uppercase
    r"\p{Ll}": r"[a-z]",  # uppercase
    r"\P{Ll}": r"[^a-z]",  # uppercase
    r"\p{N}": r"\d",  # All Numbers
    r"\P{N}": r"\D",  # All Numbers
    r"\p{Nd}": r"\d",  # decimal digit
    r"\P{Nd}": r"\D",  # decimal digit
    r"\p{C}": r"[\x00-\x1F\x7F-\x9F]",  # invisible control characters and unused code points
    r"\P{C}": r"[^\x00-\x1F\x7F-\x9F]",  # invisible control characters and unused code points
    r"\p{P}": r"[!\"'#$%&\"()*+,\-./:;<=>?@[\\\]^_`{|}~]",  # punctuation
    r"\P{P}": r"[^!\"'#$%&\"()*+,\-./:;<=>?@[\\\]^_`{|}~]",  # punctuation
}


def convert_pattern(pattern: str) -> str:
    """
    Convert xmlschema pattern into python regex.
    ToDo: This is just a quick fix and need to be done better
    """
    for search, replace in translation_map.items():
        pattern = pattern.replace(search, replace)
    return pattern
