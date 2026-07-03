# SAIROBSS AI Core 🤖🛰️ | Distributed Cloud & Multi-Threaded Intelligent Agent

The central cognitive processing engine and real-time state synchronization hub designed for the SAIROBSS robotic ecosystem. This repository contains the distributed AI architecture, low-latency audio execution pipelines, and a dual-UI synchronization layer that handles complex human-robot interaction loops.

---

## 🏗️ System Architecture & Distributed Data Topology

To optimize processing capability and prevent hardware bottlenecks on edge controllers (Raspberry Pi), the system employs a decoupled, event-driven server-client model. 

```text
[ Streamlit Web Server ] ──┐
                           ├──> [ Firebase Realtime Cloud ] <──> [ Raspberry Pi Gateway ] <──> [ Arduino Low-Level Pins ]
[ Kodular Mobile Client ] ─┘
```
1. **The Brain (AI Server Core):** Operates asynchronously on high-compute local environments, maintaining a multi-threaded Streamlit dashboard, listening for voice cues, evaluating Groq LLM inference requests, and outputting real-time system mutations.
2. **The Cloud State Layer (Firebase):** Acts as a low-latency transactional bridge ensuring the Web Application and the custom **Kodular Android Mobile App** maintain a uniform state.
3. **The Edge Gateway (Raspberry Pi & Arduino):** A headless physical gateway running background loop listeners that intercept structural command nodes from the cloud layer and pipe them over hardware Serial connections (`/dev/ttyACM0`) to execute micro-pin commands natively.

---

## 🛠️ Technical Stack & Software Core

* **Core Execution Framework:** Python 3.10+
* **User Interfaces:** Streamlit (Desktop Web Console), Kodular Framework (Android Mobile Client Wrapper)
* **Inference Pipeline:** Groq SDK (Ultra-fast LLM orchestration), Hugging Face Hub (Edge validation models)
* **Audio Synthesis:** Edge-TTS (Asynchronous Text-to-Speech stream synthesis)
* **State Engine:** Firebase Admin SDK (Real-time Cloud Database pipelines)
* **Automation Engineering:** PyAutoGUI & Pynput (System-level UI emulation and peripheral macro integration)

---

## 🚀 Key Engineering & Structural Challenges Solved

### 1. Multi-Threaded Audio Pipeline & Asynchronous Wake Word Logic
Running real-time Speech-to-Text (STT) and text stream synthesis inside a web loop usually results in terminal blocking, halting incoming user messages or database checks.
* Implemented a persistent conversational state management loop wrapped in an alert trigger cascade (`wake_beep.mp3`).
* Isolated speech listening routines (`listen_record_transcribe`) from the main display threads, allowing users to talk seamlessly without interrupting state listeners.

### 2. Algorithmic Function Calling & Hardware Automation Intercepts
Instead of using basic, brittle hardcoded keyword matching, the AI handles unstructured user intent and maps it to clean execution blocks using Groq function calls.
* The system evaluates complex user queries, extracts operational JSON arguments, and updates Firebase nodes instantaneously.
* **Automation Fallback:** Leveraged `PyAutoGUI` and `pywhatkit` to build localized automation bridges, translating linguistic intent into direct software-level macros, OS interactions, and scheduled communication dispatches.

### 3. Cross-Platform Dual-Frontend State Management
Synchronizing a web interface and an Android application simultaneously without creating race conditions or infinite feedback loops requires strict data filtering.
* Engineered data transaction loops via `firebase_admin.db`. When parameters are altered inside the Kodular mobile client, the data changes propagate to Firebase, triggering the Streamlit application's `check_message` logic instantly.
* Built automatic image cleanup caching mechanisms to purge generated asset artifacts (`generated_image*`) on startup, conserving local processing storage footprints.

---

## 📋 Module & Component Breakdown

* **`chat.py`:** Controls the primary Streamlit presentation engine, utilizing custom layout components, managing historical user chat transcripts natively in session states, and plotting systemic analytical graph vectors.
* **`ai_functions.py`:** Houses the transactional logic for model orchestration, custom voice preset layouts (`en-US-AndrewNeural`), prompt vector injection configurations, and cloud database state manipulation queries.
* **`ras_functions.py`:** Contains targeted edge routines, camera matrices, and hardware-level `serial.Serial` interfaces tailored specifically for executing commands directly inside the Raspberry Pi subsystem environment.

---

## 🧑‍💻 Project Significance for Recruiters

* **Decoupled Architecture:** Demonstrates deep practical knowledge of modern distributed microservice methodologies—keeping frontend presentation, cloud databases, and hardware control safely separated.
* **Low-Latency Synthesis:** Focuses heavily on reducing user friction, optimizing speech rendering, caching local parameters, and tuning API parameters to minimize system delays.
* **Production Adaptability:** Moves beyond basic Python console loops by delivering real-world utility across physical robotic hardware, a web console dashboard, and an Android mobile app simultaneously.

> 🔒 **Compliance & Asset Disclosure Note:** In accordance with personal data privacy guidelines and software protection protocols, exact Firebase SDK administration certificates (`json` configurations), unique private operational API endpoints, and direct cloud configuration parameters have been excluded from the public codebase.
