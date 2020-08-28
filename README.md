# Immo-Webscraping-app-on-Heroku
## What does the app do
This app automatically sends an e-mail as soon as a new "article" is posted on one or more of the 3 specified webpages.

## How the code works
Using python the three webpages: zimmo.be, immoweb.be and immoscoop.be are webscraped. A unique identifier is gotten for every house (or 'article' in the code), and compared to the records in the PostGreSQL database. If the article does not yet exist in the database, a screenshot is taken from the article (or the source url of the image of the article) and send via e-mail to the user. Finally, the unique identifiers of the newly found articles are inserted into the database.