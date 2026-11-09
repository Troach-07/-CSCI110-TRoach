from anewalphabet import translate_text


def test_translates_all_lowercase_letters():
    assert translate_text("abcdefghijklmnopqrstuvwxyz") == (
        "@8(|)3#6[-]|_||<1[]\\/[][]\\[]0|D(,)|Z$']['|_|\\/\\/\\/}{`/2"
    )


def test_translates_uppercase_and_mixed_case():
    assert translate_text("Hello World!") == "[-]3110 \\/\\/0|Z1|)!"


def test_preserves_nonletters():
    assert translate_text("123 !?.,\t") == "123 !?.,\t"
