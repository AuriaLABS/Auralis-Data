"""Stage 7 PII placeholders and stage 10 split assignment."""

from __future__ import annotations

import re

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")
IPV4_RE = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b")
IPV6_RE = re.compile(r"\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b")
IBAN_ES_RE = re.compile(r"\bES\d{22}\b")
DNI_RE = re.compile(r"\b(\d{8})([A-Za-z])\b")
NIE_RE = re.compile(r"\b([XYZxyz])(\d{7})([A-Za-z])\b")
PHONE_RE = re.compile(r"\+34[\s\-]?(?:6|7)\d{2}[\s\-]?\d{3}[\s\-]?\d{3}\b")
DNI_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"
NIE_PREFIX = {"X": "0", "Y": "1", "Z": "2"}


def valid_dni(number: str, letter: str) -> bool:
    return DNI_LETTERS[int(number) % 23] == letter.upper()


def valid_nie(prefix: str, number: str, letter: str) -> bool:
    mapped = NIE_PREFIX.get(prefix.upper())
    if mapped is None:
        return False
    return valid_dni(mapped + number, letter)


def redact_pii(text: str) -> tuple[str, list[str]]:
    tags: list[str] = []

    def stamp(kind: str, token: str):
        def _fn(_m: re.Match) -> str:
            tags.append(kind)
            return token

        return _fn

    def dni(m: re.Match) -> str:
        if not valid_dni(m.group(1), m.group(2)):
            return m.group(0)
        tags.append("id")
        return "<ID>"

    def nie(m: re.Match) -> str:
        if not valid_nie(m.group(1), m.group(2), m.group(3)):
            return m.group(0)
        tags.append("id")
        return "<ID>"

    text = EMAIL_RE.sub(stamp("email", "<EMAIL>"), text)
    text = IPV6_RE.sub(stamp("ip", "<IP>"), text)
    text = IPV4_RE.sub(stamp("ip", "<IP>"), text)
    text = IBAN_ES_RE.sub(stamp("iban", "<IBAN>"), text)
    text = PHONE_RE.sub(stamp("phone", "<PHONE>"), text)
    text = NIE_RE.sub(nie, text)
    text = DNI_RE.sub(dni, text)
    return text, tags


def assign_split(digest: str, val: float = 0.05, test: float = 0.05) -> str:
    n = int(digest[:8], 16) / 0xFFFFFFFF
    if n < test:
        return "test"
    if n < test + val:
        return "validation"
    return "train"
