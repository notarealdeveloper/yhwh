from yhwh import derive, rough_derivation


def test_import_standard_story_he_says():
    assert derive("אמר", "story", "3ms") == "ויאמר"


def test_import_standard_story_she_says():
    assert derive("אמר", "story", "3fs") == "ותאמר"


def test_import_standard_story_they_say():
    assert derive("אמר", "story", "3mp") == "ויאמרו"


def test_import_final_he_story_he_sees():
    assert derive("ראה", "story", "3ms") == "וירא"


def test_import_final_he_story_she_sees():
    assert derive("ראה", "story", "3fs") == "ותרא"


def test_import_final_he_completed_i_saw():
    assert derive("ראה", "completed", "1s") == "ראיתי"


def test_import_hyh_story_it_happens():
    assert derive("היה", "story", "3ms") == "ויהי"


def test_import_hyh_infinitive():
    assert derive("היה", "infinitive", "3ms") == "להיות"


def test_import_initial_l_take_story():
    assert derive("לקח", "story", "3ms") == "ויקח"


def test_import_initial_n_give_story():
    assert derive("נתן", "story", "3ms") == "ויתן"


def test_import_middle_w_come_story():
    assert derive("בוא", "story", "3ms") == "ויבא"


def test_import_latin_final_h_completed_i():
    assert derive("XXH", "completed", "1s") == "XXYti"


def test_import_paleo_story_he():
    assert derive("𐤇𐤇𐤇", "story", "3ms") == "𐤅𐤉𐤇𐤇𐤇"


def test_rough_derivation_mentions_weak_rule():
    rows = rough_derivation("ראה", "story", "3ms")
    assert ("ראה", "root") in rows
    assert ("יראה", "add he prefix") in rows
    assert ("ירא", "weak-final-H short-story rule: final H drops") in rows
    assert ("וירא", "add story-and prefix w") in rows
