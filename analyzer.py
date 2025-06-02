import google.generativeai as genai
from typing import Dict
import re
import textstat

class ContentAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_content(self, content_data: Dict, url: str) -> Dict:
        content_text = content_data.get('content_text', '')
        readability_scores = self.calculate_readability_scores(content_text)
        
        analysis_prompt = self.create_analysis_prompt(content_data, readability_scores)
        
        response = self.model.generate_content(analysis_prompt)
        analysis_text = response.text
        
        structured_analysis = self.parse_analysis_response(analysis_text)
        
        return {
            "success": True,
            "url": url,
            "title": content_data.get('title', 'Unknown'),
            "word_count": content_data.get('word_count', 0),
            "analysis": structured_analysis
        }
    
    def calculate_readability_scores(self, text: str) -> Dict:
        #readability scores
        if not text.strip():
            return {"flesch_kincaid": 0, "gunning_fog": 0}
        
        return {
            "flesch_kincaid": round(textstat.flesch_kincaid_grade(text), 1),
            "gunning_fog": round(textstat.gunning_fog(text), 1)
        }
    
    def create_analysis_prompt(self, content_data: Dict, readability_scores: Dict) -> str:
        #prompt
        content_text = content_data.get('content_text', '')
        title = content_data.get('title', 'Unknown')
        word_count = content_data.get('word_count', 0)
        paragraph_count = content_data.get('paragraph_count', 0)
        heading_count = content_data.get('heading_count', 0)
        list_count = content_data.get('list_count', 0)
        
        prompt = f"""
Analyze this documentation content based on 4 criteria:

CONTENT STRUCTURE:
Title: {title}
Word Count: {word_count}
Paragraphs: {paragraph_count}
Headings: {heading_count}
Lists: {list_count}
Flesch-Kincaid Grade Level: {readability_scores['flesch_kincaid']}
Gunning Fog Index: {readability_scores['gunning_fog']} 

FORMATTING NOTE: 
- Headings are followed by single line breaks (\n)
- Paragraphs are separated by double line breaks (\n\n)  
- List items are prefixed with bullet points (•)

CONTENT:
{content_text}

ANALYSIS CRITERIA:

1. READABILITY FOR MARKETERS:
- Current Flesch-Kincaid score: {readability_scores['flesch_kincaid']} (ideal for marketers: 8-12)
- Current Gunning Fog score: {readability_scores['gunning_fog']} (ideal for marketers: 7-12)
- Assess sentence complexity and technical jargon
- Provide specific examples and actionable suggestions

2. STRUCTURE AND FLOW:
- Evaluate logical flow and organization using the heading structure ({heading_count} headings total)
- Assess paragraph length and readability ({paragraph_count} paragraphs total)
- Check effective use of lists ({list_count} lists total) - look for bullet points (•)
- Consider if headings create clear navigation paths
- Provide specific structural improvements

3. COMPLETENESS AND EXAMPLES:
- Check if content provides enough detail for implementation
- Look for code examples, step-by-step instructions within the structured content
- Evaluate if lists (marked with •) provide clear actionable steps
- Suggest specific types of examples to add

4. STYLE GUIDELINES ADHERENCE:
Focus on these aspects:
- Voice and Tone: Customer-focused, clear, and concise?
- Clarity and Conciseness: Complex sentences or unnecessary jargon?
- Action-oriented Language: Does it guide users effectively?
- Bias-free Communication: Inclusive language, avoids assumptions about user background/expertise?

Format response as:
## READABILITY FOR MARKETERS
Assessment: [assessment with readability scores interpretation]
Suggestions:
1. [specific suggestion]
2. [specific suggestion]

## STRUCTURE AND FLOW
Assessment: [assessment]
Suggestions:
1. [specific suggestion]
2. [specific suggestion]

## COMPLETENESS AND EXAMPLES
Assessment: [assessment]
Suggestions:
1. [specific suggestion]
2. [specific suggestion]

## STYLE GUIDELINES
Assessment: [assessment]
Suggestions:
1. [specific suggestion]
2. [specific suggestion]
3. [specific suggestion]
4. [specific suggestion]

Note: 1) Make sure to not give suggestions like -  "Provide a screenshot of the \"Contact Support\" button on the login page." or Include screenshots/visual examples." ,since assume that image examples are given after each paragraph, and it is not provided in the content text given to you since I cannot pass images to Gemini.
2) Assessments should be clear and actionable, not just general statements, and can be comprehensive. Mention the readability scores in the assessment for readability.
3) If you cannot analyze a section, just say "Analysis completed" metion something generic chnages that can be made.
"""
        return prompt
    
    def parse_analysis_response(self, analysis_text: str) -> Dict:
        # since gemini follows our format well, we can just split by sections
        sections = analysis_text.split('##')
        
        result = {
            "readability": {"assessment": "Analysis completed", "suggestions": []},
            "structure": {"assessment": "Analysis completed", "suggestions": []},
            "completeness": {"assessment": "Analysis completed", "suggestions": []},
            "style_guidelines": {"assessment": "Analysis completed", "suggestions": []}
        }
        
        for section in sections:
            section = section.strip()
            if 'READABILITY' in section.upper():
                result["readability"] = self.simple_parse(section)
            elif 'STRUCTURE' in section.upper():
                result["structure"] = self.simple_parse(section)
            elif 'COMPLETENESS' in section.upper():
                result["completeness"] = self.simple_parse(section)
            elif 'STYLE' in section.upper():
                result["style_guidelines"] = self.simple_parse(section)
        
        return result
    
    def simple_parse(self, section_text: str) -> Dict:
        """Simple parsing - just extract assessment and suggestions"""
        lines = section_text.split('\n')
        assessment = ""
        suggestions = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('Assessment:'):
                assessment = line.replace('Assessment:', '').strip()
            elif line.startswith(('1.', '2.', '3.')):
                suggestions.append(line[2:].strip())
        
        return {
            "assessment": assessment if assessment else "Analysis completed",
            "suggestions": suggestions
        }