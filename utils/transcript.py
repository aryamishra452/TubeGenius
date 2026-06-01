import re
import yt_dlp

from youtube_transcript_api import (
    YouTubeTranscriptApi
)


def extract_video_id(url):
    """
    Extract video ID from YouTube URL.
    """

    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:shorts/)([A-Za-z0-9_-]{11})",
        r"(?:embed/)([A-Za-z0-9_-]{11})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            url
        )

        if match:
            return match.group(1)

    raise ValueError(
        "Invalid YouTube URL"
    )


def get_video_info(url):
    """
    Get metadata using yt-dlp.
    """

    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

    return {
        "title": info.get(
            "title",
            "Unknown"
        ),
        "author": info.get(
            "uploader",
            "Unknown"
        ),
        "views": info.get(
            "view_count",
            0
        ),
        "length": info.get(
            "duration",
            0
        ),
        "thumbnail": info.get(
            "thumbnail",
            ""
        )
    }


def fetch_transcript(url):
    """
    Fetch transcript.
    """

    video_id = extract_video_id(
        url
    )

    api = YouTubeTranscriptApi()

    try:
     transcript = api.fetch(video_id)
    except Exception as e:
     raise Exception(
        f"Transcript unavailable: {e}"
    )

    return transcript


def transcript_to_text(
    transcript_data
):
    """
    Convert transcript into text.
    """

    text = ""

    for item in transcript_data:

        text += (
            item.text + " "
        )

    return text.strip()


def clean_transcript(text):

    text = re.sub(
        r"\[.*?\]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def seconds_to_timestamp(
    seconds
):

    hours = int(
        seconds // 3600
    )

    minutes = int(
        (seconds % 3600) // 60
    )

    secs = int(
        seconds % 60
    )

    if hours > 0:

        return (
            f"{hours:02}:"
            f"{minutes:02}:"
            f"{secs:02}"
        )

    return (
        f"{minutes:02}:"
        f"{secs:02}"
    )


def transcript_with_timestamps(
    transcript_data
):

    formatted = []

    for item in transcript_data:

        timestamp = (
            seconds_to_timestamp(
                item.start
            )
        )

        formatted.append(
            f"[{timestamp}] "
            f"{item.text}"
        )

    return "\n".join(
        formatted
    )


def get_transcript_stats(
    text
):

    words = len(
        text.split()
    )

    chars = len(text)

    reading_time = max(
        1,
        round(words / 200)
    )

    return {
        "word_count": words,
        "character_count": chars,
        "reading_time": reading_time
    }


def get_full_transcript_package(
    url
):

    transcript_data = (
        fetch_transcript(
            url
        )
    )

    transcript_text = (
        transcript_to_text(
            transcript_data
        )
    )

    transcript_text = (
        clean_transcript(
            transcript_text
        )
    )

    timestamped = (
        transcript_with_timestamps(
            transcript_data
        )
    )

    stats = (
        get_transcript_stats(
            transcript_text
        )
    )

    return {
        "transcript_data":
            transcript_data,

        "transcript_text":
            transcript_text,

        "timestamped_transcript":
            timestamped,

        "stats":
            stats
    }