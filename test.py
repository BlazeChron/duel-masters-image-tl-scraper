from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag

def get_to_ability_text_contents(given_object):
    return_string = ""
    if isinstance(given_object, Tag):
        for thing in given_object.contents:
            return_string += get_to_ability_text_contents(thing)
    if isinstance(given_object, NavigableString):
        return given_object
    return return_string

f = open("check.html", "r", encoding="utf8")


soup = BeautifulSoup(f.read(), features="html.parser")

f.close()

full_ability_text = ""
english_texts = soup.find_all(string="English Text")
thing = english_texts[0]
for ability in thing.parent.parent.parent.parent.parent.find_all("td"):
    for part in ability.contents:
        text = get_to_ability_text_contents(part)
        if text.__contains__("English Text") or len(text) == 1:
            continue
        full_ability_text += text

print(full_ability_text)