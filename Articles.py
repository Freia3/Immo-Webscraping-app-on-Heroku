from helperfunctions import get_parsed_page_content
from config import max_count
from bs4 import BeautifulSoup
import os
import pandas as pd

class ListNewArticles:
    # ListNewArticles object will hold a dataframe with new articles, dataframe with existing articles, and instance of chromedriver

    def __init__(self, driver, df_existing_article_ids):
        self.df_articles = pd.DataFrame(columns=["article_id", "html_message", "files_images","article_type","webpage"])
        self.driver=driver  # chromedriver will be used to get source page
        self.df_existing_article_ids=df_existing_article_ids

    def get_df_articles(self):
        return self.df_articles

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

        # Check if you get ReCaptcha error
        if parsed_page_source.get_text().find("Om zeker te zijn dat u geen robot bent") == -1:

            # loop over articles (should be ordered chronologically), until "max_count" numbered article
            for item in parsed_page_source.find_all('div', {'class': 'property-item'}):
                if count < max_count:  # max_count can be changed in config file
                    count += 1
                    article_id = item.get('id')  # unique identifier for article, this will be saved in database

                    if not (article_id in self.df_existing_article_ids.values):  # article is not yet in database

                        # html message that will be included in e-mail
                        src_image = item.find("img", class_="property-thumb").get("src")   # find source url image
                        text = item.get_text()
                        text_formatted = (' '.join(text.split()))
                        html_message = "<p> <b>" + f"Nieuwe {article_type} zimmo: </b>" + text_formatted + "<br>" \
                                       + f" <a href=\"{url}\"> <img src={src_image} height=\"200\" width=\"450\" />" "</a></p>"

                        # add new articles
                        df = pd.DataFrame({"article_id":article_id,"html_message":html_message,"files_images":None,"article_type":article_type,"webpage":webpage}, index=[1])
                        self.df_articles=self.df_articles.append(df,ignore_index = True)
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
                    if not (article_id in self.df_existing_article_ids.values):  # article is not yet in database

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
                            files_images = [("inline", open(str(os.getcwd()) + f"\\screenshot_immoweb_{article_type}{count}.png", "rb"))]
                        else:
                            files_images = [("inline", open(str(os.getcwd()) + f"/screenshot_immoweb_{article_type}{count}.png", "rb"))]

                        # add new articles
                        df = pd.DataFrame({"article_id":article_id,"html_message":html_message,"files_images":files_images,"article_type":article_type,"webpage":webpage}, index=[1])
                        self.df_articles=self.df_articles.append(df,ignore_index = True)
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
                if not (article_id in self.df_existing_article_ids.values):
                    item.screenshot(
                        f"screenshot_immoscoop_{article_type}{count}.png")

                    # html message that will be included in e-mail
                    html_message = f" <p> <b> nieuwe {article_type} immoscoop <br> " \
                                   f"</b> <a href=\"{url}\"> <img src=\"cid:screenshot_immoscoop_{article_type}{count}.png\" " \
                                   f"height=\"200\" width=\"450\" /> " + "</a></p>"
                    # define files_images, this will make sure screenshot is attached to e-mail
                    if str(os.getcwd()) != "/app":  # code is run on my local machine (windows)
                        files_images = [("inline", open(str(os.getcwd()) + f"\\screenshot_immoscoop_{article_type}{count}.png", "rb"))]
                    else:  # code is run on heroku
                        files_images = [("inline", open(str(os.getcwd()) + f"/screenshot_immoscoop_{article_type}{count}.png", "rb"))]

                    # add new articles
                    df = pd.DataFrame({"article_id": article_id, "html_message": html_message, "files_images": files_images, "article_type": article_type, "webpage": webpage}, index=[1])
                    self.df_articles=self.df_articles.append(df,ignore_index = True)

                else:
                    # article is already in database, so we stop here. As articles are ordered chronologically, we won't find new articles after this one
                    break
            else:
                break


    def get_list_html_message(self,article_type):
        list=self.df_articles[self.df_articles["article_type"]==article_type]["html_message"].values.tolist()
        return list

    def get_list_files_images(self,article_type):
        list=self.df_articles[(self.df_articles["article_type"]==article_type) & (self.df_articles["files_images"].notnull())]["files_images"].values.tolist()
        return list

    def __str__(self):
        print_str="number of articles zimmo "+str(len(self.df_articles[self.df_articles["webpage"]=="zimmo"].index)) \
         +"\n" \
         + "number of articles immoweb " \
         +str(len(self.df_articles[self.df_articles["webpage"]=="immoweb"].index)) +"\n" \
         +"number of articles immoscoop "+str(len(self.df_articles[self.df_articles["webpage"]=="immoscoop"].index))

        return print_str


