# Intelligent AI Agent with Conversational Interaction and Text-to-Speech

## 1. Project Overview

This project is an Intelligent AI Agent designed to provide conversational interaction using a Large Language Model (LLM).

The agent can understand user requests, generate natural-language responses, maintain conversation context, use external tools for specific tasks, accept microphone input, and convert AI-generated responses into speech.

The project uses Google's Gemini model as the AI engine and Streamlit as the user interface.

---

## 2. Objectives

The main objectives of this project are:

* To build an intelligent conversational AI agent.
* To integrate a Large Language Model.
* To maintain conversation context during a session.
* To integrate tools for performing specific tasks.
* To provide mathematical calculations through a calculator tool.
* To provide current date and time information.
* To implement Text-to-Speech functionality.
* To implement Speech-to-Text voice input.
* To provide a simple and user-friendly interface.
* To demonstrate practical AI agent architecture.

---

## 3. Main Features

### Conversational AI

The agent can answer general questions and communicate with the user using natural language through Google's Gemini model.

### Conversation Memory

The application stores messages during the current Streamlit session so that the agent can use previous conversation context.

### Calculator Tool

The agent can use a calculator tool for mathematical expressions instead of relying on manual calculation.

### Date and Time Tool

The agent can retrieve the current date and time when requested.

### Text-to-Speech

AI-generated responses can be converted into speech using Google Text-to-Speech (gTTS).

### Speech-to-Text Voice Input

Users can record their voice through the Streamlit interface. The recorded audio is converted into text using the SpeechRecognition library and then processed by the AI agent.

### Voice Responses

Users can enable or disable AI voice responses through the application's voice-response control.

### Clear Conversation

Users can clear the current conversation and start a new session.

### User Interface

The application provides a customized Sakura-inspired interface with styled chat messages, buttons, microphone input, and other interface elements.

---

## 4. Technologies Used

* Python
* Streamlit
* Google Gemini API
* Google GenAI Python SDK
* gTTS
* SpeechRecognition
* python-dotenv
* Python AST
* PowerShell / VS Code

---

## 5. Project Structure

```text
AI_Agent_Project/
|
|-- app.py
|-- tools.py
|-- check_models.py
|-- requirements.txt
|-- README.md
|-- .env
|-- .gitignore
`-- .venv/
```

> The `.env` file contains the Gemini API key and should never be shared publicly.

---

## 6. Requirements

The project requires Python and the packages listed in `requirements.txt`.

The main dependencies include:

* Streamlit
* Google GenAI
* python-dotenv
* gTTS
* SpeechRecognition

---

## 7. Configuration

The Gemini API key is stored in an environment file.

Create a `.env` file in the project directory:

```text
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your Gemini API key.

Do not publish or share the `.env` file.

---

## 8. Installation

### Step 1: Open the project directory

Open PowerShell or a terminal inside the project folder.

### Step 2: Create a virtual environment

```powershell
python -m venv .venv
```

### Step 3: Activate the virtual environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 4: Install the dependencies

```powershell
pip install -r requirements.txt
```

### Step 5: Configure the API key

Create the `.env` file and add:

```text
GEMINI_API_KEY=your_api_key_here
```

---

## 9. Running the Application

Start the Streamlit application with:

```powershell
streamlit run app.py
```

Streamlit will provide a local URL that can be opened in a web browser.

---

## 10. How the AI Agent Works

The general workflow of the application is:

```text
User
  |
  v
Streamlit Interface
  |
  v
Text Input / Microphone Input
  |
  v
Conversation History
  |
  v
Gemini AI Model
  |
  +----------------------+
  |                      |
  v                      v
General Response       Tool Request
                         |
                    +----+----+
                    |         |
                    v         v
               Calculator   Date/Time
                    |         |
                    +----+----+
                         |
                         v
                    Tool Result
                         |
                         v
                    Gemini Model
                         |
                         v
                   Final Response
                         |
                  +------+------+
                  |             |
                  v             v
               Display      Text-to-Speech
```

---

## 11. Voice Interaction

The application supports two voice-related features:

### Speech-to-Text

The user can record audio through the microphone input. The recorded speech is converted into text and sent to the AI agent.

### Text-to-Speech

The generated AI response can be converted into speech using gTTS when voice responses are enabled.

---

## 12. Security

The Gemini API key is stored in `.env` rather than directly inside the Python source code.

The `.gitignore` file excludes:

```text
.env
.venv/
__pycache__/
```

This helps prevent the API key and local environment files from being accidentally committed to Git.

---

## 13. Project Outcome

The completed project demonstrates an AI agent that combines:

* Large Language Model interaction
* Conversation memory
* Tool/API integration
* Mathematical calculations
* Date and time retrieval
* Speech-to-Text
* Text-to-Speech
* Voice interaction
* Streamlit-based user interface

The project demonstrates how multiple AI-agent components can be integrated into a single conversational application using Python.
