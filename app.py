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

if __name__ == "__main__":
    app.run(debug=True)