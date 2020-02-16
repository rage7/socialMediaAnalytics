import time

import mysql.connector
import twitter
from mysql.connector import DatabaseError
from django.conf import settings

api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY, consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                  access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
                  access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)


def process(username, campaign_id):
    statuses = get_full_user_timeline(username)
    user_id = save_user(statuses[0])
    save_user_campaign_relation(campaign_id, user_id)
    for s in statuses:
        urls = extract_urls_from_status(s)
        mentions = extract_mentions_from_status(s)
        hashtags = extract_hashtags_from_status(s)
        media = extract_media_from_status(s)

        try:
            status_id = save_status(s, user_id, campaign_id)
            save_urls(urls, status_id)
            save_mentions(mentions, status_id)
            save_hashtags(hashtags, status_id)
            save_media(media, status_id)
        except DatabaseError as e:
            print("Could not save due to, ", e)
            continue


def get_full_user_timeline(screen_name):
    all_statuses = []
    statuses = api.GetUserTimeline(screen_name = screen_name, count = 200)
    all_statuses = all_statuses + statuses
    statuses_size = len(statuses)

    if statuses_size == 0:
        return []

    last_status = statuses.__getitem__(statuses_size-1)

    while statuses_size == 200:
        statuses = api.GetUserTimeline(screen_name=screen_name, count=200, max_id=last_status.__getattribute__("id"))

        if not statuses:
            break

        all_statuses = all_statuses + statuses
        statuses_size = len(statuses)
        last_status = statuses.__getitem__(statuses_size - 1)

    return all_statuses


def save_user(user_status):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    user_name = user_status.user.screen_name
    followers_count = user_status.user.followers_count
    social_medium = 'tw'
    cursor.execute("""insert into sm_user (name, followers, social_medium) values ('%s', '%s', '%s')"""
                   % (user_name, followers_count, social_medium))
    user_id = cursor.lastrowid
    cnx.commit()
    cnx.close()
    return user_id


def save_user_campaign_relation(campaign_id, user_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute(
        """insert into campaign_has_sm_user (campaign_campaign_id, sm_user_user_id) values ('%s', '%s')""" % (
        campaign_id, user_id))
    cnx.commit()
    cnx.close()


def extract_urls_from_status(status):
    url_list = []
    urls = status.urls
    for u in urls:
        url = u.expanded_url
        url_list.append(url)
    return url_list


def extract_mentions_from_status(status):
    mention_list = []
    mentions = status.user_mentions
    for m in mentions:
        username = m.screen_name
        # print(username)
        mention_list.append(username)
    return mention_list


def extract_hashtags_from_status(status):
    hashtag_list = []
    hashtags = status.hashtags
    for h in hashtags:
        hashtag = h.text
        # print(hashtag)
        hashtag_list.append(hashtag)
    return hashtag_list


def extract_media_from_status(status):
    media_list = []
    medias = status.media
    if medias is None:
        return []
    for m in medias:
        url = m.media_url
        type = m.type

        media_list.append((url,type))
    return media_list


def save_status(status, user_id, campaign_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    text = status.text
    timestamp = status.created_at
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(timestamp, '%a %b %d %H:%M:%S +0000 %Y'))
    retweets = status.retweet_count
    favorites = status.favorite_count

    cursor.execute("""insert into post (text, timestamp, shares, sm_user_user_id,favorites, campaign_campaign_id) values (%s, %s, %s, %s, %s, %s)""", (text, ts, retweets, user_id, favorites, campaign_id))
    status_id = cursor.lastrowid
    cnx.commit()
    cnx.close()
    return status_id


def save_urls(urls, status_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    for url in urls:
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


def save_media(medias, status_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    for m in medias:
        cursor.execute("""insert into media (url, type, post_post_id) values (%s,%s, %s)""", (m[0], m[1], status_id))

    cnx.commit()
    cnx.close()


def print_statuses(statuses):
    idx = 0
    for s in statuses:
        idx += 1
        print(idx, "\t", s)


def get_db_connection():
    cnx = mysql.connector.connect(user=settings.DB_USER, password=settings.DB_PASSWORD,
                                  host=settings.DB_HOST, database=settings.DB_NAME)
    return cnx



# process("cnn", 5)


