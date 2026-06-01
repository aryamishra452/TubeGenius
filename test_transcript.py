from utils.transcript import *

url = input(
    "Enter URL: "
)

video_id = extract_video_id(
    url
)

print(
    "\nVideo ID:"
)

print(video_id)

print(
    "\nVideo Info:"
)

info = get_video_info(
    url
)

print(info)

package = (
    get_full_transcript_package(
        url
    )
)

print(
    "\nWord Count:"
)

print(
    package["stats"][
        "word_count"
    ]
)

print(
    "\nTranscript Preview:"
)

print(
    package[
        "transcript_text"
    ][:1000]
)