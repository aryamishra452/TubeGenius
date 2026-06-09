# ==========================================
# DETAILED NOTES
# ==========================================

DETAILED_NOTES_PROMPT = """
You are an expert note-taking assistant.

Analyze the provided YouTube transcript and create comprehensive study notes.

Requirements:

1. Use proper headings.
2. Use sub-headings where needed.
3. Explain important concepts.
4. Include examples if mentioned.
5. Keep content structured.
6. Remove repetitive information.
7. Make notes suitable for exam preparation.
8. Use markdown formatting.

Transcript:

{transcript}
"""


# ==========================================
# POINT WISE SUMMARY
# ==========================================

POINT_SUMMARY_PROMPT = """
You are an expert summarizer.

Create a concise point-wise summary.

Requirements:

1. Maximum 15 points.
2. Each point should be meaningful.
3. Avoid repetition.
4. Highlight important takeaways.
5. Use bullet points.

Transcript:

{transcript}
"""


# ==========================================
# FLASHCARDS
# ==========================================

FLASHCARD_PROMPT = """
You are a learning assistant.

Generate flashcards from the transcript.

Requirements:

1. Create 15 flashcards.
2. Format:

Q: Question

A: Answer

3. Cover important concepts only.
4. Questions should test understanding.
5. Keep answers concise.

Transcript:

{transcript}
"""


# ==========================================
# QUIZ GENERATOR
# ==========================================

QUIZ_PROMPT = """
You are an assessment generator.

Create a quiz from the transcript.

Requirements:

1. Generate 10 MCQs.
2. Provide 4 options.
3. Mark correct answer.
4. Include explanation.
5. Cover different concepts.

Format:

Question:

A)
B)
C)
D)

Correct Answer:

Explanation:

Transcript:

{transcript}
"""


# ==========================================
# TIMESTAMP SUMMARY
# ==========================================

TIMESTAMP_SUMMARY_PROMPT = """
You are an expert content analyzer.

Analyze the transcript containing timestamps.

Create chapter-style summaries.

Requirements:

1. Identify topic changes.
2. Create meaningful chapter names.
3. Each chapter must be on a NEW LINE.
4. Mention timestamps.
5. Keep format:

00:00 Introduction

03:25 Topic Name

07:15 Topic Name

10:00 Topic Name

Do not create fake timestamps.

Transcript:

{transcript}
"""


# ==========================================
# MINDMAP / FLOWCHART
# ==========================================

MINDMAP_PROMPT = """
You are an expert knowledge architect.

Analyze the transcript and create a hierarchical mind map.

IMPORTANT:

Return ONLY hierarchy.

Use EXACTLY this format:

Main Topic

    Branch 1

        Subpoint 1

        Subpoint 2

    Branch 2

        Subpoint 1

        Subpoint 2

Rules:

- Maximum 5 branches.
- Maximum 3 subpoints per branch.
- Use indentation only.
- Do NOT use bullets.
- Do NOT use numbering.
- Do NOT use paragraphs.
- Keep node labels under 5 words.
- Keep labels concise.

Transcript:

{transcript}
"""

# ==========================================
# CHAT WITH VIDEO
# ==========================================

CHAT_PROMPT = """
You are a helpful AI assistant.

Use ONLY the provided transcript context.

If answer is not found in context,
say:

'I could not find this information in the video.'

Context:

{context}

Question:

{question}
"""


# ==========================================
# TRANSCRIPT CLEANER
# ==========================================

TRANSCRIPT_CLEANER_PROMPT = """
Clean the transcript.

Requirements:

1. Remove filler words.
2. Remove repeated words.
3. Keep meaning unchanged.
4. Return cleaned transcript.

Transcript:

{transcript}
"""