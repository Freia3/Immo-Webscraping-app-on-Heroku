from get_chromedriver import get_chromedriver
from fetch_records_database import fetch_records_psql
from insert_into_psql import insert_into_psql
from Articles import Articles
from send_mail import send_simple_message

type1="woning"  # two types of searches, will also be the title of the email
type2="bouwgrond"

list_existing_article_ids=fetch_records_psql() # list with article-id's already in database and thus not new
driver = get_chromedriver()
list_new_articles = Articles()  # initialize list of articles

##### IMMOSCOOP ####
url = "https://www.immoscoop.be/immo.php?min_price=25000&max_price=650000&proptype=Sale&radio-1=on&ajax=&distance=&country=&streetname=&livingareacondition=&livingarea=&plotareacondition=&plotarea=&yearcondition=&year=&province=&country=&bedroom=&feature=&searchcity=&region=&category=Woning&order=primeurs&get_newproject=&s_postcode%5B%5D=680&s_postcode%5B%5D=1408&s_postcode%5B%5D=2015&s_postcode%5B%5D=897&s_postcode%5B%5D=700&s_postcode%5B%5D=803&s_postcode%5B%5D=1522&s_postcode%5B%5D=1137&s_postcode%5B%5D=1302&s_postcode%5B%5D=199&s_postcode%5B%5D=621&s_postcode%5B%5D=1401&s_postcode%5B%5D=715&s_postcode%5B%5D=937&s_postcode%5B%5D=195&s_postcode%5B%5D=1163&s_postcode%5B%5D=186&s_postcode%5B%5D=834&s_postcode%5B%5D=1127&s_postcode%5B%5D=170&s_postcode%5B%5D=833&s_postcode%5B%5D=880&s_postcode%5B%5D=911&s_postcode%5B%5D=1514&s_postcode%5B%5D=1736&main_city%5B%5D=2624&main_city%5B%5D=2643&main_city%5B%5D=2627&main_city%5B%5D=2636&main_city%5B%5D=2623"
list_new_articles.find_and_add_new_articles(url, driver, "immoscoop", type1, list_existing_article_ids)

url= """https://www.immoscoop.be/immo.php?min_price=25000&max_price=650000&proptype=Sale&radio-1=on&ajax=&distance=&country=&streetname=&livingareacondition=&livingarea=&plotareacondition=&plotarea=&yearcondition=&year=&province=&country=&bedroom=&feature=&searchcity=&region=&category=Grond&order=primeurs&get_newproject=&s_postcode%5B%5D=680&s_postcode%5B%5D=1408&s_postcode%5B%5D=2015&s_postcode%5B%5D=897&s_postcode%5B%5D=700&s_postcode%5B%5D=803&s_postcode%5B%5D=1522&s_postcode%5B%5D=1137&s_postcode%5B%5D=1302&s_postcode%5B%5D=199&s_postcode%5B%5D=621&s_postcode%5B%5D=1401&s_postcode%5B%5D=715&main_city%5B%5D=2624&s_postcode%5B%5D=937&s_postcode%5B%5D=195&s_postcode%5B%5D=1163&main_city%5B%5D=2643&s_postcode%5B%5D=186&s_postcode%5B%5D=834&s_postcode%5B%5D=1127&main_city%5B%5D=2627&s_postcode%5B%5D=170&s_postcode%5B%5D=833&s_postcode%5B%5D=880&main_city%5B%5D=2636&s_postcode%5B%5D=911&s_postcode%5B%5D=1514&s_postcode%5B%5D=1736&main_city%5B%5D=2623"""
list_new_articles.find_and_add_new_articles(url, driver, "immoscoop", type2, list_existing_article_ids)

##### ZIMMO ####
url = "https://www.zimmo.be/nl/panden/?status=1&type%5B0%5D=3&type%5B1%5D=5&hash=49fa01e43bbc5dacc46015c75f9f8270&priceMin=100000&priceMax=610000&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=1&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=1&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&region=circle&radius=7006&lat=50.881329196507&lng=4.714985705377&sort=recent&sort_order=desc#gallery"
list_new_articles.find_and_add_new_articles(url, driver, "zimmo", type1, list_existing_article_ids)

url = "https://www.zimmo.be/nl/panden/?status=1&type%5B0%5D=3&hash=20b07c9590fb73bf99e9b2c1eabad48a&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=1&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=1&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&region=circle&radius=6957&lat=50.881329196507&lng=4.714985705377&sort=recent&sort_order=desc#gallery"
list_new_articles.find_and_add_new_articles(url, driver, "immoscoop", type2, list_existing_article_ids)

##### IMMOWEB #####
url = ("""https://www.immoweb.be/nl/zoeken/huis/te-koop?countries=BE&geoSearchAreas=mvduHoa_%5Cf%40xsGqi%40j_HcK~p%40gWjg%40swA~bBk%5DnJag%40tx%40m%7CAl~%40_bC%7C%40wv%40mLqMyD%7D%60%40ao%40qu%40oJit%40ymAmo%40%7DdBgn%40g_EyT%7BvCxTkfG~l%40ueF~Oao%40x%7C%40_cB%7CpBmpBl%60Ame%40buAxD~f%40lLjvAj%60AzTzYlz%40h%7BA~%60%40%60aBpqAf%7BAhh%40bfAbKhi%40&maxPrice=650000&minPrice=15000&priceType=PRICE&orderBy=newest""")
list_new_articles.find_and_add_new_articles(url, driver, "immoweb", type1, list_existing_article_ids)

url = ("""https://www.immoweb.be/nl/zoeken/grond/te-koop?countries=BE&geoSearchAreas=mvduHoa_%5Cf%40xsGqi%40j_HcK~p%40gWjg%40swA~bBk%5DnJag%40tx%40m%7CAl~%40_bC%7C%40wv%40mLqMyD%7D%60%40ao%40qu%40oJit%40ymAmo%40%7DdBgn%40g_EyT%7BvCxTkfG~l%40ueF~Oao%40x%7C%40_cB%7CpBmpBl%60Ame%40buAxD~f%40lLjvAj%60AzTzYlz%40h%7BA~%60%40%60aBpqAf%7BAhh%40bfAbKhi%40&maxPrice=650000&minPrice=15000&priceType=PRICE&orderBy=newest""")
list_new_articles.find_and_add_new_articles(url, driver, "immoweb", type2, list_existing_article_ids)

driver.close()  # close chromedriver

print(list_new_articles)

# insert articles into psql
insert_into_psql(list_new_articles.get_list_article_id())

#Send Emails
send_simple_message(list_new_articles,type1)
send_simple_message(list_new_articles, type2)
