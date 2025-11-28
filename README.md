# AI CodeDoc Studio

## Overview

AI CodeDoc Studio is a web application designed to generate documentation for codebases using AI. It features a modern Next.js frontend and a robust FastAPI backend powered by Google's Generative AI (Gemini).

## Technology Stack

### Frontend
-   **Framework**: Next.js 16 (React 19)
-   **Styling**: Tailwind CSS v4, Shadcn UI (Radix Primitives)
-   **State Management & Utilities**: React Hook Form, Zod, Axios
-   **Visualization**: Mermaid.js (for diagrams), Monaco Editor (for code viewing)
-   **Icons**: Lucide React

### Backend
-   **Framework**: FastAPI
-   **Database**: MongoDB (via Motor async driver)
-   **AI Engine**: Google Generative AI (Gemini)
-   **Authentication**: Google Auth with JWT
-   **External Integrations**: GitHub API (Coming Soon)

## Architecture Overview
The application follows a decoupled client-server architecture:

1.  **Frontend (Next.js)**: Handles user interface, authentication flows, and displays generated documentation. It communicates with the backend via RESTful APIs.
2.  **Backend (FastAPI)**:
    -   **Auth Service**: Manages user registration and login using JWT.
    -   **GitHub Service**: Fetches repository content and metadata.
    -   **AI Service**: Processes code using Gemini to generate documentation, flowcharts, and summaries.
    -   **Export Service**: Handles exporting documentation to various formats.
3.  **Database (MongoDB)**: Stores user data, project metadata, and cached documentation.

## Key Features
-   **AI-Powered Documentation**: Automatically generates comprehensive documentation for code files.
-   **Flowchart Generation**: Visualizes code logic using Mermaid diagrams.
-   **GitHub Integration**: (Coming Soon) Connect your repositories directly.
-   **Real-time Editing**: Edit generated documentation using a rich text editor.

## Setup & Installation

### Prerequisites
-   Node.js (v18+)
-   Python (v3.10+)
-   MongoDB instance
-   Google Gemini API Key

### Backend Setup

#### Linux/macOS
1.  Navigate to the project root:
    ```bash
    cd /home/rht/Pro/ai-code-doc
    ```
2.  Activate virtual environment and install dependencies:
    ```bash
    source backend/.venv/bin/activate
    pip install -r backend/requirements.txt
    ```
3.  Run the server:
    ```bash
    cd backend
    uvicorn app.server:app --host 0.0.0.0 --port 8000
    ```

#### Windows
1.  Navigate to the project root:
    ```bash
    cd \path\to\ai-code-doc
    ```
2.  Activate virtual environment and install dependencies:
    ```bash
    backend\.venv\Scripts\activate
    pip install -r backend\requirements.txt
    ```
3.  Run the server:
    ```bash
    cd backend
    uvicorn app.server:app --host 0.0.0.0 --port 8000
    ```

### Frontend Setup
1.  Navigate to the root directory:
    ```bash
    cd ..
    ```
2.  Install dependencies:
    ```bash
    pnpm install
    ```
3.  Run the development server:
    ```bash
    pnpm dev
    ```
