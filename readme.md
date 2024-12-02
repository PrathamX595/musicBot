# MusicBot

MusicBot is a Discord bot that allows users to play music in voice channels. It supports various commands to control the playback of music from YouTube.

## Features

- Join and leave voice channels
- Play music from YouTube
- Pause, resume, and stop playback

## Commands

- `/join` - Bot joins the voice channel you are in.
- `/leave` - Bot leaves the voice channel.
- `/play <url>` - Plays the audio from the provided YouTube URL.
- `/pause` - Pauses the current playback.
- `/resume` - Resumes the paused playback.
- `/stop` - Stops the current playback.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/musicBot.git
    cd musicBot
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file based on the `.env.example` and add your Discord bot token:
    ```sh
    cp .env.example .env
    ```

5. Run the bot:
    ```sh
    python bot.py
    ```

## Dependencies

- `discord.py` - Python wrapper for the Discord API
- `yt-dlp` - A youtube-dl fork with additional features and fixes
- `python-dotenv` - Reads key-value pairs from a `.env` file and can set them as environment variables
