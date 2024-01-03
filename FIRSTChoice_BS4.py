from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

# specify the url
Everythingpage = 'https://firstchoicebyandymark.com/everything'

# query the website and return the html to the variable ‘page’
page = urlopen(Everythingpage)

soup = BeautifulSoup(page, 'html.parser')
productids = []
mydivs = soup.select('div.product-item')

for link in mydivs:
    productid = link.find('a').attrs['href']
    productids.append(productid)

productids.sort()


headers = ["Webpage", "FC Part ID", "Item", "Description", "Source", "Source Part Number", "onhand", "onhold", "available", "Credits Price", "Max Qty"]
rows = [headers]
for id in productids:
    print(id)
    idurl = "https://firstchoicebyandymark.com" + id
    productpage = urlopen(idurl)
    idsoup = BeautifulSoup(productpage, 'html.parser')
    try:
        description = idsoup.p.string
    except:
        description = "NA"
    try:
        onhand = idsoup.select('div.stock.onhand > span.value')[0].string
    except:
        onhand = "NA"
    try:
        onhold = idsoup.select('div.stock.onhold > span.value')[0].string
    except:
        onhold = "NA"
    try:
        available = idsoup.select('div.stock.available > span.value')[0].string
    except:
        available = "NA"
    try:
        source = idsoup.select('div.overview')[0].find('a').attrs['title']
    except:
        source = "NA"
    try:
        sourcePN = idsoup.select('div.manufacturer-part-number > span.value')[0].string.replace("#", '')
    except:
        sourcePN = "NA"
    try:
        name = idsoup.find('h1').text.strip()
    except:
        name = "NA"
    try:
        price = idsoup.select('div.product-price > span ')[0].string.split(" ")[0]
    except:
        price = "NA"
    try:
        maxqty = idsoup.select('div.Maxstock > span.value')[0].string
    except:
        maxqty = "NA"

    row = [idurl, id[1:], name, description, source, sourcePN, onhand, onhold, available, price, maxqty]
    rows.append(row)

with open("FirstChoice.csv", mode='w', newline='', encoding='utf-8') as file:
    file_writer = csv.writer(file)
    file_writer.writerows(rows)
