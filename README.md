# 🤖 AI Meeting Assistant

> **An AI-powered meeting intelligence platform built from scratch with Python, local Whisper transcription, LLM-powered analysis, RAG, and ChromaDB.**

AI Meeting Assistant transforms meeting recordings, audio/video files, and YouTube videos into structured, searchable meeting intelligence.

The system can transcribe meetings, generate summaries, extract action items, identify key decisions, surface open questions, and provide a conversational interface for asking questions about the meeting using **Retrieval-Augmented Generation (RAG)**.

Built with a focus on **privacy, low-cost AI infrastructure, modular pipelines, and practical production-oriented architecture**.

---

## 🚀 Key Capabilities

### 🎙️ Multi-Source Transcription

Supports multiple meeting input formats:

* YouTube URLs
* Audio files
* Video files
* English meetings
* Hindi meetings
* Hinglish meetings

For English transcription, the application uses **OpenAI Whisper locally**, allowing transcription without sending the audio to a paid transcription service.

For Hindi/Hinglish transcription, the application integrates **Sarvam AI**.

---

### 📝 Intelligent Meeting Analysis

After transcription, the system uses an LLM pipeline to extract structured information from the meeting.

It generates:

* 📌 Executive summary
* 🔹 Key discussion points
* ✅ Action items
* 👤 Action-item owners
* 📅 Deadlines
* 🎯 Key decisions
* ❓ Open questions
* 🔄 Follow-up items

This converts an unstructured meeting transcript into an actionable report.

---

### 💬 Chat With Your Meeting

The application includes a **Retrieval-Augmented Generation (RAG)** pipeline that allows users to ask questions about the meeting.

Example questions:

```text
"What were the main decisions made?"

"Who is responsible for the website redesign?"

"What deadlines were mentioned?"

"What did the team discuss about the marketing campaign?"

"Were there any unresolved issues?"
```

The system retrieves relevant sections from the meeting transcript and provides an answer based on the available context.

---

### 🧠 RAG Architecture

The meeting transcript is processed and converted into embeddings using local **Hugging Face Embeddings**.

The embeddings are stored in **ChromaDB**, which acts as the vector database.

High-level pipeline:

```text
Meeting Audio / Video / YouTube
              ↓
       Audio Extraction
              ↓
       Speech-to-Text
      ┌───────┴────────┐
      ↓                ↓
 Local Whisper     Sarvam AI
 English          Hindi/Hinglish
      └───────┬────────┘
              ↓
       Meeting Transcript
              ↓
        Text Chunking
              ↓
    HuggingFace Embeddings
              ↓
          ChromaDB
              ↓
       Retrieval Pipeline
              ↓
        LLM Generation
              ↓
       Meeting Q&A / Chat
```

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │       Streamlit      │
                    │         UI           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Input Processing  │
                    │ YouTube / Audio /     │
                    │ Video                 │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Transcription      │
                    │                      │
                    │ Whisper / Sarvam AI  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Meeting Transcript    │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ Meeting Analysis │        │   RAG Pipeline   │
       │                  │        │                  │
       │ Summary          │        │ Chunking         │
       │ Action Items     │        │ Embeddings       │
       │ Decisions        │        │ ChromaDB         │
       │ Questions        │        │ Retrieval        │
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
                    ┌──────────────────────┐
                    │   AI Meeting Report  │
                    │   + Conversational   │
                    │       Q&A            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     PDF / TXT        │
                    │      Export          │
                    └──────────────────────┘
```

---

## 🛠️ Technology Stack

| Technology                  | Purpose                               |
| --------------------------- | ------------------------------------- |
| **Python**                  | Core application and AI orchestration |
| **OpenAI Whisper**          | Local speech-to-text transcription    |
| **Sarvam AI**               | Hindi/Hinglish transcription          |
| **LangChain LCEL**          | LLM application pipelines             |
| **Mistral AI**              | LLM-powered meeting analysis and Q&A  |
| **ChromaDB**                | Vector database for RAG               |
| **Hugging Face Embeddings** | Local text embeddings                 |
| **Streamlit**               | Interactive web application           |
| **PDF/TXT Generation**      | Meeting report export                 |

---

## 💡 Why I Built This

Many meeting intelligence platforms rely on recurring subscriptions and cloud-based transcription services.

I wanted to build a practical AI system that demonstrates how modern AI components can be combined into a complete application:

* Local speech recognition
* LLM-based information extraction
* Vector search
* Retrieval-Augmented Generation
* Multilingual AI
* Document generation
* Interactive AI interfaces

The project was also designed around keeping the infrastructure **free or low-cost where possible**, while demonstrating real-world AI engineering concepts.

---

## 🔥 Core AI Engineering Concepts

This project demonstrates hands-on experience with:

### 1. Speech-to-Text

Using Whisper locally to convert meeting audio into text.

### 2. LLM Pipelines

Using LangChain LCEL to construct reusable processing pipelines for meeting analysis.

### 3. Structured Information Extraction

Transforming raw transcripts into structured meeting intelligence:

```text
Transcript
    ↓
LLM Processing
    ↓
Summary
Action Items
Decisions
Questions
Follow-ups
```

### 4. Retrieval-Augmented Generation

Meeting transcripts are transformed into searchable vector representations.

```text
Transcript
    ↓
Chunking
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Similarity Search
    ↓
Relevant Context
    ↓
LLM
    ↓
Answer
```

### 5. Multilingual AI

The application supports English, Hindi, and Hinglish meeting workflows using different transcription systems.

### 6. AI Application Development

The project combines multiple AI components into one end-to-end application rather than implementing an isolated AI model.

---

## 📂 Project Structure

```text
AI-Meeting-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── components/
│   ├── transcription/
│   ├── analysis/
│   ├── rag/
│   └── export/
│
├── data/
│
├── vectorstore/
│
└── utils/
```

> The exact structure may vary depending on the implementation.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-meeting-assistant.git
```

```bash
cd ai-meeting-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
MISTRAL_API_KEY=your_mistral_api_key
SARVAM_API_KEY=your_sarvam_api_key
```

Use `.env.example` as the template.

**Never commit your real API keys to GitHub.**

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🔐 Privacy & Cost Considerations

One of the design goals of this project was to minimize dependency on expensive external services.

### Local Whisper

English audi
