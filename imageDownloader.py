from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag
import re
import requests
import smartLB

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
    possible_images = soup.find_all(href=re.compile("https://static.wikia.nocookie.net/duelmasters"), name="a")

    image_url = ""
    for img in possible_images:
        if img.parent.has_attr('class') and img.parent.name == 'div':
            image_url = img["href"]
    print(image_url)
    return image_url


def download_translated_image(URL):
    print("Given URL: " + URL)
    soup = get_soup_from_url(URL)

    card_type = get_card_type_from_soup(soup)

    # Extracting ability text
    english_texts = soup.find_all(string="English Text")

    thing = english_texts[0]

    full_ability_text = ""
    full_ability_text2 = ""
    for ability in thing.parent.parent.parent.parent.parent.find_all("p"):
        for part in ability.contents:
            full_ability_text += get_to_ability_text_contents(part)
    
#     full_ability_text = '''Blocker Blocker ​■ Double breaker

# ■ When you put this creature, choose 2 of the following. (You may choose the same one twice.)

# ► Choose one of your opponent's creatures. That creature gets -4000 power until the end of the turn.
# ► Put the top 4 cards of your deck into your graveyard.
# ► Put a creature that costs 4 or less from your graveyard.
# ■ When this creature would leave, you may destroy one of your other creatures instead.'''

    if card_type == CardType.TWINPACT:
        thing = english_texts[1]
        for ability in thing.parent.parent.parent.parent.parent.find_all("p"):
            for part in ability.contents:
                full_ability_text2 += get_to_ability_text_contents(part)
        #full_ability_text2 = ''' use this for other text if not working properly '''

    
    # Download image
    image_url = extract_image_url_from_soup(soup)
    img_data = requests.get(image_url).content
    with open('temp_img.png', 'wb') as handler:
        handler.write(img_data)


    editing_image = Image.open("temp_img.png")
    #editing_image = Image.open("Dm24sp2-10.png") # custom image
    print(card_type)

    if card_type == CardType.NORMAL:
        # edit image
        # The two images I sampled are 650x908

        # get a drawing context
        d = ImageDraw.Draw(editing_image)


        ABILITY_BOX_TOP_LEFT_CORNER = (40, 600)
        ABILITY_BOX_BOTTOM_RIGHT_CORNER = (600, 810)
        d.rectangle([ABILITY_BOX_TOP_LEFT_CORNER, ABILITY_BOX_BOTTOM_RIGHT_CORNER], fill=(255, 255, 255, 0))

        # draw multiline text
        ability_text_image = paste_ability_text_in_rect(full_ability_text, ABILITY_BOX_TOP_LEFT_CORNER, ABILITY_BOX_BOTTOM_RIGHT_CORNER)
        editing_image.paste(ability_text_image, ABILITY_BOX_TOP_LEFT_CORNER)
    
    if card_type == CardType.TWINPACT:
        # get a drawing context
        d = ImageDraw.Draw(editing_image)


        ABILITY_BOX_TOP_LEFT_CORNER = (40, 360)
        ABILITY_BOX_BOTTOM_RIGHT_CORNER = (600, 450)
        d.rectangle([ABILITY_BOX_TOP_LEFT_CORNER, ABILITY_BOX_BOTTOM_RIGHT_CORNER], fill=(255, 255, 255, 0))

        # draw multiline text
        ability_text_image = paste_ability_text_in_rect(full_ability_text, ABILITY_BOX_TOP_LEFT_CORNER, ABILITY_BOX_BOTTOM_RIGHT_CORNER)
        editing_image.paste(ability_text_image, ABILITY_BOX_TOP_LEFT_CORNER)

        # twinpact
        ABILITY_BOX_TOP_LEFT_CORNER = (40, 700)
        ABILITY_BOX_BOTTOM_RIGHT_CORNER = (600, 800)
        d.rectangle([ABILITY_BOX_TOP_LEFT_CORNER, ABILITY_BOX_BOTTOM_RIGHT_CORNER], fill=(255, 255, 255, 0))

        # draw multiline text
        ability_text_image = paste_ability_text_in_rect(full_ability_text2, ABILITY_BOX_TOP_LEFT_CORNER, ABILITY_BOX_BOTTOM_RIGHT_CORNER)
        editing_image.paste(ability_text_image, ABILITY_BOX_TOP_LEFT_CORNER)
    
    if card_type == CardType.SIDEWAYS:
        # get a drawing context
        d = ImageDraw.Draw(editing_image)


        ABILITY_BOX_TOP_LEFT_CORNER = (40, 420)
        ABILITY_BOX_BOTTOM_RIGHT_CORNER = (850, 600)
        d.rectangle([ABILITY_BOX_TOP_LEFT_CORNER, ABILITY_BOX_BOTTOM_RIGHT_CORNER], fill=(255, 255, 255, 0))

        # draw multiline text
        ability_text_image = paste_ability_text_in_rect(full_ability_text, ABILITY_BOX_TOP_LEFT_CORNER, ABILITY_BOX_BOTTOM_RIGHT_CORNER)
        editing_image.paste(ability_text_image, ABILITY_BOX_TOP_LEFT_CORNER)

        editing_image = editing_image.rotate(-90, expand=1)

    editing_image.save(URL.split("/")[-1] + ".png")