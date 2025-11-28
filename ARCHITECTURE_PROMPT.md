# Architecture & Flowchart Generation Prompt

Use the following prompt to generate architecture diagrams and flowcharts for your presentation using an AI chat bot (like ChatGPT, Claude, or Gemini).

---

**Prompt:**

I need you to create a high-level architecture diagram and a user flow chart for my web application, "AI CodeDoc Studio".

**Project Context:**
This is a full-stack application designed to automatically generate documentation for codebases using AI.

**Tech Stack:**
-   **Frontend**: Next.js 16, Tailwind CSS, Shadcn UI.
-   **Backend**: FastAPI (Python), MongoDB (Motor), Google Generative AI (Gemini).
-   **Key Libraries**: Mermaid.js (frontend visualization), Monaco Editor.

**System Architecture:**
1.  **Client**: The Next.js frontend serves as the user interface. It handles user inputs (repo URLs), displays code, and renders markdown/mermaid diagrams.
2.  **API Gateway**: FastAPI serves as the backend API, handling REST requests from the client.
3.  **Services**:
    -   **Auth Service**: Handles user login/signup (JWT).
    -   **GitHub Service**: Connects to GitHub API to fetch repository structures and file contents.
    -   **AI Engine**: Sends code chunks to Google Gemini API to generate explanations and Mermaid graph syntax.
    -   **Database**: MongoDB stores user profiles and generated documentation projects.

**Data Flow:**
1.  User logs in (Frontend -> Auth Service -> DB).
2.  User inputs a GitHub URL.
3.  Backend fetches repo data (Backend -> GitHub API).
4.  User selects a file to document.
5.  Backend sends file content to Gemini (Backend -> Gemini API).
6.  Gemini returns documentation and Mermaid syntax.
7.  Backend saves result to MongoDB and sends it to Frontend.
8.  Frontend renders the documentation and the flowchart.

**Request:**
1.  **Architecture Diagram**: Please provide a Mermaid.js `graph TD` or `C4Context` diagram code that visualizes this system architecture, showing the Frontend, Backend, Database, and External APIs (GitHub, Gemini).
2.  **User Flow Chart**: Please provide a Mermaid.js `sequenceDiagram` or `flowchart TD` showing the "Generate Documentation" flow described in the Data Flow section.

---
