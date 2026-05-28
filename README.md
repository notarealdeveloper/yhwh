# yhwh

Biblical Hebrew verb conjugator.

YHWH is not a dictionary. Dictionaries are gay.

YHWH takes a three-letter Hebrew root verb form and applies generative rules.

YHWH defaults to wayyiqtol format.

> But why default wayyiqtol?
>
> said the reader to YHWH.
>
> And YHWH replied
>
> I'll explain why
>
> if you bring a goat to the tabernacle,
>
> else you can die.

Supported verb forms:

- Latin alphabet: `AMR`, `RAH`, `HYH`, `XXX`
- Hebrew alphabet: `אמר`, `ראה`, `היה`, `חחח`
- Paleo Hebrew roots: `𐤀𐤌𐤓`, `𐤇𐤇𐤇` .cte

## Install for development

```sh
make develop
```

## Run

```sh
~ $ yhwh -3ms אמר
ויאמר
~ $ echo AAA | yhwh -3ms
wyAAA
```

## Run without installing

```sh
python -m yhwh --he --story אמר
```

## Test

```sh
make check
```

## Import usage

```python
from yhwh import derive

assert derive("אמר", "story", "3ms") == "ויאמר"
assert derive("ראה", "story", "3fs") == "ותרא"
```

## Philosophy

The goal is not “correct Biblical Hebrew morphology in every case.”
The goal is a programmable toy model matching the derivational grammar style:

```text
ROOT
→ add person marker
→ apply weak-root rewrite rules
→ optionally add story-w
```
