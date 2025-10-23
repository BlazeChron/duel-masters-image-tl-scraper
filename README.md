# Disclaimer:
Not affiliated with anyone (wotc, fandom maintainers). Just a fan who wants to introduce people who can't read Japanese to the game.

# What is this
Gets the images of Duel Masters cards off the Duel Masters Wiki, and pastes the translation (of the ability text) as provided as a `.png` file.

![this is supposed to be the example image](https://github.com/BlazeChron/duel-masters-image-tl-scraper/blob/master/explain.png)

Has support for sideways cards.

❗ Completely forgot to translate name and card type 🤡

❗ Does not always work, might break depending on the structure of the fandom page. I only tested on my ooga booga aggro decks in Original format.

Also it doesn't look that good, sorry 🥀

# Requirements:
| Thing    | Reason |
| -------- | ------- |
| Python >= 3.12 | It's a Python program |
| Python requests >= 2.32.5 | Get html from Wiki |
| Beautiful soup >= 4.14.2| Parse the html from Wiki   |
| Pillow >= 12.0.0 | Edit the image    |


# Usage
Open your favourite terminal.
## Download this repo, or clone it

```
git clone https://github.com/BlazeChron/duel-masters-image-tl-scraper.git
```
## Move into the directory
```
cd duel-masters-image-tl-scraper/
```
## Create image export directory, images will be exported here
```
mkdir images
```
## Installing dependencies
### Create a virtual environment for the dependencies
Running the following command might take a while with no output, just wait.
```
python -m venv ./.venv
```
### Activate the virtual environment
#### Specifically bash shell on Windows:
```
source ./.venv/Scripts/activate
```
You can deactivate it by running `deactivate`
#### Every other configuration...
I'm not sure... 😛
[Try consulting this section of the venv docs](https://docs.python.org/3/library/venv.html#how-venvs-work)

### Install dependencies
```
pip install -e .
```

And it's ready!

## Put decklist of Duel Masters wiki card links in `decklist.txt`, with 1 card link on each line
`decklist.txt`
```
https://duelmasters.fandom.com/wiki/Dogiragon_Hyper,_Blue_Royal_Road
https://duelmasters.fandom.com/wiki/DARK_MATERIAL_COMPLEX
...
```

## Run (with virtual environment enabled)
```
python url-compiler.py
```

You will find the exported images in the `/images` directory created earlier

# This sucks can I uninstall
## Deactivate your virtual environment (if it's still on)
```
deactivate
```

## Move to the location of the `duel-masters-image-tl-scraper/` directory
```
cd ..
```
## Remove the project
```
rm -rf duel-masters-image-tl-scraper/
```

# Maintenance of this repo:

Note the shoddy card text.

This is not intended to be a very good translator, but something to save time on manually creating each translate card image.

