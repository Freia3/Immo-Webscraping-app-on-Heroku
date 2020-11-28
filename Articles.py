from helperfunctions import get_parsed_page_content
from config import max_count
from bs4 import BeautifulSoup
import os

#bla
class SingleArticle:
    def __init__(self, article_id, html_message, files_images, article_type, webpage):
        self.article_id = article_id
        self.html_message = html_message
        self.files_images=files_images
        self.article_type=article_type
        self.webpage=webpage


class ListNewArticles:
    # ListNewArticles object will hold a list of SingleArticle objects which are new

    def __init__(self, driver, list_existing_article_ids):
        self.article_list=[]
        self.driver=driver  # chromedriver will be used to get source page
        self.list_existing_article_ids=list_existing_article_ids

    def add_article(self, article):
        self.article_list.append(article)

    def find_and_add_new_articles(self,url, webpage, article_type):  # find and articles that are not yet existing in database
        if webpage == "zimmo":
            self.find_and_add_zimmo_articles(url, article_type,webpage)
        elif webpage == "immoweb":
            self.find_and_add_immoweb_articles(url, article_type,webpage)
        elif webpage == "immoscoop":
            self.find_and_add_add_immoscoop_articles(url, article_type,webpage)
        else:
            print("ERROR: wrong webpage")

    def find_and_add_zimmo_articles(self, url, article_type, webpage):
        parsed_page_source = get_parsed_page_content(url)
        count = -1

        # Check if you get captcha error
        if parsed_page_source.get_text().find("Om zeker te zijn dat u geen robot bent") == -1:

            # loop over articles (should be ordered chronologically), until "max_count" numbered article
            for item in parsed_page_source.find_all('div', {'class': 'property-item'}):
                if count < max_count:  # max_count can be changed in config file
                    count += 1
                    article_id = item.get('id')  # unique identifier for article, this will be saved in database

                    if not (article_id in self.list_existing_article_ids):  # article is not yet in database

                        # html message that will be included in e-mail
                        src_image = item.find("img", class_="property-thumb").get("src")   # find source url image
                        text = item.get_text()
                        text_formatted = (' '.join(text.split()))
                        html_message = "<p> <b>" + f"Nieuwe {article_type} zimmo: </b>" + text_formatted + "<br>" \
                                       + f" <a href=\"{url}\"> <img src={src_image} height=\"200\" width=\"450\" />" "</a></p>"

                        # add new articles
                        self.add_article(SingleArticle(article_id, html_message, (), article_type,webpage))
                    else:
                        # article is already in database, so we stop here. As articles are ordered chronologically, we won't find new articles after this one
                        break
                else:
                    break
        else:
            print(f"ERROR: Captcha problem zimmo {article_type}")  # error message

    def find_and_add_immoweb_articles(self, url, article_type, webpage):
        self.driver.get(url)
        self.driver.set_window_size(1500, 2000)  # load images of this window size (otherwise unloaded images on screenshot)

        count = -1

        # Loop over articles
        for item in self.driver.find_elements_by_class_name('search-results__item'):
            item_page_source=item.get_attribute('innerHTML')
            item_parsed_paged_source = BeautifulSoup(item_page_source, 'html.parser')

            if count < max_count:
                count += 1
                if item_parsed_paged_source.find('article', class_="card") is not None:
                    article_id = item_parsed_paged_source.find('article', class_="card").get('id')

                    if not (article_id in self.list_existing_article_ids):  # article is not yet in database

                        try:
                            self.driver.find_element_by_id("uc-btn-accept-banner").click()  # click on accept cookies
                        except:
                            pass
                        item.screenshot(f"screenshot_immoweb_{article_type}{count}.png")

                        # html message to include in email
                        html_message = f" <p> <b> nieuwe {article_type} immoweb: </b>" \
                                       f"<br> <a href=\"{url}\"> <img src=\"cid:screenshot_immoweb_{article_type}{count}.png\" height=\"200\" width=\"450\" /> " + "</a></p>"

                        # files_images makes sure screenshot is attached to email
                        if str(os.getcwd()) != "/app":  # is code run on my local machine or on heroku?
                            files_images = ("inline", open(str(os.getcwd()) + f"\\screenshot_immoweb_{article_type}{count}.png", "rb"))
                        else:
                            files_images = ("inline", open(str(os.getcwd()) + f"/screenshot_immoweb_{article_type}{count}.png", "rb"))

                        # add new articles
                        self.add_article(SingleArticle(article_id, html_message, files_images, article_type,webpage))

                    else:
                        # article is already in database, so we stop here. As articles are ordered chronologically, we won't find new articles after this one
                        break
            else:
                 break

    def find_and_add_add_immoscoop_articles(self, url, article_type, webpage):
        self.driver.get(url)

        count = -1

        # Loop over articles (should be ordered chronologically), until "max_count" numbered article
        for item in self.driver.find_elements_by_class_name('search-result-position'):
            item_page_source=item.get_attribute('innerHTML')
            item_parsed_paged_source = BeautifulSoup(item_page_source, 'html.parser')

            if count < max_count:
                count += 1
                article_id = item_parsed_paged_source.find('a').get('href')  # unique identifier for article, this will be saved in database

                # does article already exist in database?
                if not (article_id in self.list_existing_article_ids):
                    item.screenshot(
                        f"screenshot_immoscoop_{article_type}{count}.png")

                    # html message that will be included in e-mail
                    html_message = f" <p> <b> nieuwe {article_type} immoscoop <br> " \
                                   f"</b> <a href=\"{url}\"> <img src=\"cid:screenshot_immoscoop_{article_type}{count}.png\" " \
                                   f"height=\"200\" width=\"450\" /> " + "</a></p>"

                    # define files_images, this will make sure screenshot is attached to e-mail
                    if str(os.getcwd()) != "/app":  # code is run on my local machine (windows)
                        files_images = ("inline", open(str(os.getcwd()) + f"\\screenshot_immoscoop_{article_type}{count}.png", "rb"))
                    else:  # code is run on heroku
                        files_images = ("inline", open(str(os.getcwd()) + f"/screenshot_immoscoop_{article_type}{count}.png", "rb"))

                    # add new articles
                    self.add_article(SingleArticle(article_id, html_message, files_images, article_type,webpage))
                else:
                    # article is already in database, so we stop here. As articles are ordered chronologically, we won't find new articles after this one
                    break
            else:
                break

    def get_list_article_id(self):
        list_article_id=[]
        for item in self.article_list:
            list_article_id.append(item.article_id)
        return list_article_id

    def get_list_html_message(self,article_type):
        list_html_message=[]
        for item in self.article_list:
            if item.article_type == article_type:
                list_html_message.append(item.html_message)
        return list_html_message

    def get_list_files_images(self,article_type):
        list_files_images=[]
        for item in self.article_list:
            if item.article_type == article_type:
                if item.files_images != ():
                    list_files_images.append(item.files_images)
        return list_files_images

    def __str__(self):

        # Count number of new articles per webpage and article_type
        count = {}
        for item in list(self.article_list):
            count[item.webpage + " " + item.article_type] = count.get(item.webpage + " " + item.article_type, 0) + 1

        # Create string to print out number of new articles
        print_string=""
        for k, v in count.items():
            if v == 1:
                print_string += (k+": "+str(v)+" new article \n")
            else:
                print_string += (k + ": " + str(v) + " new articles \n")
        return print_string
