from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ScriptKind = Literal["latin", "hebrew", "paleo"]


@dataclass(frozen=True)
class Alphabet:
    kind: ScriptKind
    aleph: str
    ayin: str
    he: str
    heth: str
    yod: str
    waw: str
    tav: str
    nun: str
    mem_final: str
    nun_final: str
    lamed: str
    prefix_a: str
    prefix_y: str
    prefix_t: str
    prefix_n: str
    prefix_w: str
    prefix_m: str
    prefix_l: str
    suffix_h: str
    suffix_i: str
    suffix_w: str
    suffix_t: str
    suffix_nw: str
    suffix_tm: str
    suffix_tn: str
    suffix_nh: str
    suffix_im: str
    suffix_wt: str


LATIN = Alphabet(
    kind="latin",
    aleph="A",
    ayin="O",
    he="H",
    heth="X",
    yod="Y",
    waw="W",
    tav="T",
    nun="N",
    mem_final="m",
    nun_final="n",
    lamed="L",
    prefix_a="a",
    prefix_y="y",
    prefix_t="t",
    prefix_n="n",
    prefix_w="w",
    prefix_m="m",
    prefix_l="l",
    suffix_h="h",
    suffix_i="i",
    suffix_w="w",
    suffix_t="t",
    suffix_nw="nw",
    suffix_tm="tm",
    suffix_tn="tn",
    suffix_nh="nh",
    suffix_im="im",
    suffix_wt="wt",
)

HEBREW = Alphabet(
    kind="hebrew",
    aleph="א",
    ayin="ע",
    he="ה",
    heth="ח",
    yod="י",
    waw="ו",
    tav="ת",
    nun="נ",
    mem_final="ם",
    nun_final="ן",
    lamed="ל",
    prefix_a="א",
    prefix_y="י",
    prefix_t="ת",
    prefix_n="נ",
    prefix_w="ו",
    prefix_m="מ",
    prefix_l="ל",
    suffix_h="ה",
    suffix_i="י",
    suffix_w="ו",
    suffix_t="ת",
    suffix_nw="נו",
    suffix_tm="תם",
    suffix_tn="תן",
    suffix_nh="נה",
    suffix_im="ים",
    suffix_wt="ות",
)

PALEO = Alphabet(
    kind="paleo",
    aleph="𐤀",
    ayin="𐤏",
    he="𐤄",
    heth="𐤇",
    yod="𐤉",
    waw="𐤅",
    tav="𐤕",
    nun="𐤍",
    mem_final="𐤌",
    nun_final="𐤍",
    lamed="𐤋",
    prefix_a="𐤀",
    prefix_y="𐤉",
    prefix_t="𐤕",
    prefix_n="𐤍",
    prefix_w="𐤅",
    prefix_m="𐤌",
    prefix_l="𐤋",
    suffix_h="𐤄",
    suffix_i="𐤉",
    suffix_w="𐤅",
    suffix_t="𐤕",
    suffix_nw="𐤍𐤅",
    suffix_tm="𐤕𐤌",
    suffix_tn="𐤕𐤍",
    suffix_nh="𐤍𐤄",
    suffix_im="𐤉𐤌",
    suffix_wt="𐤅𐤕",
)

HEBREW_CHARS = set("אבגדהוזחטיכךלמםנןסעפףצץקרשת")
PALEO_CHARS = set("𐤀𐤁𐤂𐤃𐤄𐤅𐤆𐤇𐤈𐤉𐤊𐤋𐤌𐤍𐤎𐤏𐤐𐤑𐤒𐤓𐤔𐤕")

Person = Literal["1s", "2ms", "2fs", "3ms", "3fs", "1p", "2mp", "2fp", "3mp", "3fp"]
Conjugation = Literal[
    "completed",
    "prefix",
    "story",
    "command",
    "participle",
    "passive",
    "infinitive",
    "infinitive-bare",
]


def detect_alphabet(root: str) -> Alphabet:
    if any(ch in PALEO_CHARS for ch in root):
        return PALEO
    if any(ch in HEBREW_CHARS for ch in root):
        return HEBREW
    return LATIN


def normalize_root(raw: str) -> str:
    root = raw.strip()
    if not root:
        raise ValueError("empty root")
    return root


def is_final_he(root: str, a: Alphabet) -> bool:
    return root.endswith(a.he)


def is_middle_wy(root: str, a: Alphabet) -> bool:
    return len(root) == 3 and root[1] in {a.waw, a.yod}


def is_initial_n(root: str, a: Alphabet) -> bool:
    return root.startswith(a.nun)


def is_initial_y(root: str, a: Alphabet) -> bool:
    return root.startswith(a.yod)


def is_initial_l(root: str, a: Alphabet) -> bool:
    return root.startswith(a.lamed)


def drop_final_he(root: str, a: Alphabet) -> str:
    return root[:-1] if is_final_he(root, a) else root


def final_he_to_y(root: str, a: Alphabet) -> str:
    return root[:-1] + a.yod if is_final_he(root, a) else root


def drop_initial(root: str) -> str:
    return root[1:]


def drop_middle(root: str) -> str:
    return root[0] + root[2]


def completed(root: str, person: Person, a: Alphabet) -> str:
    if person == "3ms":
        return root

    if person == "3fs":
        if is_final_he(root, a):
            return drop_final_he(root, a) + a.suffix_t + a.suffix_h
        return root + a.suffix_h

    if person in {"1s", "2ms", "2fs", "1p", "2mp", "2fp"}:
        suffix = {
            "1s": a.suffix_t + a.suffix_i,
            "2ms": a.suffix_t,
            "2fs": a.suffix_t,
            "1p": a.suffix_nw,
            "2mp": a.suffix_tm,
            "2fp": a.suffix_tn,
        }[person]
        if is_final_he(root, a):
            return final_he_to_y(root, a) + suffix
        return root + suffix

    if person in {"3mp", "3fp"}:
        if is_final_he(root, a):
            return drop_final_he(root, a) + a.suffix_w
        return root + a.suffix_w

    raise ValueError(f"unknown person: {person}")


def prefix_base(root: str, person: Person, a: Alphabet, *, short: bool = False) -> str:
    prefix = {
        "1s": a.prefix_a,
        "2ms": a.prefix_t,
        "2fs": a.prefix_t,
        "3ms": a.prefix_y,
        "3fs": a.prefix_t,
        "1p": a.prefix_n,
        "2mp": a.prefix_t,
        "2fp": a.prefix_t,
        "3mp": a.prefix_y,
        "3fp": a.prefix_t,
    }[person]

    stem = root

    if is_initial_n(root, a) or is_initial_y(root, a) or is_initial_l(root, a):
        stem = drop_initial(root)

    if short and is_middle_wy(root, a):
        stem = drop_middle(root)

    if short and is_final_he(root, a) and person in {"3ms", "3fs"}:
        stem = drop_final_he(root, a)

    form = prefix + stem

    if person == "2fs":
        form += a.suffix_i
    elif person in {"2mp", "3mp"}:
        if is_final_he(root, a):
            form = prefix + drop_final_he(root, a) + a.suffix_w
        else:
            form += a.suffix_w
    elif person in {"2fp", "3fp"}:
        form += a.suffix_nh

    if person == "1s" and root.startswith(a.aleph):
        form = root

    return form


def prefix_live(root: str, person: Person, a: Alphabet) -> str:
    return prefix_base(root, person, a, short=False)


def story(root: str, person: Person, a: Alphabet) -> str:
    return a.prefix_w + prefix_base(root, person, a, short=True)


def command(root: str, person: Person, a: Alphabet) -> str:
    if person not in {"2ms", "2fs", "2mp", "2fp"}:
        raise ValueError("command only supports 2ms, 2fs, 2mp, 2fp")

    base = root
    if is_initial_l(root, a):
        base = drop_initial(root)

    if person == "2ms":
        return base
    if person == "2fs":
        if is_final_he(root, a):
            return final_he_to_y(root, a) + a.suffix_i
        return base + a.suffix_i
    if person == "2mp":
        if is_final_he(root, a):
            return drop_final_he(root, a) + a.suffix_w
        return base + a.suffix_w
    if person == "2fp":
        return base + a.suffix_nh

    raise AssertionError("unreachable")


def participle(root: str, person: Person, a: Alphabet) -> str:
    base = a.prefix_m + root
    if person == "3ms":
        return base
    if person == "3fs":
        return base + a.suffix_t
    if person == "3mp":
        return base + a.suffix_im
    if person == "3fp":
        return base + a.suffix_wt
    raise ValueError("participle supports 3ms/ms, 3fs/fs, 3mp/mp, 3fp/fp only")


def passive_adj(root: str, person: Person, a: Alphabet) -> str:
    if len(root) == 3:
        base = root[0] + a.waw + root[1:]
    else:
        base = root

    if person == "3ms":
        return base
    if person == "3fs":
        return base + a.suffix_h
    if person == "3mp":
        return base + a.suffix_im
    if person == "3fp":
        return base + a.suffix_wt
    raise ValueError("passive adjective supports 3ms/ms, 3fs/fs, 3mp/mp, 3fp/fp only")


def infinitive(root: str, a: Alphabet, *, with_l: bool = True) -> str:
    if is_final_he(root, a):
        body = drop_final_he(root, a) + a.waw + a.tav
    else:
        body = root
    return a.prefix_l + body if with_l else body


def derive(root: str, conjugation: Conjugation = "story", person: Person = "3ms") -> str:
    root = normalize_root(root)
    a = detect_alphabet(root)

    if conjugation == "completed":
        return completed(root, person, a)
    if conjugation == "prefix":
        return prefix_live(root, person, a)
    if conjugation == "story":
        return story(root, person, a)
    if conjugation == "command":
        return command(root, person, a)
    if conjugation == "participle":
        return participle(root, person, a)
    if conjugation == "passive":
        return passive_adj(root, person, a)
    if conjugation == "infinitive":
        return infinitive(root, a, with_l=True)
    if conjugation == "infinitive-bare":
        return infinitive(root, a, with_l=False)

    raise ValueError(f"unknown conjugation: {conjugation}")


def rough_derivation(root: str, conjugation: Conjugation, person: Person) -> list[tuple[str, str]]:
    a = detect_alphabet(root)
    rows: list[tuple[str, str]] = [(root, "root")]

    if conjugation == "completed":
        if person == "3ms":
            rows.append((root, "he-completed form has no added consonant"))
        elif person == "3fs":
            rows.append((root + a.suffix_t + a.suffix_h, "add she-completed suffix th"))
            if is_final_he(root, a):
                rows.append((drop_final_he(root, a) + a.suffix_t + a.suffix_h, "weak-final-H rule: root-final H drops before th"))
            else:
                rows.append((root + a.suffix_h, "standard she-completed suffix h"))
        elif person in {"1s", "2ms", "2fs", "1p", "2mp", "2fp"}:
            suffix = {
                "1s": a.suffix_t + a.suffix_i,
                "2ms": a.suffix_t,
                "2fs": a.suffix_t,
                "1p": a.suffix_nw,
                "2mp": a.suffix_tm,
                "2fp": a.suffix_tn,
            }[person]
            rows.append((root + suffix, f"add {person}-completed suffix"))
            if is_final_he(root, a):
                rows.append((final_he_to_y(root, a) + suffix, "weak-final-H rule: final H becomes Y before this suffix"))
        elif person in {"3mp", "3fp"}:
            rows.append((root + a.suffix_w, "add they-completed suffix w"))
            if is_final_he(root, a):
                rows.append((drop_final_he(root, a) + a.suffix_w, "weak-final-H rule: root-final H drops before w"))

    elif conjugation in {"prefix", "story"}:
        pfx = {
            "1s": a.prefix_a,
            "2ms": a.prefix_t,
            "2fs": a.prefix_t,
            "3ms": a.prefix_y,
            "3fs": a.prefix_t,
            "1p": a.prefix_n,
            "2mp": a.prefix_t,
            "2fp": a.prefix_t,
            "3mp": a.prefix_y,
            "3fp": a.prefix_t,
        }[person]

        names = {
            "1s": "I",
            "2ms": "you",
            "2fs": "you",
            "3ms": "he",
            "3fs": "she",
            "1p": "we",
            "2mp": "you-all",
            "2fp": "you-all-f",
            "3mp": "they",
            "3fp": "they-f",
        }

        short = conjugation == "story"
        stem = root
        form = pfx + stem
        rows.append((form, f"add {names[person]} prefix"))

        if is_initial_n(root, a) or is_initial_y(root, a) or is_initial_l(root, a):
            stem = drop_initial(root)
            form = pfx + stem
            rows.append((form, "weak-initial rule: first root letter drops after prefix"))

        if short and is_middle_wy(root, a):
            stem = drop_middle(root)
            form = pfx + stem
            rows.append((form, "middle-w/y short-story rule: middle W/Y drops"))

        if short and is_final_he(root, a) and person in {"3ms", "3fs"}:
            stem = drop_final_he(root, a)
            form = pfx + stem
            rows.append((form, "weak-final-H short-story rule: final H drops"))

        if person == "2fs":
            form += a.suffix_i
            rows.append((form, "add feminine singular suffix i"))
        elif person in {"2mp", "3mp"}:
            if is_final_he(root, a):
                form = pfx + drop_final_he(root, a) + a.suffix_w
                rows.append((form, "weak-final-H plural rule: final H drops before w"))
            else:
                form += a.suffix_w
                rows.append((form, "add plural suffix w"))
        elif person in {"2fp", "3fp"}:
            form += a.suffix_nh
            rows.append((form, "add feminine plural suffix nh"))

        if person == "1s" and root.startswith(a.aleph):
            form = root
            rows.append((form, "A-root rule: I-prefix A plus root-initial A collapses to one A"))

        if conjugation == "story":
            rows.append((a.prefix_w + form, "add story-and prefix w"))

    elif conjugation == "command":
        form = root
        if is_initial_l(root, a):
            form = drop_initial(root)
            rows.append((form, "weak-initial-L short-command rule: initial L drops"))

        if person == "2ms":
            rows.append((form, "masculine singular command has no added consonant"))
        elif person == "2fs":
            form = (final_he_to_y(root, a) if is_final_he(root, a) else form) + a.suffix_i
            rows.append((form, "add feminine command suffix i"))
        elif person == "2mp":
            form = (drop_final_he(root, a) if is_final_he(root, a) else form) + a.suffix_w
            rows.append((form, "add plural command suffix w"))
        elif person == "2fp":
            form = form + a.suffix_nh
            rows.append((form, "add feminine plural command suffix nh"))

    elif conjugation in {"participle", "passive", "infinitive", "infinitive-bare"}:
        rows.append((derive(root, conjugation, person), f"apply {conjugation} rule"))

    return rows
