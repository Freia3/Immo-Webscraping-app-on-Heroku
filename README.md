# Immo Webscraping app on Heroku with Python
## What does the app do
This app automatically sends an e-mail as soon as a new house is posted on one or more of the 3 specified real estate webpages.

## How the code works
Using python the following three webpages are webscraped: zimmo.be, immoweb.be and immoscoop.be. A unique identifier is gotten for every house (or 'article' in the code), and compared to the records in the database. If the article does not yet exist in the database, a screenshot is taken from the article (or the source url of the image of the article) and send via e-mail to the user. Finally, the unique identifiers of the newly found articles are inserted into the database.

## Deployment
I deployed the app on Heroku. I used the Heroku Postgres add-on for the database, and the Mailgun add-on for sending the e-mails. I scheduled the code to run every hour by using the Heroku scheduler add-on. (All this can be done for free on Heroku, for more details on how to deploy to heroku: https://github.com/Freia3/Immo-Webscraping-app-on-Heroku/wiki/How-to-deploy-the-python-app-to-Heroku)

## How to run the code
First the config.py file needs to be added, based on the config - TEMPLATE.py file. This config file will contain the database URL and the domain used to send the emails.
Change the URLs in the main.py file with your own and run the main.py file.

### Comments 
- When the app is deployed from Heroku, you get a reCAPTCHA from zimmo.be when requesting the page source a second time. This is probably because you are accessing the webpage   from outside Belgium when running from Heroku.
- We use the requests python module to get the page source of the zimmo webpage and the selenium module for the other webpages because zimmo.be requests captcha with selenium
