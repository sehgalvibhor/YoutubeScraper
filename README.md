# YoutubeScraper
Python code to scrape Youtube videos (500+), Comments and Channel statistics.

### youtube_search(args)
* Searches for the specific keyword

### get_video_details()
* Gets all the possible details about the video(based on the Video IDs searched using the youtube_search function, dumps the json output in a CSV file.

### get_channel_details()
* Gets all the possible details about the Channel(based on the Channel IDs the Video IDs belong to using the youtube_search function. Dumps the json output in a CSV file.

### get_video_comments()
* Gets top 10 comments of the videos based on Video IDs (Runs a little slow)
