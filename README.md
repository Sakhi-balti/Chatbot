# 🤖 AI Chatbot - LangGraph & Streamlit

A modern, production-ready chatbot application built with LangGraph and Streamlit, featuring a clean separation between frontend and backend without the complexity of API servers.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.0.20-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🌟 Overview

This chatbot application demonstrates best practices for building conversational AI systems with:
- **LangGraph** for stateful conversation management
- **DeepSeek-V3** language model via Hugging Face
- **Streamlit** for an intuitive web interface
- Clean separation between UI and business logic

Perfect for developers looking to build production-ready chatbots without the overhead of managing API servers.

## ✨ Features

### Core Functionality
- 💬 **Real-time Chat Interface** - Smooth conversational experience
- 🧠 **Conversation Memory** - Maintains context across multiple turns
- 🔄 **Session Management** - Multiple conversation threads
- 📊 **Statistics Dashboard** - Track message counts and usage

### Advanced Features
- ⚙️ **Adjustable Settings** - Control temperature and token limits
- 💾 **Export Conversations** - Download chat history as text files
- 📥 **Load History** - Resume previous conversations
- 🔍 **Health Monitoring** - Real-time backend status checks
- 🎨 **Modern UI** - Clean, responsive interface with dark theme

### Developer Features
- 🏗️ **Modular Architecture** - Separated frontend and backend
- 🐛 **Easy Debugging** - Direct function calls, no HTTP overhead
- 📝 **Well Documented** - Comprehensive code comments
- 🧪 **Testable** - Backend can be tested independently

## 🏗️ Architecture
