from helperfunctions import insert_into_psql, send_simple_message, get_chromedriver, fetch_records_psql
from Articles import ListNewArticles
from config import database_url, TO_EMAIL, MAILGUN_API_KEY,MAILGUN_DOMAIN, MYNAME
import pandas as pd

# Get Dataframe of existing Articles from database
df_existing_article_ids=fetch_records_psql(database_url)

# Initialize List where we will put new Articles
driver=get_chromedriver()  # chromedriver will be used to scrape webpages
list_new_articles = ListNewArticles(driver, df_existing_article_ids)  # df_existing_article_ids will be used to check if article is new

type1="woning"  # We will do two types of searches (type1 and type2 will also be the titles of the emails sent)
type2="bouwgrond"

# Add newly found articles to the list:
# Replace 'url' variables with your own urls. Make sure articles in url are sorted chronologically from newest to oldest!
#   IMMOSCOOP #
url="https://www.immoscoop.be/immo.php?search_field=&main_city%5B%5D=2623&s_postcode%5B%5D=897&s_postcode%5B%5D=700&s_postcode%5B%5D=803&s_postcode%5B%5D=1522&s_postcode%5B%5D=1514&category=&min_price=0&max_price=&bedroom=&baths=&order=date&proptype=Sale"
list_new_articles.find_and_add_new_articles(url, "immoscoop", type1)
#
url="https://www.immoscoop.be/immo.php?min_price=0&max_price=&proptype=Sale&radio-1=on&ajax=&distance=&country=&streetname=&livingareacondition=&livingarea=&plotareacondition=&plotarea=&yearcondition=&year=&province=&country=&bedroom=&feature=&searchcity=&region=&category=Grond&order=date&get_newproject=&s_postcode%5B%5D=897&s_postcode%5B%5D=700&s_postcode%5B%5D=803&s_postcode%5B%5D=1522&s_postcode%5B%5D=1514&main_city%5B%5D=2623"
list_new_articles.find_and_add_new_articles(url, "immoscoop", type2)

# #   ZIMMO #
url="https://www.zimmo.be/nl/panden/?status=1&type%5B0%5D=5&hash=d29e8ddd1fa4ad3f7fc14bb8a1cfb91d&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=1&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=1&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&region=list&district=MzCgLjAEAA%253D%253D&sort=recent&sort_order=desc#gallery"
list_new_articles.find_and_add_new_articles(url, "zimmo", type1)

url="https://www.zimmo.be/nl/panden/?status=1&type%5B0%5D=3&hash=3f761ce658b9c44b4f4d6df656e425bd&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=1&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=1&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&region=list&district=MzCgLjAEAA%253D%253D#gallery"
list_new_articles.find_and_add_new_articles(url, "immoscoop", type2)

#   IMMOWEB #
url="https://www.immoweb.be/nl/zoeken/huis/te-koop/leuven/3000?countries=BE&orderBy=newest"  # -->orderBy=newest --> chronologically ordered items
list_new_articles.find_and_add_new_articles(url, "immoweb", type1)

url="https://www.immoweb.be/nl/zoeken/grond/te-koop/leuven/arrondissement?countries=BE&orderBy=newest"
list_new_articles.find_and_add_new_articles(url, "immoweb", type2)

driver.close()  # close chromedriver
#
# Print all the new found articles
with pd.option_context('display.max_rows', 1000, 'display.max_columns', 100):
    print(list_new_articles.df_articles)

# Insert newly found articles into database
insert_into_psql(list_new_articles.get_df_articles(), database_url)

# Send Emails with newly found articles
send_simple_message(list_new_articles,type1, TO_EMAIL, MAILGUN_API_KEY,MAILGUN_DOMAIN, MYNAME)
send_simple_message(list_new_articles, type2, TO_EMAIL, MAILGUN_API_KEY,MAILGUN_DOMAIN, MYNAME)
