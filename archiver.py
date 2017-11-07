import praw
import time
import datetime

#this code uses inspiration from peoplma's subredditarchive

reddit = praw.Reddit('user settings')
subreddit = 'milliondollarextreme'
start_date = int(time.mktime(datetime.datetime.strptime('15/12/2012', "%d/%m/%Y").timetuple()))


