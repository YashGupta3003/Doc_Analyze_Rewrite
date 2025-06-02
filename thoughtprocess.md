# Thought Process - AI Documentation Improvement Agent

## Initial Setup and Architecture

Made main with root api endpoint and fetch-content endpoints. 

The content fetcher does the main scraping task for us, uses beautifulsoup to extract data from the article. Did some old fashioned inspect element to figure out where the title and article body lie, went to those header and div classes and focused on those for scraping instead of some logic based scraping (went through 2-3 articles to make sure the classes for scraping remains same).

## Challenge 1: Content Structure Preservation

**Failure faced:** Failed through this approach since through this method we just end up scraping the data as one big para, but we need to analyse everything, the use of lists, para etc. and hence we need to give this scraped text to the llm in the same format as on the website.

**Solution:** It iterates through all heading tags (h1-h6), paragraphs (p), lists (ul, ol), and div elements within the article body. 
- For headings, it adds the heading text with \n. 
- For paragraphs, it adds the text with \n\n. 
- For lists, it adds each list item prefixed with a bullet (•), followed by a \n.

## Challenge 2: Bot Protection

MoEngage doc website had bot protection, requests not able to go through.

**Solution:** bs4 and requests did not work through ai generated headers, switched to selenium webdrivers instead of requests.

## LLM Selection Process

Wanted to use 'microsoft/DialoGPT-medium' llm on hugging face, but not great results hence switched to Gemini, which is free and much better in terms of analysis ability. Llama was not gone ahead with due to slow outputs, since laptop does not have specs and graphic card, for faster computation.

## Prompt Engineering and Analysis

Created prompt based on the assignment pdf, added bias-free language as part of adherence from MS Guidelines. We calculate readability scores, add them to the response from gemini, then parse the text from gemini by splitting into sections.

## API Structure

Created 3 api endpoints:
- One is just root for basic check
- Second is the main one which does the gives the analysis as the response
- Third is the content-fetcher api which returns the fetched content

## Technical Issues and Fixes

Was facing some issue with textstat for our reading scores, regarding module pkg_resources, please install it separately as pip install pkg_resources for textstat (added to requirements.txt file now).

After I was done implementing, went through some examples and saw problems with table parsing and subheadings being considered as paras. Made some changes to read tables and consider adjacent tables as 1, also went ahead stopped counting subheadings as a separate paragraph.

## Image Handling

**Challenge:** Considering there were images in these articles, I could not scrape and pass them to gemini. Was about to go ahead with ocr if I was able to parse, but that would lead to unnecessary complication with analyzation.

**Solution:** Hence went ahead and made tweaks to prompts to make sure it understood that images were provided as examples and it need not gives suggestions like 'give examples or screenshots'.

## Agent 2 Implementation

**Initial Plan:** Wanted to use something else to incorporate the changes instead of Gemini. Used gemma since I had used to previously for a code beautification project. I knew that it would be a good open source llm to use for style guideline changes. Hence went ahead with implementing that.

**Final Decision:** EDIT - Went ahead with GEMINI only because model weights (.safetensors file) were more than 5GB, hence installing that for me and the evaluator would be a big headache.

**Implementation:** Simple implementation - made a prompt with the following context - original text, assessment and guidelines from the styles guidelines section. 

In the main, made a new api endpoint, which first fetches content, then performs analysis, then from the data received from executing analysis, gets the styles guidelines sections and passes it to the rewrite_for_style function in style rewriter file.