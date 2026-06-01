from pathlib import Path

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib import enums


EXPORT_FOLDER = "exports"

Path(EXPORT_FOLDER).mkdir(
    exist_ok=True
)


def sanitize_filename(text):
    """
    Safe filename.
    """

    invalid_chars = r'<>:"/\|?*'

    for char in invalid_chars:
        text = text.replace(
            char,
            "_"
        )

    return text[:80]


def generate_pdf(
    title,
    content,
    filename
):
    """
    Generate PDF.
    """

    filepath = (
        f"{EXPORT_FOLDER}/{filename}.pdf"
    )

    doc = SimpleDocTemplate(
        filepath
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]

    body_style = styles["BodyText"]

    story = []

    story.append(
        Paragraph(
            title,
            title_style
        )
    )

    story.append(
        Spacer(
            1,
            12
        )
    )

    paragraphs = content.split("\n")

    for line in paragraphs:

        if line.strip() == "":
            continue

        story.append(
            Paragraph(
                line,
                body_style
            )
        )

        story.append(
            Spacer(
                1,
                4
            )
        )

    doc.build(
        story
    )

    return filepath


def create_summary_pdf(
    video_title,
    summary_text
):
    """
    Summary PDF.
    """

    filename = sanitize_filename(
        f"{video_title}_summary"
    )

    return generate_pdf(
        title=f"{video_title} - Summary",
        content=summary_text,
        filename=filename
    )


def create_notes_pdf(
    video_title,
    notes_text
):
    """
    Detailed notes PDF.
    """

    filename = sanitize_filename(
        f"{video_title}_notes"
    )

    return generate_pdf(
        title=f"{video_title} - Notes",
        content=notes_text,
        filename=filename
    )


def create_flashcards_pdf(
    video_title,
    flashcard_text
):
    """
    Flashcards PDF.
    """

    filename = sanitize_filename(
        f"{video_title}_flashcards"
    )

    return generate_pdf(
        title=f"{video_title} - Flashcards",
        content=flashcard_text,
        filename=filename
    )


def create_quiz_pdf(
    video_title,
    quiz_text
):
    """
    Quiz PDF.
    """

    filename = sanitize_filename(
        f"{video_title}_quiz"
    )

    return generate_pdf(
        title=f"{video_title} - Quiz",
        content=quiz_text,
        filename=filename
    )


def create_timestamp_pdf(
    video_title,
    timestamp_text
):
    """
    Timestamp summary PDF.
    """

    filename = sanitize_filename(
        f"{video_title}_timestamps"
    )

    return generate_pdf(
        title=f"{video_title} - Timestamp Summary",
        content=timestamp_text,
        filename=filename
    )


def create_mindmap_pdf(
    video_title,
    mindmap_text
):
    """
    Mindmap PDF.
    """

    filename = sanitize_filename(
        f"{video_title}_mindmap"
    )

    return generate_pdf(
        title=f"{video_title} - Mindmap",
        content=mindmap_text,
        filename=filename
    )