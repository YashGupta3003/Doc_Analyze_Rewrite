import os
from typing import List
import google.generativeai as genai


class StyleRewriter:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def rewrite_for_style(
        self,
        original_content: str,
        style_suggestions: List[str],
        assessment: str = ""
    ) -> str:
        
        #to address style guideline suggestions using Gemini API.
        suggestions_text = "\n".join(f"- {s}" for s in style_suggestions)
        prompt = f"""
You are an expert technical writer. Your task is to revise the following documentation content to address the provided style guideline suggestions. 
- Only change the writing style, tone, clarity, conciseness, and bias-free language as per the suggestions.
- Do NOT change the technical meaning, structure, headings, lists, or tables.
- Preserve all formatting, subheadings, and tables as in the original.
- Output the revised documentation in the same format (with headings, paragraphs, lists, and tables).

STYLE GUIDELINE ASSESSMENT:
{assessment}

STYLE GUIDELINE SUGGESTIONS:
{suggestions_text}

ORIGINAL CONTENT:
{original_content}

REVISED CONTENT:
"""
        response = self.model.generate_content(prompt)
        if hasattr(response, "text"):
            return response.text.strip()
        return "Error: did not return expected text."