#!/usr/bin/env python
"""
YouTube Analytics - Simplified Runner

This script runs the YouTube API tests to show analytics for your channel
using the configuration from .env file and automatically finding the client secrets.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Make sure we can find the modules in the test directory
test_dir = Path(__file__).parent / "test"
sys.path.append(str(test_dir))

# Import the tests
from test_youtube_analytics import TestYouTubeAnalytics

def main():
    """Run YouTube analytics tests"""
    print("YouTube Analytics")
    print("================")
    
    # Load environment variables
    load_dotenv()
    
    # Get the channel ID from environment
    youtube_id = os.environ.get('yourube_id', '')
    if not youtube_id:
        print("Error: No YouTube ID found in .env file")
        print("Please add 'yourube_id=\"your-channel-url\"' to your .env file")
        return
    
    print(f"Using YouTube ID: {youtube_id}")
    
    # Initialize the test class
    test_class = TestYouTubeAnalytics()
    test_class.setUpClass()
    
    try:
        # Test connection
        print("\nTesting API connection...")
        test_class.test_api_connection()
        print("✓ API connection successful")
        
        # Test channel statistics
        print("\nRetrieving channel statistics...")
        test_class.test_channel_statistics()
        
        # Test video statistics
        print("\nRetrieving video statistics...")
        test_class.test_video_analytics()
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return
    
    print("\nAnalytics completed successfully!")

if __name__ == "__main__":
    main() 