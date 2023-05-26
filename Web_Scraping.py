# Imports
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")


# Get all product links 
productlinks = []
baseurl = "https://turbo.az/"


for page_num in range(1,600):
    r = requests.get(f"https://turbo.az/autos?page={page_num}")
    soup = BeautifulSoup(r.content, 'html.parser')
    productlist = soup.find_all("div", class_='products-i')
    for item in productlist:
        for links in item.find_all("a", href=True):
            productlinks.append(baseurl + links["href"])


# Links which end wtih a "bookmarks" are not active links
# Add active links to new list

alllinks = []
for link in productlinks:
    if not link.endswith("bookmarks"):
        alllinks.append(link)



# Check the number of links
print(f"Number of links: {len(alllinks)}")


# Create empty DataFrame
CarPrice= pd.DataFrame()


# Scrap the data as key and value 
for link in alllinks[:10000]:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    details = soup.find_all("div", class_="product-properties__i")
    price =soup.find("div", class_= "product-price__i product-price__i--bold")
    information=re.sub('<[^>]+>', ' ', str(details))
    information = re.sub("\[|\]",'',information)
    information = information.split(" ,")
    information = [l.strip() for l in information]
    mydict = {}                                            # Create dictionary from the information of each product
    for s in information:
        words = s.split("  ")
        key = words[0]
        value = ' '.join(words[1:])
        mydict[key] = value.strip()
        mydict["Qiymət"] = price.text.strip()
    CarPrice = CarPrice.append(mydict,ignore_index=True)   # Append each dictionary to dataframe

print(CarPrice)


# Drop duplicates
CarPrice = CarPrice.drop_duplicates()


# Save dataframe to csv
CarPrice.to_csv("CarPrice.csv")
