# SAIROBSS AI Core 🤖

> **A modular AI platform powering the SAIROBSS robotics ecosystem through multimodal intelligence, real-time cloud synchronization, computer vision, voice interaction, and distributed hardware control.**

---

## 📌 Overview

SAIROBSS AI Core is the central intelligence platform behind the **SAIROBSS (Swalih Artificial Intelligence Robotic Security System)** ecosystem. Rather than functioning as a traditional chatbot, it serves as the cognitive engine responsible for decision-making, human-robot interaction, cloud synchronization, and intelligent hardware automation.

The platform is designed around a modular and distributed architecture, allowing Raspberry Pi-powered robots, Arduino microcontrollers, mobile applications, and web dashboards to communicate seamlessly through a centralized AI layer.

Its architecture prioritizes scalability, maintainability, and future expansion, making it suitable for integrating new AI models, robotic platforms, sensors, and autonomous capabilities without redesigning the entire system.

---

# 📸 User Interface

## 🏠 Home Dashboard

The primary Streamlit interface used to communicate with the AI, monitor system status, access tools, and control connected robotics hardware.

<img width="959" height="475" alt="Screenshot 2026-07-03 224304" src="https://github.com/user-attachments/assets/8eddf86d-994b-45a5-a512-640a3b2d6df1" />

---

## 🎤 Voice Conversation Interface

Real-time conversational interface supporting wake-word detection, speech recognition, natural language processing, and asynchronous text-to-speech generation.

<img width="959" height="475" alt="Screenshot 2026-07-03 224452" src="https://github.com/user-attachments/assets/4b73664b-5780-4a29-bb87-1e7d88b320e4" />

---

## 🌍 Environmental Monitoring Dashboard

Displays real-time environmental statistics collected by the robot, including:

- Air Quality Index (AQI)
- Temperature
- Humidity
- VOC Levels
- Environmental Reports

<img width="959" height="475" alt="Screenshot 2026-07-03 224330" src="https://github.com/user-attachments/assets/ca9fe0f1-8f82-4770-adb3-aff3c64c5ebd" />

---

# 🏗 System Architecture

To reduce computational load on edge devices while maintaining responsive AI performance, the platform follows a distributed server-client architecture.

```text
                ┌────────────────────────┐
                │ Streamlit Web Dashboard│
                └────────────┬───────────┘
                             │
                             │
      ┌──────────────────────┼──────────────────────┐
      │                      │                      │
      ▼                      ▼                      ▼
Android App          Firebase Realtime DB     AI Core Engine
(Kodular)                  (Cloud)            (Python Server)
                             │
                             ▼
                    Raspberry Pi Gateway
                             │
                             ▼
                    Arduino Controllers
                             │
                             ▼
                       Robot Hardware
```

The cloud layer acts as the synchronization bridge between every component, ensuring low-latency communication between the AI, mobile application, web dashboard, and physical robotic hardware.

---

# ⚙ Technical Stack

### Programming Languages

- Python 3.10+
- Arduino C++

### AI & Machine Learning

- Groq API
- Hugging Face
- Custom AI Function Calling

### User Interfaces

- Streamlit
- Kodular Android Application

### Database & Cloud

- Firebase Realtime Database
- Firebase Admin SDK

### Audio Processing

- Speech Recognition
- Edge-TTS
- Wake Word Detection

### Hardware

- Raspberry Pi
- Arduino
- USB Serial Communication

### Automation

- PyAutoGUI
- Pynput
- PyWhatKit

---

# 🚀 Core Features

## 🤖 Robotics Intelligence

- Natural language understanding
- AI decision making
- Robot command execution
- Hardware abstraction layer
- Multi-device synchronization

---

## 🎤 Voice Interaction

- Wake-word activation
- Speech-to-Text
- Text-to-Speech
- Real-time conversations
- Continuous listening pipeline

---

## 👀 Computer Vision

- Face Recognition
- Face Identification
- Object Recognition
- Object Detection
- Gesture Recognition
- QR Code Recognition
- Distance Estimation

---

## 🌍 Environmental Intelligence

- Air Quality Monitoring
- Temperature Monitoring
- Humidity Monitoring
- VOC Detection
- Environmental Reports

---

## 🌐 AI Search

- Live Weather Search
- News Search
- AI-powered Internet Search

---

## 📱 Cross Platform Support

- Desktop Dashboard
- Android Application
- Raspberry Pi Gateway
- Cloud Synchronization

---

# 🧠 Engineering Challenges Solved

## 1️⃣ Multi-Threaded Voice Processing

Traditional speech recognition blocks the execution of applications while waiting for user input.

To eliminate this limitation, the AI separates speech recognition, wake-word detection, and UI rendering into independent execution pipelines, allowing continuous conversation without freezing the interface.

---

## 2️⃣ Intelligent Function Calling

Instead of relying on fragile keyword matching, the AI interprets natural language requests and converts them into structured function calls.

These commands are automatically translated into hardware instructions, Firebase updates, automation tasks, or operating system actions.

---

## 3️⃣ Distributed Cloud Synchronization

Maintaining synchronization between a desktop dashboard, Android application, Raspberry Pi, and robotic hardware requires efficient state management.

Firebase serves as the centralized communication layer, allowing every connected device to receive updates almost instantly while preventing conflicting state changes.

---

## 4️⃣ Hardware Abstraction

Rather than communicating directly with hardware from every software component, all physical interactions are routed through the Raspberry Pi gateway.

This design keeps the AI independent from hardware implementation details and makes future upgrades significantly easier.

---

# 📂 Project Structure

```
SAIROBSS-AI-Core/

├── chat.py
├── ai_functions.py
├── ras_functions.py
├── assets/
│   └── images/
└── README.md
```

### chat.py

Controls the Streamlit dashboard, chat interface, session history, UI rendering, and user interaction.

### ai_functions.py

Handles AI orchestration, Groq communication, Firebase updates, voice generation, and intelligent function execution.

### ras_functions.py

Contains Raspberry Pi-specific hardware communication routines, serial interfaces, and robotics control functions.

---

# 🔮 Future Development

Planned future improvements include:

- ROS 2 Integration
- Local Large Language Models
- Autonomous Navigation
- Improved Computer Vision
- Multi-Robot Communication
- Memory Engine
- Plugin Architecture
- Advanced Behaviour Learning
- Vision-Language Models
- Smart Home Integration
- Offline AI Support

---

# 🎯 Project Significance

This project demonstrates practical experience in several engineering disciplines:

- Distributed Systems
- Robotics Software Engineering
- Cloud Synchronization
- Computer Vision
- Artificial Intelligence
- Embedded Systems
- Hardware Communication
- Voice Processing
- Human-Robot Interaction
- Full Stack Development

Rather than focusing on isolated AI features, the project demonstrates the design of a scalable intelligence platform capable of powering future robotic systems.

---

# 🔒 Security Notice

Sensitive project assets have been intentionally excluded from the public repository, including:

- Firebase service credentials
- API keys
- Cloud configuration files
- Private endpoints
- Authentication tokens

This repository focuses on demonstrating the software architecture and engineering implementation while maintaining responsible security practices.

---

# 👨‍💻 Developer

**Mohammed Swalih**

AI • Robotics • Embedded Systems • Computer Vision • Automation

Building intelligent robotics systems for the future.

---
⭐ *If you found this project interesting, consider giving it a star!*
