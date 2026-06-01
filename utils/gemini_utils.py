import os
import google.generativeai as genai

from dotenv import load_dotenv

from utils.prompts import (
    DETAILED_NOTES_PROMPT,
    POINT_SUMMARY_PROMPT,
    FLASHCARD_PROMPT,
    QUIZ_PROMPT,
    TIMESTAMP_SUMMARY_PROMPT,
    MINDMAP_PROMPT
)

# =====================================
# LOAD ENVIRONMENT VARIABLES
# =====================================

load_dotenv()

GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY"
)

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found in .env file"
    )

genai.configure(
    api_key=GOOGLE_API_KEY
)

# =====================================
# LOAD GEMINI MODEL
# =====================================

MODEL_NAME = "gemini-2.5-flash"

model = genai.GenerativeModel(
    MODEL_NAME
)

# =====================================
# GENERIC GENERATION FUNCTION
# =====================================

def generate_content(prompt):
    """
    Generic Gemini call.
    """

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"Error: {str(e)}"


# =====================================
# DETAILED NOTES
# =====================================

def generate_detailed_notes(
    transcript
):
    prompt = DETAILED_NOTES_PROMPT.format(
        transcript=transcript
    )

    return generate_content(prompt)


# =====================================
# POINT SUMMARY
# =====================================

def generate_point_summary(
    transcript
):
    prompt = POINT_SUMMARY_PROMPT.format(
        transcript=transcript
    )

    return generate_content(prompt)


# =====================================
# FLASHCARDS
# =====================================

def generate_flashcards(
    transcript
):
    prompt = FLASHCARD_PROMPT.format(
        transcript=transcript
    )

    return generate_content(prompt)


# =====================================
# QUIZ
# =====================================

def generate_quiz(
    transcript
):
    prompt = QUIZ_PROMPT.format(
        transcript=transcript
    )

    return generate_content(prompt)


# =====================================
# TIMESTAMP SUMMARY
# =====================================

def generate_timestamp_summary(
    timestamped_transcript
):
    prompt = TIMESTAMP_SUMMARY_PROMPT.format(
        transcript=timestamped_transcript
    )

    return generate_content(prompt)


# =====================================
# MINDMAP
# =====================================

def generate_mindmap(
    transcript
):
    prompt = MINDMAP_PROMPT.format(
        transcript=transcript
    )

    return generate_content(prompt)