# socialmediaanalytics
This is a web app that extracts data for specific public profiles of facebook and twitter and presents them unified

## Usage
The user of the app gives the usernames of the public profile (s)he wants to examine in facebook and twitter and  the application 
extracts and processes data and finally provides him/her with the most shared or recent posts, and visualizations that provide aggregate
data

## Installation
This app is writen in Python and uses the framework django. In the front end it uses Html, CSS, Javascript and the libraries JQuery and Plotly.js.
For the backend it uses the MySql Database, the library python-twitter for the communication with the Twitter API, BeautifulSoup for processing
html data, and the library selenium with Firefox web browser to scroll down in facebook. So, to install it, we have to:

00. (Optional) Create a Virtual Environment
01. Install Firefox Web Browser
1. Install python 3 
2. Install django
3. install selenium
4. install mysql-connector-python-rf
5. install BeautifulSoup
6. install python-twitter
7. Install MySql Server
8. run sql script socialmediaanalytics/social_media/database/mysql_db_creation.sql
9. update credentials of db and twitter API in file social_media/social_media/settings.py in the last lines
10. At directory socialmediaanalytics/social_media start the server with the command:
  python manage.py runserver
11. Visit the landing page in a browser at 127.0.0.1:8000/analytics

