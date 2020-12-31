from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

# specify the url
quote_page = 'https://firstchoicebyandymark.com/everything'

# query the website and return the html to the variable ‘page’
page = urlopen(quote_page)

soup = BeautifulSoup(page, 'html.parser')
productids = []
# mydivs = soup.findAll("div", {"class":'product-item'})
mydivs = soup.select('div.product-item')
for link in mydivs:
    productid = link.find('a').attrs['href']
    productids.append(productid)
    title = link.find('a').attrs['title']
    # print(href.attrs['href'])
    # print(productid)
    # print(title)
    priceinfo = link.select('div.prices')
    # price = priceinfo.find('price actual-price')
    # print(priceinfo)
    # price = link.find('price')
    # print(price)

headers = ["Webpage", "Item", "Description", "Source", "Source Part Number", "onhand", "onhold", "available", "Credits Price", "Max Qty"]
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

    # if (id == "/fc-fan12"):
    #     print("Name: " + name)
    #     print("Description: " + description)
    #     print("Source: " + source)
    #     print("Source Part Number: " + sourcePN.replace("#", ''))
    #     print("Onhand: " + onhand)
    #     print("Onhold: " + onhold)
    #     print("Available: " + available)
    #     print("Price: " + price)
    #     print(maxqty)
        # print(idsoup.p.string)

        # print(idsoup)


    row = [idurl, name, description, source, sourcePN, onhand, onhold, available, price, maxqty]
    rows.append(row)
    # overview = idsoup.select('div.overview')
    # name = idsoup.find('h1')
    # print(name.text.strip())
    # # for h in idsoup.find_all('h1'):
    # #     print(h.text.strip())
    # # print(source)
    # for item in overview:
    #     print("Item: \r\n~~~~~~~~~~\r\n")
    #     print(item)
    #     source = item.find('a').attrs['title']
    #     print("Source: "+source)
    #     input()
    # print(overview)
    # # name = overview.find('h1')

with open("FirstChoice.csv", mode='w', newline='') as file:
    file_writer = csv.writer(file)
    file_writer.writerows(rows)
# name = name_box.text.strip()
# print(name)
