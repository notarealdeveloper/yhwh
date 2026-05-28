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

## Test

```sh
make check
```

## Import usage

```python
>>> from yhwh import derive
>>> yhwh.derive("אמר")
'ויאמר'

```

## Philosophy

The goal is not “correct Biblical Hebrew morphology in every case.”
The goal is a model of the generative grammar of biblical hebrew,
that works and is accurate in as many cases as possible,
until we get tired and too drunk to aerflnksידעme
EOF
