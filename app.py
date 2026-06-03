#imports
import sys

print("PYTHON EXECUTABLE:")
print(sys.executable)

import os
import streamlit as st

from dotenv import load_dotenv

from utils.database import (
    initialize_database,
    get_all_history,
    get_history_by_id,
    clear_history
)

from utils.transcript import (
    extract_video_id,
    get_video_info,
    get_full_transcript_package
)

from utils.rag_chat import (
    build_vector_store,
    vector_store_exists,
    ask_video
)

from utils.gemini_utils import (
    generate_detailed_notes,
    generate_point_summary,
    generate_flashcards,
    generate_quiz,
    generate_timestamp_summary,
    generate_mindmap
)

from utils.pdf_export import (
    create_notes_pdf,
    create_summary_pdf,
    create_flashcards_pdf,
    create_quiz_pdf,
    create_timestamp_pdf,
    create_mindmap_pdf
)

from utils.graph_generator import (
    create_mindmap
)

#load environment
load_dotenv()

#page config
st.set_page_config(
    page_title="TubeGenius",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)


#database initialization
initialize_database()

#custom css for better styling
st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.card-btn button {
    width: 100%;
    height: 90px;
    font-size: 18px;
    border-radius: 12px;
}

.metric-card {
    text-align:center;
    padding:10px;
    border-radius:10px;
}

.stButton>button {
    width:100%;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

#session state
if "transcript_text" not in st.session_state:
    st.session_state.transcript_text = ""

if "timestamped_text" not in st.session_state:
    st.session_state.timestamped_text = ""

if "video_title" not in st.session_state:
    st.session_state.video_title = ""

if "video_url" not in st.session_state:
    st.session_state.video_url = ""

if "generated_output" not in st.session_state:
    st.session_state.generated_output = ""

if "current_mode" not in st.session_state:
    st.session_state.current_mode = ""

if "output_type" not in st.session_state:
    st.session_state.output_type = ""

if "saved_once" not in st.session_state:
    st.session_state.saved_once = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


#App Header
st.title("🎥 TubeGenius")

st.caption(
    "AI-Powered YouTube Learning Assistant"
)

#sidebar history
with st.sidebar:

    st.header("📜 History")

    history_items = get_all_history()

    if history_items:

        for item in history_items:

            history_id = item[0]
            title = item[1]
            summary_type = item[2]

            if st.button(
                f"{title} ({summary_type})",
                key=f"history_{history_id}"
            ):

                record = get_history_by_id(
                    history_id
                )

                st.session_state.generated_output = (
                    record[4]
                )

    st.divider()

    if st.button(
        "🗑 Clear History"
    ):
        clear_history()
        st.rerun()

#Youtube URL input
st.subheader(
    "Paste YouTube Video URL"
)

youtube_url = st.text_input(
    "",
    placeholder="https://www.youtube.com/watch?v=..."
)

#Video processing
if youtube_url:

    try:

        video_id = extract_video_id(
            youtube_url
        )

        info = get_video_info(
            youtube_url
        )

        st.session_state.video_url = (
            youtube_url
        )

        st.session_state.video_title = (
            info["title"]
        )

    except Exception as e:

        st.error(
            f"Invalid URL: {e}"
        )

#Thumbnail and meta data display
if youtube_url:

    try:

        info = get_video_info(
            youtube_url
        )

        col1, col2 = st.columns(
            [1, 2]
        )

        with col1:

            st.image(
                info["thumbnail"]
            )

        with col2:

            st.markdown(
                f"### {info['title']}"
            )

            st.write(
                f"👤 {info['author']}"
            )

            st.write(
                f"👀 {info['views']:,} views"
            )

            st.write(
                f"⏱ {info['length']//60} min"
            )

    except:
        pass

#extract transcript button
if youtube_url:

    if st.button(
        "🚀 Load Video"
    ):

        try:

            with st.spinner(
                "Extracting transcript..."
            ):

                package = (
                    get_full_transcript_package(
                        youtube_url
                    )
                )

                st.session_state.transcript_text = (
                    package[
                        "transcript_text"
                    ]
                )

                st.session_state.timestamped_text = (
                    package[
                        "timestamped_transcript"
                    ]
                )

                build_vector_store(
                    package[
                        "transcript_text"
                    ]
                )

                st.success(
                    "Video Loaded Successfully"
                )

        except Exception as e:

            st.error(
                str(e)
            )

#transcript statistics
if st.session_state.transcript_text:

    stats = (
        get_full_transcript_package(
            youtube_url
        )["stats"]
    )

    st.subheader(
        "📊 Transcript Statistics"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Words",
            stats["word_count"]
        )

    with c2:
        st.metric(
            "Characters",
            stats["character_count"]
        )

    with c3:
        st.metric(
            "Reading Time",
            f"{stats['reading_time']} min"
        )

#main navigation buttons
if st.session_state.transcript_text:

    st.divider()

    nav1, nav2 = st.columns(2)

    with nav1:

        if st.button(
            "📄 Summarize Video"
        ):
            st.session_state.current_mode = (
                "summary"
            )

    with nav2:

        if st.button(
            "💬 Chat With Video"
        ):
            st.session_state.current_mode = (
                "chat"
            )

#SUMMARY MODE SECTION
if st.session_state.current_mode == "summary":

    st.divider()

    st.subheader(
        "📚 Summary Workspace"
    )

    row1_col1, row1_col2, row1_col3 = (
        st.columns(3)
    )

    row2_col1, row2_col2, row2_col3 = (
        st.columns(3)
    )

#detailed notes button
    with row1_col1:

        if st.button(
            "📄 Detailed Notes"
        ):

            with st.spinner(
                "Generating Notes..."
            ):

                output = (
                    generate_detailed_notes(
                        st.session_state.transcript_text
                    )
                )

                st.session_state.generated_output = (
                    output
                )

                st.session_state.output_type = (
                    "Detailed Notes"
                )

#point summary button
    with row1_col2:

        if st.button(
            "📝 Point Summary"
        ):

            with st.spinner(
                "Generating Summary..."
            ):

                output = (
                    generate_point_summary(
                        st.session_state.transcript_text
                    )
                )

                st.session_state.generated_output = (
                    output
                )

                st.session_state.output_type = (
                    "Point Summary"
                )

#flashcards button
    with row1_col3:

        if st.button(
            "🧠 Flashcards"
        ):

            with st.spinner(
                "Creating Flashcards..."
            ):

                output = (
                    generate_flashcards(
                        st.session_state.transcript_text
                    )
                )

                st.session_state.generated_output = (
                    output
                )

                st.session_state.output_type = (
                    "Flashcards"
                )

#quiz button
    with row2_col1:

        if st.button(
            "❓ Quiz Generator"
        ):

            with st.spinner(
                "Generating Quiz..."
            ):

                output = (
                    generate_quiz(
                        st.session_state.transcript_text
                    )
                )

                st.session_state.generated_output = (
                    output
                )

                st.session_state.output_type = (
                    "Quiz"
                )

#timestamp summary button
    with row2_col2:

        if st.button(
            "⏰ Timestamp Summary"
        ):

            with st.spinner(
                "Generating Chapters..."
            ):

                output = (
                    generate_timestamp_summary(
                        st.session_state.timestamped_text
                    )
                )

                st.session_state.generated_output = (
                    output
                )

                st.session_state.output_type = (
                    "Timestamp Summary"
                )

#mindmap button
    with row2_col3:

        if st.button(
            "🗺️ Mind Map"
        ):

            with st.spinner(
                "Creating Mind Map..."
            ):

                output = (
                    generate_mindmap(
                        st.session_state.transcript_text
                    )
                )

                st.session_state.generated_output = (
                    output
                )

                st.session_state.output_type = (
                    "Mind Map"
                )

#OUTPUT SECTION
if st.session_state.generated_output:

    st.divider()

    st.subheader(
        st.session_state.output_type
    )

#if generated output is mindmap
    if (
        st.session_state.output_type
        == "Mind Map"
    ):

        try:

            graph = create_mindmap(
                st.session_state.generated_output
            )

            st.graphviz_chart(
                graph
            )

        except Exception as e:

            st.error(
                f"Graph Error: {e}"
            )

            st.code(
                st.session_state.generated_output
            )

#display text output
    st.markdown(
        st.session_state.generated_output
    )

#save to history
    from utils.database import (
        save_history
    )

    if (
        "saved_once"
        not in st.session_state
    ):

        save_history(
            st.session_state.video_url,
            st.session_state.video_title,
            st.session_state.output_type,
            st.session_state.generated_output
        )

        st.session_state.saved_once = True

#PDF EXPORT SECTION
    st.divider()

    st.subheader(
        "📥 Export"
    )

#detailed notes PDF
    if (
        st.session_state.output_type
        == "Detailed Notes"
    ):

        pdf_path = (
            create_notes_pdf(
                st.session_state.video_title,
                st.session_state.generated_output
            )
        )

#point summary PDF
    elif (
        st.session_state.output_type
        == "Point Summary"
    ):

        pdf_path = (
            create_summary_pdf(
                st.session_state.video_title,
                st.session_state.generated_output
            )
        )

#flashcards PDF
    elif (
        st.session_state.output_type
        == "Flashcards"
    ):

        pdf_path = (
            create_flashcards_pdf(
                st.session_state.video_title,
                st.session_state.generated_output
            )
        )



#quiz PDF
    elif (
        st.session_state.output_type
        == "Quiz"
    ):

        pdf_path = (
            create_quiz_pdf(
                st.session_state.video_title,
                st.session_state.generated_output
            )
        )

#timestamp summary PDF
    elif (
        st.session_state.output_type
        == "Timestamp Summary"
    ):

        pdf_path = (
            create_timestamp_pdf(
                st.session_state.video_title,
                st.session_state.generated_output
            )
        )

#mindmap PDF
    elif (
        st.session_state.output_type
        == "Mind Map"
    ):

        pdf_path = (
            create_mindmap_pdf(
                st.session_state.video_title,
                st.session_state.generated_output
            )
        )

#download button
    with open(
        pdf_path,
        "rb"
    ) as file:

        st.download_button(
            label="📄 Download PDF",
            data=file,
            file_name=os.path.basename(
                pdf_path
            ),
            mime="application/pdf"
        )

#CHAT SECTION
if st.session_state.current_mode == "chat":

    st.divider()

    st.subheader(
        "💬 Chat With Video"
    )

    st.caption(
        "Ask questions about the video content"
    )

#ask question input
    user_question = st.text_input(
        "Ask a question",
        placeholder="What is the main topic discussed?"
    )

#ask button
    if st.button(
        "🚀 Ask"
    ):

        if not user_question:

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching transcript..."
            ):

                try:

                    answer = ask_video(
                        user_question
                    )

                    st.session_state.chat_history.append(
                        {
                            "question": user_question,
                            "answer": answer
                        }
                    )

                except Exception as e:

                    st.error(
                        str(e)
                    )

#display chat history
    if st.session_state.chat_history:

        st.divider()

        for chat in reversed(
            st.session_state.chat_history
        ):

            st.markdown(
                f"""
### 👤 Question

{chat['question']}

### 🤖 Answer

{chat['answer']}
"""
            )

#TRANSCRIPT VIEWER
if st.session_state.transcript_text:

    st.divider()

    with st.expander(
        "📜 View Transcript"
    ):

        st.write(
            st.session_state.transcript_text
        )

#TIMESTAMPED TRANSCRIPT VIEWER
if st.session_state.timestamped_text:

    with st.expander(
        "⏰ View Timestamped Transcript"
    ):

        st.text(
            st.session_state.timestamped_text
        )

#CURRENT LOADED VIDEO INFO
if st.session_state.video_title:

    st.divider()

    st.info(
        f"Loaded Video: {st.session_state.video_title}"
    )

#SIDEBAR STATISTICS
st.divider()

st.subheader(
    "📈 Session"
)

st.write(
    f"History Records: {len(history_items)}"
)

if vector_store_exists():

    st.success(
        "Vector Store Ready"
    )

else:

    st.warning(
        "No Vector Store"
    )

#CLEAR CHAT BUTTON
    if st.button(
        "🗑 Clear Chat"
    ):

        st.session_state.chat_history = []

        st.rerun()

#FOOTER
st.divider()

st.markdown(
    """
### 🎥 VideoIQ AI

AI-Powered YouTube Learning Assistant

Features:

- Detailed Notes
- Point Summary
- Flashcards
- Quiz Generator
- Timestamp Chapters
- Mind Maps
- Chat With Video
- PDF Export
- SQLite History
- FAISS RAG Search

Built with Streamlit + Gemini 2.5 Flash
"""
)

