import unittest
from googleapiclient.discovery import build
import os
import json
import sys
import re
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path to import setup_credentials
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent))
from setup_credentials import setup_credentials

def extract_channel_id(youtube_handle_or_url):
    """Extract channel ID from a YouTube handle or URL"""
    # If it looks like a handle (@something)
    if youtube_handle_or_url.startswith('@'):
        # We need to resolve the handle to a channel ID using API
        return None, youtube_handle_or_url
    
    # If it's a channel URL
    match = re.search(r'youtube\.com/channel/([^/?&]+)', youtube_handle_or_url)
    if match:
        return match.group(1), None
    
    # If it's a username URL
    match = re.search(r'youtube\.com/(?:c|user)/([^/?&]+)', youtube_handle_or_url)
    if match:
        return None, f"@{match.group(1)}"
        
    # If it's a handle URL
    match = re.search(r'youtube\.com/@([^/?&]+)', youtube_handle_or_url)
    if match:
        return None, f"@{match.group(1)}"
    
    return None, youtube_handle_or_url

class TestYouTubeAnalytics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up YouTube API client before running tests"""
        try:
            # Get credentials using our setup_credentials utility
            credentials = setup_credentials()
            if credentials:
                cls.youtube = build('youtube', 'v3', credentials=credentials)
                
                # Load YouTube ID from .env file if available
                load_dotenv()
                cls.youtube_id = os.environ.get('yourube_id', '')
                cls.channel_id, cls.channel_handle = extract_channel_id(cls.youtube_id)
                
                # If we only have a handle, resolve it to a channel ID
                if not cls.channel_id and cls.channel_handle:
                    cls.channel_id = cls.resolve_handle_to_id(cls.channel_handle)
            else:
                cls.youtube = None
                cls.channel_id = None
                print("Failed to get credentials. Tests will fail.")
        except Exception as e:
            print(f"Failed to initialize YouTube API client: {e}")
            cls.youtube = None
            cls.channel_id = None
    
    @classmethod
    def resolve_handle_to_id(cls, handle):
        """Resolve a YouTube handle to a channel ID using the API"""
        try:
            # Remove @ symbol if present
            handle_clean = handle.lstrip('@')
            
            # Try to find the channel by handle
            request = cls.youtube.search().list(
                part="snippet",
                q=handle_clean,
                type="channel",
                maxResults=1
            )
            response = request.execute()
            
            if response.get('items'):
                return response['items'][0]['snippet']['channelId']
        except Exception as e:
            print(f"Error resolving handle to ID: {e}")
        
        return None

    def test_api_connection(self):
        """Test if we can connect to YouTube API"""
        self.assertIsNotNone(self.youtube, "YouTube API client should be initialized")

    def test_channel_statistics(self):
        """Test retrieving channel statistics"""
        # Use channel ID from .env file or prompt for it
        channel_id = self.channel_id
        if not channel_id:
            channel_id = input("Enter your YouTube channel ID (or press Enter to skip test): ")
        
        if not channel_id:
            self.skipTest("Channel ID not provided")
            
        try:
            request = self.youtube.channels().list(
                part="statistics,snippet",
                id=channel_id
            )
            response = request.execute()
            self.assertIn('items', response, "Response should contain items")
            self.assertGreater(len(response['items']), 0, "Should have at least one item")
            
            # Print out some basic analytics
            if response['items']:
                channel = response['items'][0]
                stats = channel['statistics']
                snippet = channel['snippet']
                
                print("\nChannel Statistics:")
                print(f"Channel Name: {snippet.get('title', 'N/A')}")
                print(f"Subscribers: {stats.get('subscriberCount', 'N/A')}")
                print(f"Videos: {stats.get('videoCount', 'N/A')}")
                print(f"Total Views: {stats.get('viewCount', 'N/A')}")
        except Exception as e:
            self.fail(f"Failed to retrieve channel statistics: {e}")

    def test_video_analytics(self):
        """Test retrieving video analytics"""
        # Try to get a video from the channel first
        channel_id = self.channel_id
        video_id = None
        
        if channel_id:
            try:
                # Try to get a video from the channel
                request = self.youtube.search().list(
                    part="snippet",
                    channelId=channel_id,
                    maxResults=1,
                    type="video"
                )
                response = request.execute()
                
                if response.get('items'):
                    video_id = response['items'][0]['id']['videoId']
                    print(f"Found video from channel: {video_id}")
            except Exception as e:
                print(f"Error finding videos for channel: {e}")
        
        # If we couldn't find a video, ask the user
        if not video_id:
            video_id = input("Enter a YouTube video ID (or press Enter to skip test): ")
            
        if not video_id:
            self.skipTest("Video ID not provided")
            
        try:
            request = self.youtube.videos().list(
                part="statistics,snippet",
                id=video_id
            )
            response = request.execute()
            self.assertIn('items', response, "Response should contain items")
            self.assertGreater(len(response['items']), 0, "Should have at least one item")
            
            # Print out some basic analytics
            if response['items']:
                video = response['items'][0]
                stats = video['statistics']
                snippet = video['snippet']
                
                print("\nVideo Statistics:")
                print(f"Title: {snippet.get('title', 'N/A')}")
                print(f"Views: {stats.get('viewCount', 'N/A')}")
                print(f"Likes: {stats.get('likeCount', 'N/A')}")
                print(f"Comments: {stats.get('commentCount', 'N/A')}")
        except Exception as e:
            self.fail(f"Failed to retrieve video analytics: {e}")

if __name__ == '__main__':
    unittest.main() 