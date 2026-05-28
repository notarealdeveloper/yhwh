#!/usr/bin/env python

import sys
import argparse

from .core import Conjugation, Person, derive, normalize_root, rough_derivation


PERSONS = ("1s", "2ms", "2fs", "3ms", "3fs", "1p", "2mp", "2fp", "3mp", "3fp")


def read_roots(args_roots: list[str]) -> list[str]:
    if args_roots:
        return [normalize_root(x) for x in args_roots]
    return [normalize_root(line) for line in sys.stdin if line.strip()]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="yhwh",
        description="Generate rough Biblical Hebrew verb forms from 3-letter roots by rule.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    p.add_argument("roots", nargs="*", help="3-character roots. If absent, read stdin.")

    g = p.add_argument_group("person")
    g.add_argument("-1", "--first", action="store_const", const="1", dest="person_num", help="1st person")
    g.add_argument("-2", "--second", action="store_const", const="2", dest="person_num", help="2nd person")
    g.add_argument("-3", "--third", action="store_const", const="3", dest="person_num", help="3rd person")
    g.add_argument("-s", "--singular", action="store_const", const="s", dest="number", help="singular")
    g.add_argument("-p", "--plural", action="store_const", const="p", dest="number", help="plural")
    g.add_argument("-m", "--masculine", action="store_const", const="m", dest="gender", help="masculine")
    g.add_argument("-f", "--feminine", action="store_const", const="f", dest="gender", help="feminine")

    # compact person flags: yhwh -3ms, yhwh -1p, etc.
    for code in PERSONS:
        g.add_argument(
            f"-{code}",
            dest="person_alias",
            action="store_const",
            const=code,
            help=f"alias for --person {code}",
        )

    g.add_argument("--person", choices=PERSONS, help="direct person code")
    g.add_argument("--I", dest="person_alias", action="store_const", const="1s", help="alias for --person 1s")
    g.add_argument("--you-ms", dest="person_alias", action="store_const", const="2ms")
    g.add_argument("--you-fs", dest="person_alias", action="store_const", const="2fs")
    g.add_argument("--he", dest="person_alias", action="store_const", const="3ms")
    g.add_argument("--she", dest="person_alias", action="store_const", const="3fs")
    g.add_argument("--we", dest="person_alias", action="store_const", const="1p")
    g.add_argument("--yous-m", dest="person_alias", action="store_const", const="2mp")
    g.add_argument("--yous-f", dest="person_alias", action="store_const", const="2fp")
    g.add_argument("--they-m", dest="person_alias", action="store_const", const="3mp")
    g.add_argument("--they-f", dest="person_alias", action="store_const", const="3fp")

    c = p.add_argument_group("conjugation / form")
    c.add_argument("-c", "--completed", action="store_const", const="completed", dest="conjugation", help="completed/suffix form")
    c.add_argument("-l", "--live", "--prefix", action="store_const", const="prefix", dest="conjugation", help="prefix/live/future-ish form")
    c.add_argument("-S", "--story", action="store_const", const="story", dest="conjugation", help="story-present chain form")
    c.add_argument("-C", "--command", action="store_const", const="command", dest="conjugation", help="command/imperative")
    c.add_argument("-P", "--participle", action="store_const", const="participle", dest="conjugation", help="participle / X-ing adjective")
    c.add_argument("-E", "--passive", action="store_const", const="passive", dest="conjugation", help="passive / XXXed adjective")
    c.add_argument("-i", "--infinitive", action="store_const", const="infinitive", dest="conjugation", help="to XXX")
    c.add_argument("-b", "--bare-infinitive", action="store_const", const="infinitive-bare", dest="conjugation", help="bare infinitive body")

    p.add_argument("-d", "--derivation", action="store_true", help="print rough derivation chain instead of only final form")
    p.add_argument("--tsv", action="store_true", help="print root<TAB>form")
    p.set_defaults(conjugation="story")
    return p


def infer_person(ns: argparse.Namespace) -> Person:
    if ns.person_alias:
        return ns.person_alias
    if ns.person:
        return ns.person

    num = ns.person_num or "3"
    number = ns.number or "s"
    gender = ns.gender

    if num == "1":
        return "1s" if number == "s" else "1p"

    if num == "2":
        if number == "s":
            return "2fs" if gender == "f" else "2ms"
        return "2fp" if gender == "f" else "2mp"

    if num == "3":
        if number == "s":
            return "3fs" if gender == "f" else "3ms"
        return "3fp" if gender == "f" else "3mp"

    raise ValueError("could not infer person")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(argv)
    person = infer_person(ns)
    conjugation: Conjugation = ns.conjugation

    roots = read_roots(ns.roots)
    if not roots:
        parser.error("no roots supplied on argv or stdin")

    for root in roots:
        try:
            form = derive(root, conjugation, person)
            if ns.derivation:
                print(f"# {root} -> {form}")
                for f, rule in rough_derivation(root, conjugation, person):
                    print(f"{f}\t{rule}")
            elif ns.tsv:
                print(f"{root}\t{form}")
            else:
                print(form)
        except Exception as e:
            print(f"yhwh: {root}: {e}", file=sys.stderr)
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
