import imageDownloader
import time

f = open("decklist.txt", "r")

for line in f.readlines():
    imageDownloader.download_translated_image(line.rstrip())
    time.sleep(2)

#imageDownloader.download_translated_image("https://duelmasters.fandom.com/wiki/Taburasa_Chantaram,_Temple_of_D")