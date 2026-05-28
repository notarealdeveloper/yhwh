# yhwh

Tiny rule-based Biblical Hebrew-ish verb generator.

This is deliberately **not** a verb dictionary. It takes a three-letter root-like string and applies broad generative rules.

Supported root scripts:

- Latin logical roots: `AMR`, `RAH`, `HYH`, `XXX`
- Hebrew roots: `אמר`, `ראה`, `היה`, `חחח`
- Paleo Hebrew roots: `𐤀𐤌𐤓`, `𐤇𐤇𐤇`

## Install for development

```bash
make develop
```

## Run

```bash
yhwh --he --story אמר
# ויאמר

yhwh --she --story ראה
# ותרא

echo "אמר
ראה
היה" | yhwh --he --story
# ויאמר
# וירא
# ויהי
```

## Run without installing

```bash
python -m yhwh --he --story אמר
```

## Test

```bash
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
