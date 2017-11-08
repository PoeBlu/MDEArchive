import praw
import time
import datetime
import os
import requests

#this code uses inspiration from peoplma's subredditarchive
absolute_path = os.path.dirname(os.path.abspath(__file__))
archive_path = os.path.join(absolute_path, 'data')
reddit = praw.Reddit(client_id="client id",
                     client_secret="client secret",
                     user_agent="python:MDEArchiver:v0.1.0")
subreddit = reddit.subreddit('milliondollarextreme')

def main():
    #if archives already exist, update instead
    if os.path.isdir(archive_path):
        update()
    else:
        new_archive()
 
#the program goes into this function if the archive has already started. Uses date located in
#dates.txt for the start time
def update():
    infile = os.path.join(archive_path, 'dates.txt')
    start = None
    
    with open(infile) as dates:
        start = int(dates.readline())
    
    end = int(time.time())
    archive(start, end)

def new_archive():
    #the subreddit was created on december 12, 2012
    start = int(time.mktime(datetime.datetime.strptime('15/12/2012', "%d/%m/%Y").timetuple()))
    end = int(time.time())
    os.makedirs(archive_path)
    outfile = os.path.join(archive_path, 'dates.txt')
    with open(outfile, 'w') as dates:
        dates.write(str(start))
    archive(start, end)

#this is the function where the archiving is run
def archive(start, end):
    time.sleep(3)
    dates_path = os.path.join(archive_path, 'dates.txt')
    total = end - start
    step = 10800
    current = start
    b = 'timestamp:'
    c = 1
    d = '..'
    while  current < end:
        e = ' --'
        if c % 2 == 0:
            e = ' |'
        f = str(current)
        g = str(current + step)

        try:
            search_results = subreddit.search(b+f+d+g, syntax='cloudsearch')
            print('progress: ' + str(current - start) + '/' + str(total) + '(' + str(((current - start) / total) * 100) + '%)')
            post_count = 0
            for post in search_results:
                post_count += 1
                response = None
                filename = post.name + '.json'
                url = 'https://reddit.com' + (post.permalink).replace('?ref=search_posts', '')
                data = {'user-agent': 'python:MDEArchiver:v0.1.0'}
                good = False
                while not good:
                    try:
                        response = requests.get(url+'.json', headers=data)
                        good = True
                    except Exception as e:
                        print('Error on retrieving post: trying again')
                        print(e)

                filename = os.path.join(archive_path, filename)
                with open(filename, 'w') as file:
                    file.write(response.text)
                    print('archived \"' + post.name + '\"')
            
            #cut the step in half if posts in step exceed 15. This is to make sure that the posts in a range never exceed 25
            #which will cause issues with reddit
            if post_count > 15:
                step = int(step / 2)
                print("setting new step: " + str(step))

            #update the current timestamp and write out to dates.txt
            current += step
            with open(dates_path, 'w') as dates:
                dates.write(str(current))

        except Exception as e:
            print('Error on searching reddit: trying again')
            print(e)

    print('Archive complete.')
            
            
if __name__ == '__main__':
    main()
