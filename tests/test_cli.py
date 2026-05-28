from __future__ import annotations

import subprocess
import sys


def run_yhwh(*args: str, stdin: str | None = None) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "yhwh", *args],
        input=stdin,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout.strip()


def test_cli_standard_hebrew_story_he_says():
    assert run_yhwh("-3", "-m", "--story", "אמר") == "ויאמר"


def test_cli_standard_hebrew_story_she_says():
    assert run_yhwh("-3", "-f", "--story", "אמר") == "ותאמר"


def test_cli_standard_hebrew_completed_i_said():
    assert run_yhwh("-1", "-s", "--completed", "אמר") == "אמרתי"


def test_cli_final_he_story_she_sees():
    assert run_yhwh("--she", "--story", "ראה") == "ותרא"


def test_cli_hyh_completed_i_was():
    assert run_yhwh("-1", "-s", "--completed", "היה") == "הייתי"


def test_cli_initial_l_take_command():
    assert run_yhwh("--you-ms", "--command", "לקח") == "קח"


def test_cli_stdin_multiple_roots():
    out = run_yhwh("--he", "--story", stdin="אמר\nראה\nהיה\n")
    assert out.splitlines() == ["ויאמר", "וירא", "ויהי"]


def test_cli_argv_multiple_roots():
    out = run_yhwh("--he", "--story", "אמר", "ראה", "היה")
    assert out.splitlines() == ["ויאמר", "וירא", "ויהי"]


def test_cli_tsv_output():
    out = run_yhwh("--he", "--story", "--tsv", "אמר", "ראה")
    assert out.splitlines() == ["אמר\tויאמר", "ראה\tוירא"]


def test_cli_derivation_output_contains_rules():
    out = run_yhwh("--he", "--story", "--derivation", "ראה")
    assert "ראה\troot" in out
    assert "יראה\tadd he prefix" in out
    assert "ירא\tweak-final-H short-story rule" in out
    assert "וירא\tadd story-and prefix w" in out
