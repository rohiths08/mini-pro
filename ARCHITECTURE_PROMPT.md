# Architecture & Flowchart Generation Prompt

Use the following prompt to generate architecture diagrams and flowcharts for your presentation using an AI chat bot (like ChatGPT, Claude, or Gemini).

---

**Prompt:**

I need you to create a high-level architecture diagram and a user flow chart for my web application, **"AI CodeDoc Studio"**.

## Project Context

This is a full-stack application designed to automatically generate documentation for codebases using AI. It analyzes code repositories, generates comprehensive documentation, explanations, and visual flowcharts.

## Tech Stack

### Frontend
- **Next.js 15** (App Router)
- **TypeScript**
- **Tailwind CSS** for styling
- **Shadcn UI** for component library
- **Monaco Editor** for code editing
- **Mermaid.js** for diagram visualization

### Backend
- **FastAPI** (Python) - REST API server
- **MongoDB** with Motor (async driver) - Database
- **Hugging Face Inference API** - AI model for code analysis and flowchart generation
  - Model: `Qwen/Qwen2.5-Coder-32B-Instruct`
- **JWT** for authentication
- **OAuth** integration (Google, GitHub)

### External Services
- **GitHub API** - Repository access
- **Hugging Face** - AI inference
- **MongoDB Atlas** - Cloud database

## System Architecture

### Components

1. **Client (Next.js Frontend)**
   - User interface for code input and documentation display
   - Monaco Editor for code editing
   - Mermaid.js renderer for flowcharts
   - Authentication UI (Google/GitHub OAuth)

2. **API Gateway (FastAPI Backend)**
   - RESTful API endpoints
   - Request validation and rate limiting
   - CORS middleware for cross-origin requests

3. **Core Services**
   - **Auth Service**: JWT-based authentication, OAuth integration
   - **GitHub Service**: Repository fetching, file tree navigation
   - **AI Service**: Code analysis using Hugging Face
   - **Export Service**: Documentation export (Markdown, PDF)

4. **Database Layer (MongoDB)**
   - User profiles and authentication data
   - Generated documentation storage
   - Project metadata and history

5. **AI Engine (Hugging Face)**
   - Code documentation generation
   - Code explanation
   - Flowchart generation (Mermaid syntax)
   - Code optimization suggestions

## Data Flow

### Documentation Generation Flow

1. **Authentication**
   - User logs in via Google/GitHub OAuth
   - Backend validates credentials and issues JWT token
   - Token stored in frontend for subsequent requests

2. **Repository Access**
   - User inputs GitHub repository URL
   - Backend fetches repository structure via GitHub API
   - File tree displayed in frontend

3. **Code Analysis**
   - User selects file(s) to document
   - Frontend sends code to backend `/ai/documentation` endpoint
   - Backend forwards code to Hugging Face Inference API
   - AI generates structured documentation

4. **Flowchart Generation**
   - User requests flowchart for code
   - Backend sends code to `/ai/flowchart` endpoint
   - Hugging Face generates Mermaid diagram syntax
   - Backend post-processes to fix syntax issues
   - Frontend renders flowchart using Mermaid.js

5. **Storage & Export**
   - Generated documentation saved to MongoDB
   - User can export as Markdown or PDF
   - Documentation versioning and history tracking

## Request

Please provide the following Mermaid.js diagrams:

### 1. System Architecture Diagram
A `C4Context` or `graph TD` diagram showing:
- Frontend (Next.js)
- Backend (FastAPI)
- Database (MongoDB)
- External APIs (GitHub, Hugging Face)
- Data flow between components

### 2. Authentication Flow
A `sequenceDiagram` showing:
- User → Frontend → Backend → OAuth Provider → Backend → Frontend
- JWT token generation and storage

### 3. Documentation Generation Flow
A `flowchart TD` showing the complete flow:
- User input → GitHub API → Code retrieval → Hugging Face → Documentation → Storage → Display

### 4. Component Architecture
A `graph LR` showing the internal structure:
- Frontend components (UI, Editor, Renderer)
- Backend services (Auth, GitHub, AI, Export)
- Database collections

---

**Note**: Ensure all Mermaid diagrams use proper syntax with quoted labels for special characters (e.g., `node["Label with /special chars"]`).
