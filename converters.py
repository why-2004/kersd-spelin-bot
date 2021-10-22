import re

from dragonmapper import hanzi

from wiktionaryparser import WiktionaryParser

from eng_to_ipa import jonvert as convert_to_ipa

kerct = {'m': 'm', 'n': 'n', 'ñ': 'ŋ', 'p': 'p', 't': 't', 'q': 'ʧ', 'k': 'k', 'b': 'b', 'd': 'd', 'j': 'ʤ', 'g': 'g',
         'f': 'f', 'č': 'θ', 'c': 's', 's': 'ʃ', 'h': 'h', 'v': 'v', 'ž': 'ð', 'z': 'z', 'x': 'ʒ', 'l': 'l', 'r': 'r',
         'y': 'j', 'w': 'w', 'a': 'a', 'ä': 'æ', 'e': 'ə', 'ë': 'ɛ', 'ē': 'ɜː', 'o': 'ɒ', 'i': 'ɪ', 'ī': 'iː',
         'u': 'ʊ', 'ū': 'uː', 'ö': 'ˈəʊ'}
ipa = {'m': 'm', 'n': 'n', 'ŋ': 'ñ', 'p': 'p', 't': 't', 'ʧ': 'q', 'k': 'k', 'b': 'b', 'd': 'd', 'ʤ': 'j', 'g': 'g',
       'f': 'f', 'θ': 'č', 's': 'c', 'ʃ': 's', 'h': 'h', 'v': 'v', 'ð': 'ž', 'z': 'z', 'ʒ': 'x', 'l': 'l', 'r': 'r',
       'j': 'y', 'w': 'w', 'a': 'a', 'æ': 'ä', 'ə': 'e', 'ɛ': 'ë', 'ɜ': 'ē', 'ɒ': 'o', 'ɪ': 'i', 'i': 'ī', 'ʊ': 'u',
       'u': 'ū', 'ö': 'ö', 'ː': '', 'ˈ': '', 'ˌ': '', '.': '', 'ɹ': 'r', 'ɚ': 'e',
       'ʌ': 'a', 'ɑ': 'a', 'ɔ': 'o'}  # must replace "ˈəʊ" with ö


def ipa_to_kerct(text):
    output = ""
    arg = re.sub("ˈəʊ", 'ö', text)
    arg = re.sub("[(][^)]+[)]", "", arg)
    arg = re.sub("t͡ʃ", "ʧ", arg)
    arg = re.sub("tʃ", "ʧ", arg)
    arg = re.sub("d͡ʒ", "ʤ", arg)
    for i in arg.split(" "):
        for j in i:
            if j in ipa:
                output += ipa[j]
            else:
                output += j
        output += " "
    return output


def kerct_to_ipa(text):
    output = ""
    for i in text.split(" "):
        for j in i:
            if j in kerct:
                output += kerct[j]
            else:
                output += j
        output += " "
    return output


def eng_to_ipa(text):
    if len(text.split(" ")) > 20:
        return convert_to_ipa(text)

    output = ""
    for i in text.split(" "):
        word = word_to_ipa(i, 'english')
        if word == "":
            output += convert_to_ipa(i)
        else:
            output += word
        output += " "
    return output[:-1]


def lang_to_ipa(text, language):
    output = ""
    for i in text.split(" "):
        word = word_to_ipa(i, language)
        if word == "":
            output += "__" + i + "__"
        else:
            output += word
        output += " "
    return output[:-1]


def word_to_ipa(word, language):
    print(word)
    parser = WiktionaryParser()
    parser.set_default_language(language)
    word = parser.fetch(word)
    if word:
        print(word[0]['pronunciations']['text'])
        for j in word[0]['pronunciations']['text']:
            # match=re.search("^((?![(]US[)] IPA: ).)*[/][^/]+/", j)
            match = re.search("[/][^/]+/", j)
            if match:
                return match[0][1:-1]
    return ""


def eng_to_kerct(text):
    return ipa_to_kerct(eng_to_ipa(text))


def remove_vowels(text):
    output = ""
    for i in text.split(" "):
        for j in i:
            if not re.match('[aeiouAEIOU]', j):
                output += j
        output += " "
    return


def han_to_ipa(text):
    return hanzi.to_ipa(text)


def han_to_zhu(text):
    return hanzi.to_zhuyin(text)


def han_to_pin(text):
    return hanzi.to_pinyin(text)
