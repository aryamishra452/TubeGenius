#imports
import traceback
import sys

print("PYTHON EXECUTABLE:")
print(sys.executable)

import os
import streamlit as st

import base64

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
    create_mindmap,save_graph
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

.stApp {

    background:

    /* Top white glow */
    radial-gradient(
        circle at 50% -10%,
        rgba(255,255,255,0.65) 0%,
        rgba(255,255,255,0.18) 18%,
        transparent 40%
    ),

    /* Middle blue glow */
    radial-gradient(
        ellipse at center,
        rgba(56,189,248,0.22) 0%,
        rgba(56,189,248,0.08) 25%,
        transparent 50%
    ),

    /* Base background */
    linear-gradient(
        180deg,
        #071426 0%,
        #0A1B2E 35%,
        #04121F 100%
    );

    background-attachment: fixed;
}

            
/* Remove white/gray gaps */
[data-testid="stAppViewContainer"] {
    background: transparent;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: rgba(10,10,20,0.85);
}
            
.main {
    background: transparent;
    padding-top: 1rem;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 1rem;
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

.footer-container {
    text-align: center;
    width: 100%;
    margin-top: 20px;
    color: #9CA3AF;
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

if "loaded_url" not in st.session_state:
    st.session_state.loaded_url = ""


#App Header
col1, col2 = st.columns([1, 8],vertical_alignment="center")

with col1:
    st.image("assets/logo.png", width=1500)

with col2:
    st.title("TubeGenius")
    st.markdown(
        """
        <p style='font-size:17px; color:#9CA3AF;'>
        AI-Powered YouTube Learning Assistant
        </p>
        """,
        unsafe_allow_html=True
    )
with st.container(border=True):

    st.markdown(
        "<h4 style='text-align:center;'>Learn Faster With Any YouTube Video</h4>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "Notes • Summaries • Flashcards • Quizzes • Mind Maps • AI Chat"
        "</p>",
        unsafe_allow_html=True
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
    "Paste YouTube Video Watch URL"
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

# Auto Load Video

current_url = youtube_url.strip()

if (
    current_url
    and
    current_url != st.session_state.get(
        "loaded_url",
        ""
    )
):

    try:

        st.session_state.loaded_url = (
            current_url
        )

        package = (
            get_full_transcript_package(
                current_url
            )
        )

        st.session_state.transcript_text = (
            package["transcript_text"]
        )

        st.session_state.timestamped_text = (
            package["timestamped_transcript"]
        )

        video_info = (
            get_video_info(
                current_url
            )
        )

        st.session_state.video_title = (
            video_info["title"]
        )

        st.session_state.video_author = (
            video_info["author"]
        )

        st.session_state.video_thumbnail = (
            video_info["thumbnail"]
        )

        st.success(
            f"Loaded: {video_info['title']}"
        )

    except Exception as e:

        st.error(
            f"Error loading video: {e}"
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

    # Mind Map Output
    if (
        st.session_state.output_type
        == "Mind Map"
    ):

        try:

            graph = create_mindmap(
                st.session_state.generated_output
            )

            st.graphviz_chart(
                graph,
                use_container_width=True
            )


        except Exception:

            st.code(
                traceback.format_exc()
            )

            st.code(
                st.session_state.generated_output
            )

    # Timestamp Summary Output
    elif (
        st.session_state.output_type
        == "Timestamp Summary"
    ):

        formatted_output = (
            st.session_state.generated_output
            .replace("00:", "\n\n00:")
            .replace("01:", "\n\n01:")
            .replace("02:", "\n\n02:")
            .replace("03:", "\n\n03:")
            .replace("04:", "\n\n04:")
            .replace("05:", "\n\n05:")
            .replace("06:", "\n\n06:")
            .replace("07:", "\n\n07:")
            .replace("08:", "\n\n08:")
            .replace("09:", "\n\n09:")
            .replace("10:", "\n\n10:")
            .replace("11:", "\n\n11:")
            .replace("12:", "\n\n12:")
            .replace("13:", "\n\n13:")
            .replace("14:", "\n\n14:")
            .replace("15:", "\n\n15:")
            .replace("16:", "\n\n16:")
            .replace("17:", "\n\n17:")
            .replace("18:", "\n\n18:")
            .replace("19:", "\n\n19:")
            .replace("20:", "\n\n20:")
        )

        st.markdown(
            formatted_output
        )

    # All Other Outputs
    else:

        st.markdown(
            st.session_state.generated_output
        )

    # Save History
    from utils.database import (
        save_history
    )

    if not st.session_state.get(
        "saved_once",
        False
    ):

        save_history(
            st.session_state.video_url,
            st.session_state.video_title,
            st.session_state.output_type,
            st.session_state.generated_output
        )

        st.session_state.saved_once = True

    # PDF EXPORT SECTION
    st.divider()

    st.subheader(
        "📥 Export"
    )

    pdf_path = None

    # Detailed Notes
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

    # Point Summary
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

    # Flashcards
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

    # Quiz
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

    # Timestamp Summary
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

    # Mind Map
    elif (
     st.session_state.output_type== "Mind Map"
    ):

     graph = create_mindmap(
        st.session_state.generated_output
     )

     image_path = save_graph(
        graph,
        "mindmap"
     )

     with open(
        image_path,
        "rb"
     ) as file:

        st.download_button(
            label="🖼 Download Mind Map PNG",
            data=file,
            file_name="mindmap.png",
            mime="image/png"
        )

    # Download Button
    if pdf_path:

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

    user_question = st.text_input(
        "Ask a question",
        placeholder="What is the main topic discussed?"
    )

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


#CURRENT LOADED VIDEO INFO
if st.session_state.video_title:

    st.divider()

    st.info(
        f"Loaded Video: {st.session_state.video_title}"
    )

    if st.button(
        "🗑 Clear Chat"
    ):

        st.session_state.chat_history = []

        st.rerun()


#FOOTER
st.markdown("""
<div class="footer-container">

Made by <b>Arya Mishra</b>
<br>
<a href="https://www.linkedin.com/in/arya-m4/">LinkedIn</a> •
<a href="https://github.com/aryamishra452">GitHub</a> •
<a href="https://x.com/AryaMishra45235">Twitter/X</a> •
<a href="https://www.instagram.com/about_aryaa_?igsh=MXF1YXoxYzEwZzEwNg==">Instagram</a>
<br>
© 2026 TubeGenius

</div>
""", unsafe_allow_html=True)