from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag
import re
import requests
import smartLB
import shutil

from PIL import Image, ImageDraw, ImageFont

from enum import Enum

class CardType(Enum):
    NORMAL = 1
    TWINPACT = 2
    SIDEWAYS = 3 # D2 field, DG field


def get_to_ability_text_contents(given_object):
    return_string = ""
    if isinstance(given_object, Tag):
        for thing in given_object.contents:
            return_string += get_to_ability_text_contents(thing)
    if isinstance(given_object, NavigableString):
        return given_object
    return return_string

def paste_ability_text_in_rect(full_ability_text, ABILITY_BOX_TOP_LEFT_CORNER, ABILITY_BOX_BOTTOM_RIGHT_CORNER):
    font_size = 19
    ability_text_image = None
    while True:
        try:
            fnt = ImageFont.truetype("fonts/calibri.ttf", font_size)
            ability_text_image = Image.new("RGB", (ABILITY_BOX_BOTTOM_RIGHT_CORNER[0] - ABILITY_BOX_TOP_LEFT_CORNER[0], ABILITY_BOX_BOTTOM_RIGHT_CORNER[1] - ABILITY_BOX_TOP_LEFT_CORNER[1]), (255, 255, 255))
            smartLB.fit_text(ability_text_image, full_ability_text, (0, 0, 0), fnt)
            break
        except ValueError:
            print("text does not fit")
            font_size -= 1
    return ability_text_image

def get_soup_from_url(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, features="html.parser")
    return soup

def get_card_type_from_soup(soup):
    card_type = CardType.NORMAL
    if len(soup.find_all(title="DG Field")) != 0 or len(soup.find_all(title="D2 Field")) != 0:
        card_type = CardType.SIDEWAYS

    # Extracting ability text
    english_texts = soup.find_all(string="English Text")

    if not len(english_texts) == 1:
        card_type = CardType.TWINPACT
    return card_type

def extract_image_url_from_soup(soup):
    # Get image URL
    # possible_images = soup.find_all(href=re.compile("https://static.wikia.nocookie.net/duelmasters"), name="a")
    possible_images = soup.find_all(href=re.compile("https://static.wikia.nocookie.net/duelmasters"), class_="mw-file-description image")
    print("Possible images: ")
    print(possible_images)

    image_url = ""
    for img in possible_images:
        if img.parent.has_attr('class') and img.parent.name == 'figure':
            image_url = img["href"]
        #image_url = img["href"]
    print("Image url: " + image_url)
    return image_url

def add_text_box_on_image(editing_image, text, ABILITY_BOX_TOP_LEFT_CORNER, ABILITY_BOX_BOTTOM_RIGHT_CORNER):
    # get a drawing context
    d = ImageDraw.Draw(editing_image)
    d.rectangle([ABILITY_BOX_TOP_LEFT_CORNER, ABILITY_BOX_BOTTOM_RIGHT_CORNER], fill=(255, 255, 255, 0))

    # draw multiline text
    ability_text_image = paste_ability_text_in_rect(text, ABILITY_BOX_TOP_LEFT_CORNER, ABILITY_BOX_BOTTOM_RIGHT_CORNER)
    editing_image.paste(ability_text_image, ABILITY_BOX_TOP_LEFT_CORNER)

def extract_ability_text_from_soup(soup, english_text_instance):
    full_ability_text = ""
    english_texts = soup.find_all(string="English Text")
    thing = english_texts[english_text_instance]
    for ability in thing.parent.parent.parent.parent.parent.find_all("td"):
        for part in ability.contents:
            text = get_to_ability_text_contents(part)
            # len(text) == 1 is for a blank line for some reason
            if text.__contains__("English Text") or len(text) == 1:
                continue
            full_ability_text += text
    return full_ability_text.rstrip()

def download_translated_image(URL):
    print("Given URL: " + URL)
    soup = get_soup_from_url(URL)

    card_type = get_card_type_from_soup(soup)

    full_ability_text = extract_ability_text_from_soup(soup, 0)
    full_ability_text2 = ""
    if card_type == CardType.TWINPACT:
        full_ability_text2 = extract_ability_text_from_soup(soup, 1)



    name_split = URL.split("/")
    name = ""
    name_started = False
    for i in name_split:
        if name_started:
            name += i
        if i == "wiki":
            name_started = True
    
    # Download image
    image_url = extract_image_url_from_soup(soup)
    img_data = requests.get(image_url).content
    with open('.\\images\\' + name + ".png", 'wb') as handler:
        handler.write(img_data)

    editing_image = Image.open('.\\images\\' + name + ".png")
    #editing_image = Image.open("Dm24sp2-10.png") # custom image
    print(card_type)

    if card_type == CardType.NORMAL:
        add_text_box_on_image(editing_image, full_ability_text, (40, 600), (600, 810))
    
    if card_type == CardType.TWINPACT:
        add_text_box_on_image(editing_image, full_ability_text, (40, 360), (600, 450))
        add_text_box_on_image(editing_image, full_ability_text2, (40, 700), (600, 800))
    
    if card_type == CardType.SIDEWAYS:
        add_text_box_on_image(editing_image, full_ability_text, (40, 420), (850, 600))
        editing_image = editing_image.rotate(-90, expand=1)

    editing_image.save('.\\images\\' + name + ".png")