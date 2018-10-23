import requests
from bs4 import BeautifulSoup
import csv

#sets up your ua to look like a web browser instead of a python script
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
           }
keyword = 'chair'

def getContent(query):
    url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' + query

    res = requests.get(url, headers=headers)
    res = BeautifulSoup(res.content, "html.parser")

    return res

def getProductNames(pageContent):
    textContent = []

    for i in range(0, 20):
        names = pageContent.find_all("h2")[i].text
        textContent.append({'name' : names})
        
    return textContent

def getProductPrices(pageContent):
    textContent = []

    for i in range(0, 20):
        currencies = pageContent.find_all("sup", {'class' : 'sx-price-currency' })[i].text
        dollarPrice = pageContent.find_all("span", {'class' : 'sx-price-whole' })[i].text
        centPrice = pageContent.find_all("sup", {'class' : 'sx-price-fractional' })[i].text

        textContent.append({'currency' : currencies, 'dollarPrice' : dollarPrice, 'centPrice' : centPrice})

    return textContent

def sloppyWriteToFile(textList, fileName):
    file = open(fileName, 'w+')
    file.write('[%s]' % '\n'.join(map(str, textList)))
    file.close()

def writeToCSV(textList, fileName):
    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = ['name', 'currency', 'dollarPrice', 'centPrice']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in textList:
            writer.writerow(item)

content = getContent(keyword)

productNames = getProductNames(content)
sloppyWriteToFile(productNames, keyword + 'ProductNames.txt')

productPrices = getProductPrices(content)
sloppyWriteToFile(productPrices, keyword + 'ProductPrices.txt')

productNamesAndPrices = []

for i in range(0, len(productNames)):
    productNamesAndPrices.append({**productNames[i],**productPrices[i]})

writeToCSV(productNamesAndPrices, keyword + 'ProductList.csv')
