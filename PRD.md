# Product Requirements Document: CodeMind Vault

## 1. Overview
CodeMind Vault is an AI-powered code snippet manager designed for developers. It allows users to store, organize, and collaborate on code snippets in real-time, leveraging AI to automatically document, format, and explain code.

## 2. Tech Stack
- **Backend**: Django, Django REST Framework, Django Channels (WebSockets), Redis.
- **Frontend**: React 19, Vite, Tailwind CSS, Monaco Editor (`@monaco-editor/react`).
- **AI Integration**: Google Gemini API (or OpenAI API) for code processing.
- **Database**: SQLite (Development) / PostgreSQL (Production).

## 3. Core Features

### 3.1 AI Auto-Documenter
- Users paste raw, undocumented code snippets.
- Click "AI Enhance" button.
- Backend sends code to an LLM.
- LLM returns formatted code, auto-generated inline comments, and a short, human-readable summary.

### 3.2 Live Collaboration Room
- Snippets can be opened in a "Live Room" with a unique shareable URL.
- Multiple users can view and edit the snippet simultaneously.
- WebSockets handle real-time text updates to keep all clients in sync.

### 3.3 Advanced Search & Organization
- Tags and Folder support for organization.
- Fuzzy search to find snippets based on intent or keywords.

### 3.4 Premium Developer UI
- Dark mode default with neon accents.
- Syntax highlighting via Monaco Editor (same engine as VS Code).
- Glassmorphic UI elements and subtle micro-animations for a premium feel.

## 4. User Flow
1. **Dashboard**: User views recent snippets, folders, and search bar.
2. **Creation**: User clicks "New Snippet", pastes code, uses "AI Enhance" to clean it up, and saves.
3. **Collaboration**: User clicks "Share Live", sends link to a colleague, colleague joins, both edit the code in real-time.
