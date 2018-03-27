from bs4 import BeautifulSoup
import requests as req
import pandas as pd
import re


def scrape():
    url1 = req.get('https://mars.nasa.gov/news/').text
    url2 = req.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars').text
    url3 = req.get('https://twitter.com/marswxreport?lang=en').text
    url4 = 'http://space-facts.com/mars/'
    url5 = req.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars').text

    mars_collection = {}


    soup = BeautifulSoup(url1, 'lxml')
    news_title = soup.select_one(".content_title").get_text(strip=True)
    news_p = soup.select_one(".rollover_description_inner").get_text(strip=True)
    mars_collection['news_title'] = news_title
    mars_collection['news_p'] = news_p


    soup = BeautifulSoup(url2, 'lxml')
    image_url = soup.select_one(".carousel_item")['style']
    strip = re.findall("url\('(.*?)'\)", image_url)[0]
    featured_image_url = "https://www.jpl.nasa.gov{}".format(strip)
    mars_collection['featured_image_url'] = featured_image_url


    soup = BeautifulSoup(url3, 'lxml')
    tweets = soup.find_all("p", class_="tweet-text")
    for tweet in tweets:
        if tweet.text.partition(' ')[0] == 'Sol':
            mars_weather = tweet.text
            break
    mars_collection['mars_weather'] = mars_weather


    df = pd.read_html(url4, attrs={'id': 'tablepress-mars'})[0]
    df = df.set_index(0).rename(columns={1: "value"})
    del df.index.name
    mars_facts = df.to_html(justify='left')
    mars_collection['mars_facts'] = mars_facts



    soup = BeautifulSoup(url5, 'lxml')
    title = soup.find_all('h3')
    first = title[0].text
    second = title[1].text
    third = title[2].text
    fourth = title[3].text

    def pull_url(insert):
        img_url = "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/{}_enhanced.tif/full.jpg".format(insert)
        return img_url
    first_img = pull_url(first.split(' ')[0].lower())
    second_img = pull_url(second.split(' ')[0].lower())
    third_img = pull_url(third.split(' ')[0].lower() + "_" + third.split(' ')[1].lower())
    fourth_img = pull_url(fourth.split(' ')[0].lower() + "_" + fourth.split(' ')[1].lower())

    hemisphere_image_urls = [
        {'title': first, 'img_url': first_img},
        {'title': second, 'img_url': second_img},
        {'title': third, 'img_url': third_img},
        {'title': fourth, 'img_url': fourth_img}
    ]

    mars_collection['hemisphere_image_urls'] = hemisphere_image_urls



    return mars_collection
