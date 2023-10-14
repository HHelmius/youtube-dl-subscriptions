#!/usr/bin/env python3

from time import time, mktime
from datetime import datetime
import argparse
import sys
from glob import glob
import feedparser
import yt_dlp


def longer_than_a_minute(info, *, incomplete):
    """Download only videos longer than a minute (or with unknown duration)"""
    duration = info.get('duration')
    if duration and duration < 60:
        return 'The video is too short'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--directory',
                        default = '.',
                        help="Specify the directory to save the file")
    args = parser.parse_args()
    path = args.directory if args.directory[-1] == '/' else args.directory+'/'
    if sys.version_info[0] < 3:
        raise Exception('Must be using Python 3')


    if len(glob('last.txt')) == 0:
        with open('last.txt', 'w') as f:
            f.write(str(time()))
            print('Initialized a last.txt file with current timestamp.')

    else:
        with open('last.txt', 'r') as f:
            content = f.read()


        ptime = datetime.utcfromtimestamp(float(content))
        ftime = time()

        urls = []

        with open('subscriptions.csv') as f:
            for row in f.read().splitlines()[1:]:
                if len(row.strip())==0:
                    continue
                urls.append('https://www.youtube.com/feeds/videos.xml?channel_id='
                            f'{row.split(",")[0]}')

        videos = []
        for i, url in enumerate(urls):
            print('Parsing through channel '+str(i+1)+' out of '+str(len(urls)), end='\r')
            feed = feedparser.parse(url)
            for j in range(0,len(feed['items'])):
                timef = feed['items'][j]['published_parsed']
                dt = datetime.fromtimestamp(mktime(timef))
                if dt > ptime:
                    videos.append(feed['items'][j]['link'])

        with open('last.txt', 'w') as f:
            f.write(str(ftime))

        if len(videos) == 0:
            print('Sorry, no new video found')
        else:
            print(str(len(videos))+' new videos found')

        ydl_opts = {
            'match_filter': longer_than_a_minute,
            'write-thumbnail': True,
            'outtmpl': f'{path}%(channel)s-%(title)s.%(ext)s',
            'ignoreerrors': True}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(videos)

if __name__ == '__main__':
    main()
