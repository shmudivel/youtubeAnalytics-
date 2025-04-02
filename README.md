# YouTube Analytics Testing

A simple test suite for YouTube API analytics.

## Setup

You already have the necessary files:
- OAuth credentials in `client_secret_*.json`
- YouTube channel ID in `.env` file

### 1. Set Up Conda Environment

```bash
# Create a new conda environment
conda create -n youtube_analytics python=3.10 -y

# Activate the environment
conda activate youtube_analytics

# Install required packages
pip install -r requirements.txt
```

## Running the Tests

### Option 1: Simplified Run (Recommended)

Just run the simplified script with your conda environment activated:

```bash
conda activate youtube_analytics
python run_analytics.py
```

This will:
- Automatically find your client secrets file
- Use your YouTube channel ID from the .env file
- Display your channel and video statistics

### Option 2: Manual Run

If you prefer to run the individual tests:

```bash
conda activate youtube_analytics
cd test
python test_youtube_analytics.py
```

The tests will:
- Automatically find your client secrets file 
- Use your YouTube channel ID from the .env file
- Display your channel and video statistics

## Notes

- The first time you run the tests, it will create a `token.json` file which stores your access tokens
- This allows future runs to work without re-authenticating
- If you encounter authentication issues, delete the `token.json` file and run again
- All YouTube API requests use the read-only scope, so your account is safe