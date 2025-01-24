from typing import List
from pytest import mark, param

from pydantify.utility.patterns import convert_pattern


@mark.parametrize(
    ("input", "expected"),
    [
        param(
            r"(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}"
            + r"([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
            + r"(%[\p{N}\p{L}]+)?",
            r"(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}"
            + r"([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
            + r"(%[\d\w]+)?",
            id="ietf ipv4-address",
        ),
        param(
            r"\p{L}\p{Lu}\p{Ll}",
            r"\w[A-Z][a-z]",
            id="letters",
        ),
        param(
            r"\P{L}\P{Lu}\P{Ll}",
            r"\W[^A-Z][^a-z]",
            id="no letters",
        ),
        param(
            r"\p{N}\p{Nd}",
            r"\d\d",
            id="numbers",
        ),
        param(
            r"\P{N}\P{Nd}",
            r"\D\D",
            id="no numbers",
        ),
        param(
            r"\p{C}",
            r"[\x00-\x1F\x7F-\x9F]",
            id="control characters",
        ),
        param(
            r"\P{C}",
            r"[^\x00-\x1F\x7F-\x9F]",
            id="no control characters",
        ),
        param(
            r"\p{P}",
            r"[!\"'#$%&\"()*+,\-./:;<=>?@[\\\]^_`{|}~]",
            id="punctuation",
        ),
        param(
            r"\P{P}",
            r"[^!\"'#$%&\"()*+,\-./:;<=>?@[\\\]^_`{|}~]",
            id="no punctuation",
        ),
    ],
)
def test_pattern(input: str, expected: str):
    assert expected == convert_pattern(input)
