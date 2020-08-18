import requests
from config import MAILGUN_API_KEY
from config import MAILGUN_DOMAIN
from config import TO_EMAIL

def send_simple_message(list_articles, article_type):
    files_images = list_articles.get_list_files_images(article_type)
    html_message = list_articles.get_list_html_message(article_type)
    if html_message:  # if not empty
        return requests.post(
            "https://api.mailgun.net/v3/"+MAILGUN_DOMAIN+"/messages",
            auth=("api", MAILGUN_API_KEY),
            files=files_images,
            data={"from": "MyName <mailgun@"+MAILGUN_DOMAIN+">",
                  "to": [TO_EMAIL],
                  "subject": f"{article_type}",
                  "html": html_message})

