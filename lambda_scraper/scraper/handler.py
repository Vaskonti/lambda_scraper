import json
from botocore.vendored import requests
from bs4 import BeautifulSoup
import mail_service
import os


def lambda_handler(event, context):
    response = requests.get("https://www.time2play.bg/")
    soup = BeautifulSoup(response.content, 'html.parser')

    title = None
    old_price = None
    new_price = None
    link = None
    imgSrc = None

    for row in soup.select('div.day-deal-holder'):
        title = row.find('div', class_='product-title').find('a').get_text()
        old_price = row.find('span', class_='old-price').get_text()
        new_price = row.find('span', class_='product-price').get_text()
        link = row.find('a', class_='product-image').get('href')
        imgSrc = row.find('img', class_='lazyload').get('data-src')

    template = mail_service.load_html_file("time2play.html")
    return mail_service.send_email(
        "Time2Play.bg",
        template.render(title=title, old_price=old_price, new_price=new_price, link=link,
                        image=imgSrc),
        os.environ['RECEIVERS'].split(","),
    )
