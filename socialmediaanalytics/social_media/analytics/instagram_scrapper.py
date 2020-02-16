import datetime
import time

import selenium.common.exceptions as sel_error
from django.conf import settings
from mysql.connector import DatabaseError
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import mysql.connector


def process(username, campaign_id):
    posts_meta = get_posts_with_scrapping(username)
    #print(posts_meta)
    user_id = save_user(username)
    save_user_campaign_relation(campaign_id, user_id)
    for p in posts_meta:
        try:
            clean_text, hashtags, img_url, like_count, shares_count, source, timestamp, mentions = extract_post_data(p)
            #print_post_data(clean_text, hashtags, img_url, like_count, shares_count, source, timestamp)
            save_post_data(clean_text, hashtags, img_url, like_count, shares_count, source, timestamp, user_id, campaign_id, mentions)
        except DatabaseError as e:
            print("Could not save due to, ", e)
            continue
        except AttributeError as ae:
            print("Could not extract due to, ", ae)
            continue
        except TypeError as te:
            print("Could not extract due to, ", te)
            continue
        #print_post_data(clean_text, hashtags, img_url, like_count, shares_count, source, timestamp)


def get_posts_with_scrapping(username):
    browser = webdriver.Firefox(executable_path=r'/home/psyentist/Downloads/geckodriver')
    browser.get("https://www.instagram.com/" + username + "/?hl=en")
    lenOfPage = browser.execute_script(
       "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    scroll_count = 0
    while match is False and scroll_count < 5:  # default 200 -> 1232 statuses
        lastCount = lenOfPage
        time.sleep(5)  # 5secs for slow connections
        try :
            lenOfPage = browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        except sel_error.JavascriptException as je:
            print("Could not scroll down, due to ", je)
            continue

        scroll_count += 1
        print(scroll_count)
        if lastCount == lenOfPage:
            match = True
    # Now that the page is fully scrolled, grab the source code.
    source_data = browser.page_source
    # Throw your source into BeautifulSoup and start parsing!
    soup = bs(source_data, 'html.parser')
    #posts_meta = bs(source_data, 'html.parser')
    #posts_meta = soup.findAll("article", {"class": "ySN3v"})
    posts_meta = soup.findAll("div", {"class": "v1Nh3"})
    browser.close()
    return posts_meta


def save_user(user_name):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    social_medium = 'insta'
    cursor.execute("""insert into sm_user (name, social_medium) values (%s, %s)""", (user_name, social_medium))
    user_id = cursor.lastrowid
    cnx.commit()
    cnx.close()
    return user_id


def save_user_campaign_relation(campaign_id, user_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("""insert into campaign_has_sm_user (campaign_campaign_id, sm_user_user_id) 
        values (%s, %s)""", (campaign_id, user_id))
    cnx.commit()
    cnx.close()


def extract_post_data(p):
   # post_div = p.find("div", {"class": "v1Nh3 kIKUG  _bz0w"})
   # print(post_div)
    post_path = p.find("a").get("href")
    #print(post_path)
    browser = webdriver.Firefox(executable_path=r'/home/psyentist/Downloads/geckodriver')
    browser.get("https://www.instagram.com" + post_path + "?hl=en")
    post_source = browser.page_source
    post_html = bs(post_source, 'html.parser')
    #print(post_html)
    browser.close() 
    #clean_text = post_html.find("span", {"class": ""})
    text = post_html.find("div", {"class": "C4VMK"}).find("span", recursive=False)
    #clean_text_span = text.findChildren("span", recursive=False)
    clean_text = text.text
    print("clean_text", clean_text)
  #  text_nospan = remove_span(text)
  # print(text_nospan)
    #clean_text = extract_post_text(text)
    #clean_text = extract_post_text(text)
    #print(clean_text)
    mentions = extract_mentions_from_text(text)
    print("mentions", mentions)
    hashtags = extract_hashtags_from_text(text)
    #hash_a= post_html.find("a", {"class": "xil3i"})
    #hashtags = hash_a.text 
    print("hashtags", hashtags)
    timestamp_parent = post_html.find("time", {"class": "_1o9PC Nzb55"})
    timestamp = timestamp_parent['datetime']
    print("timestamp", timestamp)
   # timestamp_html = post_html.find("time", {"class": "_1o9PC Nzb55"})
    #timestamp = extract_timestamp_from_html(timestamp_html)
    #source_html = post_html.find("div", {"class": "KL4Bh"})
    #source = None
    #if source_html is not None:
    source = "https://www.instagram.com" + post_path + "?hl=en"
    print("source", source)
    # todo fix img urls
    img_html = p.find("img", {"class": "FFVAD"})
    img_url = None
    if img_html is not None:
        img_url = img_html['src']
    #share_section = p.find("div", {"class": "UFIList"})
    print("img_url", img_url)
    shares_count = like_count = 0
    #if share_section is None:
        #shares_text = p.find("a", {"class": "_3rwx _42ft"})
        #shares_count = extract_share_count_from_text(shares_text)

    #if share_section is not None and shares_count == 0:
    #    likes = share_section.find("div", {"class": "UFILikeSentenceText"}).findChildren('span', recursive='false')
    #    like_count = 0
    #    if likes is not []:
    #        like_count = int(before(likes[0].text.replace(",", ""), ' others like this.').split(' ')[-1])
    #    shares = share_section.find("div", {"class": "UFIShareRow"}).findChildren('a', recursive='false')
    #    shares_count = []
    #    if shares is not []:
    #        try:
    #            print('shares txt', shares[0])
    #            shares_count = int(before(shares[0].text.replace(",", ""), ' share'))
    likes_button = post_html.find("div", {"class": "Nm9Fw"})
    if likes_button is None:
        #likes_button = post_html.find("div", {"class": "HbPOm"})
        likes_button = post_html.find("span", {"class": "vcOH2"})
    print("likes_button", likes_button)
    likes_span = likes_button.find("span")
    print("likes_span", likes_span)
    #likes=likes_span.text
    #likes = remove_span(likes_span)
    likes = likes_span.contents
    print("likes", likes)
    if likes is not []:
        like_count = int(likes[0].replace(",", ""))

            #except ValueError as ve:
                #print('Could convert to int due to:', ve)
    print("likes_count", like_count)
    return clean_text, hashtags, img_url, like_count, shares_count, source, timestamp, mentions


def save_post_data(text, hashtags, img_url, like_count, shares_count, source, timestamp, user_id, campaign_id, mentions):
    post_id = save_post(text, like_count, shares_count, timestamp, user_id, campaign_id)
    if source is not None:
        save_url(source, post_id)
    save_mentions(mentions, post_id)
    save_hashtags(hashtags, post_id)
    if img_url is not None:
        save_media(img_url, post_id)


def save_post(text, like_count, shares_count, timestamp, user_id, campaign_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    #ts = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    noT = timestamp.replace("T", " ")
    ts = noT.replace("Z","000")
    print("ts", ts)
    cursor.execute(
        """insert into post (text, timestamp, shares, sm_user_user_id, likes, campaign_campaign_id) 
            values (%s, %s, %s, %s, %s, %s)""",
        (text, ts, shares_count, user_id, like_count, campaign_id))
    status_id = cursor.lastrowid
    cnx.commit()
    cnx.close()
    return status_id


def get_db_connection():
    cnx = mysql.connector.connect(user=settings.DB_USER, password=settings.DB_PASSWORD,
                                  host=settings.DB_HOST, database=settings.DB_NAME)
    return cnx


def save_url(url, status_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    cursor.execute("""insert into url (url, post_post_id) values (%s,%s)""", (url, status_id))

    cnx.commit()
    cnx.close()


def save_mentions(mentions, status_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    for mnt in mentions:
        cursor.execute("""insert into mention (username, post_post_id) values (%s,%s)""", (mnt, status_id))

    cnx.commit()
    cnx.close()


def save_hashtags(hashtags, status_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    for h in hashtags:
        cursor.execute("""insert into hashtag (hashtag, post_post_id) values (%s,%s)""", (h, status_id))

    cnx.commit()
    cnx.close()


def save_media(media, status_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    cursor.execute("""insert into media (url, type, post_post_id) values (%s,%s, %s)""", (media, 'image', status_id))

    cnx.commit()
    cnx.close()


def print_post_data(clean_text, hashtags, img_url, like_count, shares_count, source, timestamp):
    print("clean_text:\n\n",clean_text)
    print("timestamp:\n\n ", timestamp)
    print("source:\n\n",source)
    print("img_url\n\n",img_url)
    print("likes_count\n\n",like_count)
    print("shares_count:\n\n",shares_count)
    #print("mentions", mentions)
    print("hashtags", hashtags)


def before(string, substring):
    position = string.find(substring)
    if position == -1:
        return ''
    return string[0:position]


def extract_post_text(txt):
    cleaned_text = txt.find("span", {"class": ""})
    txt = ''
    for t in cleaned_text:
        txt += t.text

    return txt


def extract_mentions_from_text(text):
    mentions = []
    mentions_html = text.findAll("a", {"class": "notranslate"})
    i = 0
    if mentions_html is not None:
        for m in mentions_html:
            mentions.append(i)
            mentions[i] = m.contents[0]
            i+=1
    return mentions


def extract_hashtags_from_text(text):
    hashtags = []
    hashtags_html = text.findAll("a", {"class": "xil3i"})
    #print("hashtags_html", hashtags_html)
    i = 0
    if hashtags_html is not None:
        for h in hashtags_html:
            hashtags.append(i)
            hashtags[i] = h.contents[0]
            i+=1    
            #hashtags = hashtags_html.contents
    return hashtags


def extract_timestamp_from_html(tstamp_html):
    return tstamp_html['datetime']


def extract_share_count_from_text(shares_text):
    before_text = before(shares_text.text.replace(",", ""), ' Share')
    if before_text.__contains__('K') :
        before_text = float(before(before_text, 'K'))*1000

    return int(before_text)

def remove_span(text):
        for sp in text.findAll('span'):
                sp.replaceWith('')
        return text


# process("time", 14)
