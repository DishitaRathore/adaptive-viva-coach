import hashlib
import os
import sys
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import snapshot_download

from database import (
    get_recent_attempts,
    get_topic_progress,
    initialize_database,
    save_attempt,
)
from notes import extract_pdf_pages, retrieve_relevant_pages
from questions import QUESTION_BANK
from tutor import evaluate_answer


PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env")


@st.cache_resource
def load_asr():
    """Download the model if needed, then reuse it while Streamlit is running."""
    model_dir = snapshot_download("bodhan-ai/indic-transcribe-core")

    if model_dir not in sys.path:
        sys.path.insert(0, model_dir)

    from indic_transcribe import IndicTranscribe

    return IndicTranscribe.from_pretrained(model_dir)


def calculate_score(required_points, covered_points):
    """Return a score from 0 to 3 based on rubric coverage."""
    total = len(required_points)
    covered = len(covered_points)

    if total == 0 or covered == 0:
        return 0
    if covered == total:
        return 3
    if covered >= (total + 1) // 2:
        return 2
    return 1


st.set_page_config(page_title="Voice Viva Coach", page_icon="🎓")
initialize_database()

st.title("🎓 Voice Viva Coach")
st.write(
    "Practise DBMS interview questions aloud. The app transcribes your answer, "
    "checks it against key concepts, and gives feedback."
)
st.info(
    "The speech model runs on your computer. Your transcript and the selected "
    "PDF excerpts are sent to the text-model API for evaluation. The complete "
    "PDF stays on your computer."
)

topic = st.selectbox(
    "Choose a DBMS topic",
    list(QUESTION_BANK.keys()),
    format_func=lambda value: value.replace("_", " ").title(),
)

# Reset the question sequence when the selected topic changes.
if st.session_state.get("active_topic") != topic:
    st.session_state.active_topic = topic
    st.session_state.question_index = 0
    st.session_state.retry_mode = False
    st.session_state.retry_points = []
    st.session_state.last_result = None
    st.session_state.audio_version = st.session_state.get("audio_version", 0) + 1

question_bank = QUESTION_BANK[topic]
question_index = st.session_state.question_index
base_question = question_bank[question_index]
retry_mode = st.session_state.retry_mode

if retry_mode:
    question_text = base_question["retry_question"]
    rubric_points = st.session_state.retry_points
    st.caption("Follow-up question")
else:
    question_text = base_question["question"]
    rubric_points = base_question["key_points"]

st.markdown(f"### {question_text}")

if st.button("Skip to next question"):
    st.session_state.retry_mode = False
    st.session_state.retry_points = []
    st.session_state.question_index = (
        question_index + 1
    ) % len(question_bank)
    st.session_state.audio_version += 1
    st.rerun()

# Optional course notes PDF.
uploaded_pdf = st.file_uploader(
    "Optional: upload your DBMS notes as a PDF",
    type=["pdf"],
    key="notes_pdf_upload",
)

retrieved_sources = []

if uploaded_pdf is None:
    st.session_state.pop("notes_pdf_fingerprint", None)
    st.session_state.pop("notes_pdf_pages", None)
else:
    pdf_bytes = uploaded_pdf.getvalue()
    pdf_fingerprint = hashlib.sha256(pdf_bytes).hexdigest()

    if st.session_state.get("notes_pdf_fingerprint") != pdf_fingerprint:
        try:
            with st.spinner("Reading your PDF notes..."):
                extracted_pages = extract_pdf_pages(pdf_bytes)

            st.session_state.notes_pdf_fingerprint = pdf_fingerprint
            st.session_state.notes_pdf_pages = extracted_pages

        except Exception as error:
            st.error(f"Could not read this PDF: {error}")
            st.session_state.notes_pdf_pages = []

    pdf_pages = st.session_state.get("notes_pdf_pages", [])

    if not pdf_pages:
        st.warning(
            "No selectable text was found in this PDF. It may be scanned; "
            "this version does not run OCR."
        )
    else:
        retrieval_query = (
            question_text
            + "\n"
            + "\n".join(rubric_points)
        )
        retrieved_sources = retrieve_relevant_pages(
            pdf_pages,
            retrieval_query,
            top_k=3,
        )

        if retrieved_sources:
            with st.expander("Relevant excerpts found in your notes"):
                for excerpt in retrieved_sources:
                    st.markdown(f"**PDF page {excerpt['page']}**")
                    st.write(excerpt["text"])
        else:
            st.caption(
                "No matching passages were found in the uploaded notes. "
                "Feedback will use the question rubric."
            )

language_choice = st.selectbox(
    "Answer language",
    ["English", "Hindi"],
    help="For a Hindi or Hinglish answer, choose Hindi.",
)
language_code = {"English": "en", "Hindi": "hi"}[language_choice]

audio_version = st.session_state.audio_version
answer_key = f"answer_text_{audio_version}"

audio = st.audio_input(
    "Record your answer",
    sample_rate=16000,
    key=f"audio_{audio_version}",
)

if audio and st.button("Transcribe my answer", key=f"transcribe_{audio_version}"):
    audio_path = None

    try:
        with st.spinner("Loading the speech model and transcribing..."):
            asr = load_asr()

            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False,
            ) as audio_file:
                audio_file.write(audio.getvalue())
                audio_path = audio_file.name

            transcript = asr.transcribe(audio_path, lang=language_code)

        st.session_state[answer_key] = transcript
        st.success("Transcript ready. Review or correct it below.")

    except Exception as error:
        st.error(f"Transcription failed: {error}")

    finally:
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)

answer_text = st.text_area(
    "Review or correct your transcript",
    key=answer_key,
    height=150,
)

if st.button("Evaluate answer", disabled=not answer_text.strip()):
    try:
        with st.spinner("Checking your answer against the key concepts..."):
            evaluation_question = {
                "question": question_text,
                "key_points": rubric_points,
            }
            review = evaluate_answer(
                evaluation_question,
                answer_text,
                source_excerpts=retrieved_sources,
            )

        covered_points = [
            point
            for point in rubric_points
            if point in review["covered_points"]
        ]
        missing_points = [
            point
            for point in rubric_points
            if point not in covered_points
        ]
        score = calculate_score(rubric_points, covered_points)

        source_pages = sorted({
            excerpt["page"] for excerpt in retrieved_sources
        })

        save_attempt(
            topic=topic,
            question=question_text,
            transcript=answer_text,
            score=score,
            covered_points=covered_points,
            missing_points=missing_points,
            feedback=review["feedback"],
        )

        st.session_state.last_result = {
            "question": question_text,
            "score": score,
            "covered_points": covered_points,
            "missing_points": missing_points,
            "feedback": review["feedback"],
            "source_pages": source_pages,
        }

        # Give one simpler retry if the initial answer missed several concepts.
        if not retry_mode and score <= 1 and missing_points:
            st.session_state.retry_mode = True
            st.session_state.retry_points = missing_points
        else:
            st.session_state.retry_mode = False
            st.session_state.retry_points = []
            st.session_state.question_index = (
                question_index + 1
            ) % len(question_bank)

        # A new widget key clears the old recording and transcript.
        st.session_state.audio_version += 1
        st.rerun()

    except Exception as error:
        st.error(f"Evaluation or saving failed: {error}")

if st.session_state.last_result:
    result = st.session_state.last_result

    st.markdown("---")
    st.subheader("Previous answer feedback")
    st.write(f"**Question:** {result['question']}")
    st.write(f"**Score:** {result['score']} / 3")
    st.write(f"**Feedback:** {result['feedback']}")

    if result["source_pages"]:
        page_labels = ", ".join(
            f"page {page}" for page in result["source_pages"]
        )
        st.caption(f"Relevant notes supplied to the evaluator: {page_labels}")

    if result["covered_points"]:
        st.write("**Concepts covered:**")
        for point in result["covered_points"]:
            st.write(f"- {point}")

    if result["missing_points"]:
        st.write("**Concepts to practise:**")
        for point in result["missing_points"]:
            st.write(f"- {point}")

st.markdown("---")
st.subheader("Progress dashboard")

progress = get_topic_progress(topic)

if progress["attempt_count"]:
    col1, col2 = st.columns(2)
    col1.metric("Attempts", progress["attempt_count"])
    col2.metric("Average score", f"{progress['average_score']:.1f} / 3")

    st.write("**Score across your last 20 attempts:**")
    st.line_chart(progress["score_history"])

    if progress["weak_points"]:
        st.write("**Concepts to revisit most often:**")
        for point, count in progress["weak_points"]:
            st.write(f"- {point} — missed {count} time(s)")
else:
    st.write("Complete an evaluation to see your progress for this topic.")

st.markdown("---")
st.subheader("Recent practice")

attempts = get_recent_attempts(topic)

if attempts:
    st.dataframe(attempts, use_container_width=True)
else:
    st.write("Your attempts for this topic will appear here.")