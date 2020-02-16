from django.http import HttpResponse
from django.shortcuts import render

from . import facebook_scrapper
from . import instagram_scrapper
from . import twitter_data_extractor
from . import campaign_info_service as svc
import csv


def index(request):
    campaigns = svc.get_all_campaigns()
    context = {'campaigns': campaigns}
    return render(request, 'analytics/index.html', context)


def campaign(request, campaign_id):
    top_posts = svc.get_top_posts(campaign_id)
    recent_posts = svc.get_recent_posts(campaign_id)
    twitter_hashtag_data = svc.get_hashtag_data_for_medium('tw', campaign_id)
    fb_hashtag_data = svc.get_hashtag_data_for_medium('fb', campaign_id)
    insta_hashtag_data = svc.get_hashtag_data_for_medium('insta', campaign_id)
    twitter_mention_data = svc.get_mention_data_for_medium('tw', campaign_id)
    fb_mention_data = svc.get_mention_data_for_medium('fb', campaign_id)
    insta_mention_data = svc.get_mention_data_for_medium('insta', campaign_id)
    twitter_url_data = svc.get_url_data_for_medium('tw', campaign_id)
    fb_url_data = svc.get_url_data_for_medium('fb', campaign_id)
    insta_url_data = svc.get_url_data_for_medium('insta', campaign_id)
    twitter_intraday_data = svc.get_intraday_post_distr_for_medium('tw', campaign_id)
    fb_intraday_data = svc.get_intraday_post_distr_for_medium('fb', campaign_id)
    insta_intraday_data = svc.get_intraday_post_distr_for_medium('insta', campaign_id)
    twitter_daily_data = svc.get_daily_post_distr_for_medium('tw', campaign_id)
    fb_daily_data = svc.get_daily_post_distr_for_medium('fb', campaign_id)
    insta_daily_data = svc.get_daily_post_distr_for_medium('insta', campaign_id)

    context = {'posts': top_posts, 'recent_posts': recent_posts, 'tw_hashtags': twitter_hashtag_data,'fb_hashtags': fb_hashtag_data, 'insta_hashtags': insta_hashtag_data ,'tw_mentions': twitter_mention_data, 'fb_mentions': fb_mention_data, 'insta_mentions' : insta_mention_data ,'tw_urls': twitter_url_data, 'fb_urls': fb_url_data, 'insta_urls' : insta_url_data ,'tw_hourly': twitter_intraday_data,'fb_hourly': fb_intraday_data, 'insta_hourly' : insta_intraday_data, 'tw_daily': twitter_daily_data, 'fb_daily': fb_daily_data, 'insta_daily' : insta_daily_data}
    return render(request, 'analytics/campaign.html', context)


"""def new_campaign(request):
    twitter_username = facebook_username = instagram_username = ''
    try:
        twitter_username = request.GET['twitter_username']
    except KeyError:
        pass

    try:
        facebook_username = request.GET['facebook_username']
    except KeyError:
        pass
    
    try:
        instagram_username = request.GET['instagram_username']
    except KeyError:
        pass

    if twitter_username == '' and facebook_username == '' and instagram_username == '':
        return HttpResponse("Wrong Input. Try again")
    else:
        if twitter_username != '':
            campaign_name = twitter_username
            campaign_id = svc.save_campaign(campaign_name)
            twitter_data_extractor.process(twitter_username, campaign_id)
        else:
            if facebook_username != '':
                campaign_name = facebook_username
                campaign_id = svc.save_campaign(campaign_name)
                facebook_scrapper.process(facebook_username, campaign_id)
            else:
                campaign_name = instagram_username
                campaign_id = svc.save_campaign(campaign_name)
        if instagram_username != '':
            instagram_scrapper.process(instagram_username, campaign_id)

        #if facebook_username != '':
        #    facebook_scrapper.process(facebook_username, campaign_id)
    return index(request)
"""

def new_campaign(request):
    twitter_username = facebook_username = instagram_username = ''
    with open('/home/psyentist/myProjects/socialMediaAnalytics/socialmediaanalytics/social_media/analytics/usernames.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            try:
                twitter_username = row[0]
            except KeyError:
                pass

            try:
                facebook_username = row[1]
            except KeyError:
                pass

            try:
                instagram_username = row[2]
            except KeyError:
                pass

            if twitter_username == '' and facebook_username == '' and instagram_username == '':
                return HttpResponse("Wrong Input. Try again")
            else:
                if twitter_username != '':
                    campaign_name = twitter_username
                    campaign_id = svc.save_campaign(campaign_name)
                    twitter_data_extractor.process(twitter_username, campaign_id)
                else:
                    if facebook_username != '':
                        campaign_name = facebook_username
                        campaign_id = svc.save_campaign(campaign_name)
                        #facebook_scrapper.process(facebook_username, campaign_id)
                    else:
                        campaign_name = instagram_username
                        campaign_id = svc.save_campaign(campaign_name)
                if facebook_username != '':
                    facebook_scrapper.process(facebook_username, campaign_id)
                if instagram_username != '':
                    instagram_scrapper.process(instagram_username, campaign_id)
    return index(request)

