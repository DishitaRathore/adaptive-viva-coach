# Adaptive Voice Viva Coach

A speech-based practice app for DBMS interview questions. It transcribes spoken answers, checks them against question-specific concepts, provides feedback, and tracks practice by topic.

## Features

- **DBMS question bank:** Questions about SQL basics, normalization, transactions, and indexes.
- **Voice input:** Record an answer in the app and choose English or Hindi.
- **Speech transcription:** Uses Bodhan Indic-Transcribe-Core. The transcript is editable before evaluation.
- **Rubric-based feedback:** An OpenAI model checks the answer against the question’s key points and returns covered concepts and feedback.
- **Adaptive practice:** The app scores concept coverage from 0 to 3. If an answer misses several concepts, it offers one simpler follow-up. You can also skip to the next question.
- **Optional PDF notes:** Extracts selectable text and retrieves up to three relevant excerpts using keyword overlap. Feedback can refer to the source page numbers.
- **Topic-wise progress:** SQLite stores practice attempts. The dashboard shows attempt count, average score, score history, and concepts missed most often.

## How it works

1. Select a DBMS topic and question.
2. Record an answer in English or Hindi.
3. Transcribe it and review or correct the transcript.
4. Optionally upload course notes in PDF format.
5. Evaluate the answer against the question rubric.
6. Review feedback, then retry or continue.
7. View saved attempts and progress for the selected topic.

## Technologies

- Python
- Streamlit
- Bodhan Indic-Transcribe-Core
- OpenAI Responses API
- SQLite
- pypdf

## Project files

```text
adaptive-viva-coach/
├── app.py
├── questions.py
├── tutor.py
├── database.py
├── notes.py
├── requirements.txt
├── .env.example
└── README.md
