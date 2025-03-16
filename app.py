from flask import Flask, render_template
import requests
import json
from bs4 import BeautifulSoup as soup

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scmp")
def scmp():
    url = "https://www.scmp.com/rss/36/feed"
    html_page = soup(requests.get(url).content, "xml")
    
    news_list = html_page.findAll("item")
    title_list = []
    link_list = []
    desc_list = []
    date_list = []

    for news in news_list:
        title_list.append(news.title.text)
        link_list.append(news.link.text)
        desc_list.append(news.description.text)
        date_list.append(news.pubDate.text)

    news_dict = {
    "title": title_list,
    "link": link_list,
    "description": desc_list,
    "date": date_list
    
    }
    return render_template("scmp.html", news_dict=news_dict)

@app.route("/nike")
def nike():
    return render_template("nike.html")

@app.route("/nike/<string:category>")
def nike_cat(category):
    url = "https://www.nike.com.hk/" + category + "/shoe/list.htm?intpromo=PNTP"
    soup_page = soup(requests.get(url).content, "html")

    product_list_content = soup_page.find_all("dl", {"class" : "product_list_content"})
    product_name_list = []
    product_price_list = []

    for product in product_list_content:
        product_name_list.append(product.find("span", {"class" : "up"}).text)
        product_price_list.append(product.find("dd", {"class" : "color666"}).text.split("HK$")[-1].replace(",", ""))

    nike_dict = {
        "names" : product_name_list,
        "prices" : product_price_list
    }
    
    return render_template("nikef.html", nike_dict=nike_dict, title=category)

if __name__ == "__main__":
    app.run(debug=True)