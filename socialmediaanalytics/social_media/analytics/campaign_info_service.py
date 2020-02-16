from datetime import datetime

import mysql.connector
from django.conf import settings


def get_all_campaigns():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("""select campaign.*, count(post.post_id) posts 
        from campaign 
        left join post on campaign_id = campaign_campaign_id 
        group by campaign_id order by campaign.timestamp desc limit 50;""")
    campaigns = cursor.fetchall()

    campaign_list = []
    for c in campaigns:
        campaign = {'id': c[0], 'time': c[1], 'name': c[2], 'posts': c[3]}
        cursor.execute("""select social_medium from sm_user 
            inner join campaign_has_sm_user on sm_user_user_id = user_id 
            inner join campaign on campaign_campaign_id = campaign_id  
            where campaign_id = %s""" % (campaign['id']))
        social_media = cursor.fetchall()
        social_media_str = ''
        for s in social_media:
            social_media_str += ' ' + s[0]
        campaign['social_media'] = social_media_str
        campaign_list.append(campaign)
    print(campaign_list)
    cnx.close()
    return campaign_list


def get_top_posts(campaign_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("""select text, timestamp, shares, social_medium
        from post inner join sm_user on sm_user_user_id = user_id
        where campaign_campaign_id = %s order by shares desc limit 100;""" % campaign_id)
    posts = cursor.fetchall()

    post_list = []
    for p in posts:
        post = {'text': p[0], 'time': p[1], 'shares': p[2], 'medium': p[3]}
        post_list.append(post)
    cnx.close()
    return post_list


def get_hashtag_data_for_medium(medium, campaign_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("""select count(*) as cnt, hashtag 
        from hashtag 
        inner join post on post_post_id = post_id 
        inner join sm_user on sm_user_user_id = user_id 
        where social_medium = '%s' and campaign_campaign_id = %s group by hashtag order by cnt desc limit 10;"""
                   % (medium, campaign_id))
    hashtags = cursor.fetchall()
    hashtag_list = []

    for h in hashtags:
        hashtag = {'hashtag': h[1], 'count': h[0]}
        hashtag_list.append(hashtag)
    cnx.close()
    return hashtag_list


def get_mention_data_for_medium(medium, campaign_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("""select count(*) as cnt, username 
        from mention 
        inner join post on post_post_id = post_id 
        inner join sm_user on sm_user_user_id = user_id 
        where social_medium = '%s' and campaign_campaign_id = %s group by username order by cnt desc limit 20;"""
                   % (medium, campaign_id))
    mentions = cursor.fetchall()
    mention_list = []

    for m in mentions:
        mention = {'username': m[1], 'count': m[0]}
        mention_list.append(mention)
    cnx.close()
    return mention_list


def get_url_data_for_medium(medium, campaign_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = get_query_string_for_medium(medium, campaign_id)
    cursor.execute(query)
    urls = cursor.fetchall()
    url_list = []

    for u in urls:
        url = {'site': u[0], 'count': u[1]}
        url_list.append(url)
    cnx.close()
    return url_list


def get_intraday_post_distr_for_medium(medium, campaign_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    cursor.execute("""select hour(timestamp), count(*)
        from post inner join sm_user on user_id = sm_user_user_id
        where campaign_campaign_id = %s and social_medium = '%s'
        group by hour(timestamp);""" % (campaign_id, medium))
    hourly_posts = cursor.fetchall()
    hour_list = []

    for h in hourly_posts:
        hour = {'hour': 'Hour '+str(h[0]), 'count': h[1]}
        hour_list.append(hour)
    cnx.close()
    return hour_list


def get_daily_post_distr_for_medium(medium, campaign_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    cursor.execute("""select dayname(timestamp), count(*)
        from post inner join sm_user on user_id = sm_user_user_id
        where campaign_campaign_id = %s and social_medium = '%s'
        group by dayname(timestamp), dayofweek(timestamp) order by dayofweek(timestamp);""" % (campaign_id, medium))
    daily_posts = cursor.fetchall()
    day_list = []

    for d in daily_posts:
        day = {'day': d[0], 'count': d[1]}
        day_list.append(day)
    cnx.close()
    return day_list


def get_recent_posts(campaign_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("""select text, timestamp, shares, social_medium
        from post inner join sm_user on sm_user_user_id = user_id
        where campaign_campaign_id = %s order by timestamp desc limit 100;""" % campaign_id)
    posts = cursor.fetchall()

    post_list = []
    for p in posts:
        post = {'text': p[0], 'time': p[1], 'shares': p[2], 'medium': p[3]}
        post_list.append(post)
    cnx.close()
    return post_list


def save_campaign(name):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    now = datetime.now()
    cursor.execute("""insert into campaign (timestamp, campaign_name) values ('%s', '%s')""" % (now, name))
    campaign_id = cursor.lastrowid
    cnx.commit()
    cnx.close()
    return campaign_id


def get_db_connection():
    cnx = mysql.connector.connect(user=settings.DB_USER, password=settings.DB_PASSWORD,
                                  host=settings.DB_HOST, database=settings.DB_NAME)
    return cnx


def get_query_string_for_medium(medium, campaign_id):
    if medium == 'tw':
        return ("""SELECT left(url_pref, instr(url_pref, '/')-1) as site, count(*) as cnt 
        FROM(
            select substring(url, instr('https://',url)+1+ length('https://'),length(url)) as url_pref 
            from url inner join post on post_post_id = post_id inner join sm_user on sm_user_user_id = user_id 
            where social_medium = 'tw' and url like 'https://%' and campaign_campaign_id = {}
            union all
            select substring(url, instr('http://',url)+1+ length('http://'),length(url)) as url_pref 
            from url inner join post on post_post_id = post_id inner join sm_user on sm_user_user_id = user_id 
            where social_medium = 'tw' and url like 'http://%' and campaign_campaign_id = {})  as url_prefs
        group by site order by cnt desc limit 20;""".format(campaign_id, campaign_id))
    else:
        return ("""SELECT left(url_pref, instr(url_pref, '%2F')-1) as site, count(*) as cnt 
            FROM (
                select substring(url, instr('https://l.facebook.com/l.php?u=https%3A%2F%2F',url)+1+ length('https://l.facebook.com/l.php?u=https%3A%2F%2F'),length(url)) as url_pref 
                from url inner join post on post_post_id = post_id inner join sm_user on sm_user_user_id = user_id 
                where social_medium = 'fb' and campaign_campaign_id = {}) AS url_prefs 
            group by site order by cnt limit 20;""".format(campaign_id))
