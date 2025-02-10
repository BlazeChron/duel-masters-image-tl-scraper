import requests

f = open("check.html", "+w", encoding="UTF-8")

page = requests.get("https://duelmasters.fandom.com/wiki/Bolshack_Cross_NEX_/_Bolshack_Saga")
f.write(page.text)
f.close()
