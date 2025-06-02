## Setup & Run Instructions

## Directory Structure & File Roles

Below is an overview of the main files and their responsibilities:

```
Doc_Analyzer_MoEngage/
│
├── main.py                # The main FastAPI app. Defines all API endpoints and connects the agents.
├── content_fetcher.py     # Handles scraping and extracting structured content from documentation URLs using Selenium and BeautifulSoup.
├── analyzer.py            # Contains logic for analyzing documentation structure, style, and quality using Gemini.
├── style_rewriter.py      # Uses Gemini API to automatically rewrite documentation for style guideline improvements.
│
├── requirements.txt       # Python dependencies for the project.
├── .env                   # Environment variables (your Gemini API key). Not committed to version control.
│
├── readme.md              # Setup instructions, API usage, and project overview.
├── thoughtprocess.md      # Detailed notes on the development process, challenges, and solutions.
│
└── EXAMPLES/
    ├── examples_url.txt           # Example URLs for testing the API endpoints.
    ├── example1_analysis.txt      # Saved JSON output for analysis of Example 1.
    ├── example1_rewrite.txt       # Saved JSON output for rewrite of Example 1.
    ├── example2_analysis.txt      # Saved JSON output for analysis of Example 2.
    └── example2_rewrite.txt       # Saved JSON output for rewrite of Example 2.
```

**Summary:**
- `main.py`: Entry point and API routing for the FastAPI app.
- `content_fetcher.py`: Scrapes and structures documentation content from the web.
- `analyzer.py`: Analyzes the content for structure, style, and quality using Gemini.
- `style_rewriter.py`: Rewrites documentation using Gemini, based on style suggestions.
- `requirements.txt`: All required Python packages.
- `.env`: Store your API keys here (never commit this!).
- `readme.md`: How to set up and use the project.
- `thoughtprocess.md`: My full thought process, design choices, and troubleshooting.
- `EXAMPLES/examples_url.txt`: Example URLs for quick testing.
- `EXAMPLES/example1_analysis.txt`: Saved JSON output for analysis of Example 1.
- `EXAMPLES/example1_rewrite.txt`: Saved JSON output for rewrite of Example 1.
- `EXAMPLES/example2_analysis.txt`: Saved JSON output for analysis of Example 2.
- `EXAMPLES/example2_rewrite.txt`: Saved JSON output for rewrite of Example 2.

---


### 1. Clone the Repository
```sh
git clone https://github.com/YashGupta3003/Doc_Analyze_Rewrite.git
cd Doc_Analyze_Rewrite
```

### 2. Create and Activate a Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Set Up API Keys

- **Gemini API Key:**  
  You must have a Google Gemini API key.  
  - Sign up at [Google AI Studio](https://aistudio.google.com/app/apikey) and generate an API key.
  - Create a `.env` file in the project root and add:
    ```
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

### 5. Run the Application
```sh
uvicorn main:app --reload
```
- The API will be available at `http://localhost:8000`.

### 6. API Endpoints

Once the server is running, you can explore and test all API endpoints interactively using **Swagger UI**:

- Open your browser and go to:  
  [http://localhost:8000/docs](http://localhost:8000/docs)

This will show you all available endpoints, their request/response formats, and let you try them out.

---

#### **POST /analyze-documentation**  
**Purpose:** Analyze a documentation page for structure, style, and quality.  
**How to use:**  
- In Swagger UI, click on `/analyze-documentation`, then "Try it out".
- Paste the documentation URL in the `url` field and click "Execute".
- **Request body example:**
  ```json
  { "url": "https://your-doc-url" }
  ```
- **Terminal example:**
  ```sh
  curl -X POST "http://localhost:8000/analyze-documentation" \
    -H "Content-Type: application/json" \
    -d '{"url": "https://your-doc-url"}'
  ```

---

#### **POST /rewrite-style**  
**Purpose:** Automatically rewrite documentation for style guideline improvements, based on the analysis suggestions.  
**How to use:**  
- In Swagger UI, click on `/rewrite-style`, then "Try it out".
- Paste the documentation URL in the `url` field and click "Execute".
- **Request body example:**
  ```json
  { "url": "https://your-doc-url" }
  ```
- **Terminal example:**
  ```sh
  curl -X POST "http://localhost:8000/rewrite-style" \
    -H "Content-Type: application/json" \
    -d '{"url": "https://your-doc-url"}'
  ```

---

#### **POST /fetch-content**  
**Purpose:** Fetches and returns the raw content from a documentation URL (for preview or debugging).  
**How to use:**  
- In Swagger UI, click on `/fetch-content`, then "Try it out".
- Paste the documentation URL in the `url` field and click "Execute".
- **Request body example:**
  ```json
  { "url": "https://your-doc-url" }
  ```
- **Terminal example:**
  ```sh
  curl -X POST "http://localhost:8000/fetch-content" \
    -H "Content-Type: application/json" \
    -d '{"url": "https://your-doc-url"}'
  ```

---

**Notes:**  
- Always provide the full URL of the documentation article you want to analyze or rewrite in the `url` field.
- The endpoints expect a JSON body with a `url` field.
- The project uses Selenium for scraping, so Chrome and ChromeDriver must be installed on your system.(in requirements.txt)
- The Gemini API is used for all AI-powered analysis and rewriting.


---

## Thought Process & Development Notes

For a detailed explanation of how this project was approached, including design decisions, encountered failures, solutions, and key assumptions, please see [`thoughtprocess.md`](./thoughtprocess.md).

This document covers:
- How scraping and content extraction was implemented and improved.
- Challenges with scraping, bot protection, and how Selenium was chosen.
- The reasoning behind LLM selection (Gemini over Hugging Face models).
- Prompt engineering and handling of special content like tables and images.
- The design and evolution of both analysis and rewriting agents.
- Troubleshooting steps and solutions for technical issues.

Reading this file will give you a clear understanding of the project's evolution and the rationale behind each major decision.


---

