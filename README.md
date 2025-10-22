# Disclaimer:
Not affiliated with anyone (wotc, fandom maintainers). Just a fan who wants to introduce people who can't read Japanese to the game.

# What is this
Gets the images of Duel Masters cards off the Duel Masters Wiki, and pastes the translation as provided.

![this is supposed to be the example image](https://github.com/BlazeChron/duel-masters-image-tl-scraper/blob/master/explain.png)

Has support for sideways cards.

Does not always work, might break depending on the structure of the fandom page.

# Requirements:
| Thing    | Reason |
| -------- | ------- |
| Python  | It's coded in Python    |
| Python requests | Get html from Wiki     |
| Beautiful soup    | Parse the html from Wiki    |
| Pillow    | Edit the image    |


# Usage
## Download this repo, or clone it

`git clone https://github.com/BlazeChron/duel-masters-image-tl-scraper.git`

## Install Python requests, Beautiful soup and Pillow

`pip install requests`

`pip install bs4`

`pip install Pillow`


## Create image export directory, images will be created here

`mkdir images`

## Put decklist of Duel Masters wiki card links in `decklist.txt`, with 1 card on each line

`decklist.txt`
```
https://duelmasters.fandom.com/wiki/Dogiragon_Hyper,_Blue_Royal_Road
https://duelmasters.fandom.com/wiki/DARK_MATERIAL_COMPLEX
...
```

## Run
`python url-compiler.py`

You will find the exported images in the `/images` directory created earlier

# Maintenance of this repo:

Note the shoddy card text.

This is not intended to be a very good translator, but something to save time on manually translating each card.

