from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json
import regex as re
import requests
import pandas as pd
from pandas.io.json import json_normalize
import random
import time

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "XXXX"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
	print "Now searching for videos ......"
	total_count = 0
	nextPageToken=""
	videos=[]
	channels = []
	unique_videos = set()

	while len(unique_videos) <= int(options.max_results) :
		search_response = youtube.search().list(
				q=options.q,
				part="id,snippet",
				maxResults=50,
				type="video",
				pageToken=nextPageToken,
				publishedAfter=str(2017)+"-"+str(01)+"-01T00:00:00Z" #Getting more than 500 videos
				#publishedBefore=str(2017)+"-"+str(01)+"-01T00:00:00Z"
			).execute()

		nextPageToken = search_response.get("nextPageToken")

		for search_result in search_response.get("items", []):
			if search_result["id"]["kind"] == "youtube#video":
				videos.append("%s" % (search_result["id"]["videoId"]))
				channels.append("%s" % (search_result["snippet"]["channelId"]))
			
		unique_videos = set(videos)
		print "Got %s videos" % len(unique_videos)

	video_ids = open('video_ids.txt','w')
	for i in videos:
		video_ids.write("%s\n" %i.encode('utf-8'))

	channel_ids = open('channel_ids.txt','w')
	for i in channels:
		channel_ids.write("%s\n" %i.encode('utf-8'))

	print "Got all the videos"

def get_video_details():
	print "Getting Video Details..."
	complete_result = pd.DataFrame()
	video_ids = open('video_ids.txt','r')
	for line in video_ids:
		v_id = line.rstrip('\n')
		url = "https://www.googleapis.com/youtube/v3/videos?part=status,snippet,topicDetails,contentDetails,statistics&id="+v_id+"&key="+DEVELOPER_KEY
		#name,video_id = line.split('|')
		r = requests.get(url)
		get_json = r.json()
		result = json_normalize(get_json['items'])
		complete_result = complete_result.append(result)
	complete_result.to_csv('Video_data.csv',encoding='utf-8')
	print "Got the video details...."

def get_channel_details():
	print "Getting Channel Details...."
	complete_result = pd.DataFrame()
	channel_ids = open('channel_ids.txt','r')
	for line in channel_ids:
		v_id = line.rstrip('\n')
		url = "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id="+v_id+"&key="+DEVELOPER_KEY
		r = requests.get(url)
		get_json = r.json()
		result = json_normalize(get_json['items'])
		complete_result = complete_result.append(result)
	complete_result.to_csv('Channel_data.csv',encoding='utf-8')
	print "Got the channel details......"

def get_video_comments():
	complete_result = pd.DataFrame()
	video_ids = open('video_ids.txt','r')
	for line in video_ids:
		v_id = line.rstrip('\n')
		url = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId="+v_id+"&key="+DEVELOPER_KEY+"&maxResults=10"
		r = requests.get(url)
		get_json = r.json()
		try:
			result = json_normalize(get_json['items'])
			complete_result = complete_result.append(result)
		except Exception as e:
			pass
	complete_result.to_csv('Comment_data.csv',encoding='utf-8')



if __name__ == "__main__":
	argparser.add_argument("--q", help="Search term")
	argparser.add_argument("--max_results", help="Max results", default=500)
	args = argparser.parse_args()

	try:
		youtube_search(args)
		get_video_details()
		get_channel_details()
		#get_video_comments() -- Use only if you want comments
	except HttpError, e:
		print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
