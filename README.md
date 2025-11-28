# AI CodeDoc Studio

## Overview

**AI CodeDoc Studio** is a powerful full-stack web application designed to revolutionize how developers document and understand code. By leveraging advanced AI models (Hugging Face's Qwen2.5-Coder and Google's Gemini), it automatically generates comprehensive documentation, visual flowcharts, code explanations, and unit tests.

The application features a modern, responsive frontend built with **Next.js 16** and a robust **FastAPI** backend, offering a seamless experience for developers to analyze their codebases.

## Key Features

-   **🤖 AI-Powered Documentation**: Automatically generates detailed documentation for code files, including summaries, parameter descriptions, and usage examples.
-   **📊 Flowchart Generation**: Visualizes code logic by generating Mermaid.js flowcharts, making complex algorithms easier to understand.
-   **📝 Code Explanation**: Provides line-by-line or block-level explanations of code functionality.
-   **🧪 Unit Test Generation**: Automatically creates unit tests for your code to ensure reliability.
-   **⚡ Code Optimization**: Suggests performance improvements and refactoring opportunities.
-   **🔗 GitHub Integration**: Connect directly to your GitHub account to browse repositories and analyze files without manual copy-pasting.
-   **✏️ Real-time Editing**: Features a rich Monaco Editor for viewing code and editing generated documentation.
-   **🔐 Secure Authentication**: JWT-based authentication system with MongoDB storage.

## Technology Stack

### Frontend
-   **Framework**: Next.js 16 (App Router)
-   **Library**: React 19
-   **Styling**: Tailwind CSS v4, Shadcn UI (Radix Primitives)
-   **Editor**: Monaco Editor (VS Code-like experience)
-   **Visualization**: Mermaid.js
-   **State/Data**: React Hook Form, Zod, Axios
-   **Icons**: Lucide React

### Backend
-   **Framework**: FastAPI (Python)
-   **Database**: MongoDB (via Motor async driver)
-   **AI Engine**:
    -   **Primary**: Hugging Face Inference API (Qwen/Qwen2.5-Coder-32B-Instruct)
    -   **Fallback**: Google Generative AI (Gemini 2.0 Flash)
-   **Authentication**: Python-Jose (JWT), Passlib (Bcrypt)
-   **HTTP Client**: Httpx

## Setup & Installation

### Prerequisites
-   **Node.js** (v18+)
-   **Python** (v3.10+)
-   **MongoDB** instance (Local or Atlas)
-   **API Keys**:
    -   Hugging Face API Key
    -   Google Gemini API Key (Optional, for fallback)

### Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Create and activate a virtual environment:
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure Environment Variables:
    Create a `.env` file in the `backend` directory with the following:
    ```env
    MONGODB_URL=mongodb://localhost:27017
    DB_NAME=aicodedoc
    SECRET_KEY=your_secret_key_here
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    HUGGINGFACE_API_KEY=your_hf_key
    GEMINI_API_KEY=your_gemini_key
    ```

5.  Run the server:
    ```bash
    uvicorn app.server:app --reload --port 8000
    ```

### Frontend Setup

1.  Navigate to the root directory:
    ```bash
    cd ..
    ```

2.  Install dependencies:
    ```bash
    pnpm install
    # or npm install
    ```

3.  Run the development server:
    ```bash
    pnpm dev
    # or npm run dev
    ```

4.  Open [http://localhost:3000](http://localhost:3000) in your browser.

## API Documentation

The backend exposes the following main endpoints:

### AI Services (`/ai`)
-   `POST /ai/documentation`: Generate documentation for code.
-   `POST /ai/flowchart`: Generate Mermaid flowchart.
-   `POST /ai/explain`: Explain code line-by-line.
-   `POST /ai/tests`: Generate unit tests.
-   `POST /ai/optimize`: Suggest code optimizations.

### GitHub (`/github`)
-   `GET /github/repos`: List user's repositories.
-   `GET /github/contents`: List repository contents.
-   `GET /github/file`: Get file content.

### Authentication (`/auth`)
-   `POST /auth/register`: Register a new user.
-   `POST /auth/login`: Login and get JWT token.

## Architecture Overview

The application follows a decoupled client-server architecture:

1.  **Client**: The Next.js frontend handles the UI, state management, and communicates with the backend via REST APIs. It uses Monaco Editor for code interaction and Mermaid.js for rendering diagrams.
2.  **API Gateway**: The FastAPI backend serves as the gateway, handling authentication, request validation, and routing.
3.  **AI Service Layer**: This layer processes code using the Hugging Face Inference API. It includes fallback logic to Google's Gemini if the primary service fails.
4.  **Integration Layer**: Handles communication with external services like GitHub for repository access.
5.  **Data Layer**: MongoDB stores user profiles, generated documentation, and project history.
