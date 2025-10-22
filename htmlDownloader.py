import requests

f = open("check.html", "+w", encoding="UTF-8")

page = requests.get("https://duelmasters.fandom.com/wiki/Dogiragon_Hyper,_Blue_Royal_Road")
f.write(page.text)
f.close()
