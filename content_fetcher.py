from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from typing import Dict

class ContentFetcher:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def fetch_content(self, url: str) -> Dict:
        try:
            self.driver.get(url)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            content_data = self._extract_content(soup)
            return {
                "success": True,
                "url": url,
                "data": content_data
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _extract_content(self, soup: BeautifulSoup) -> Dict:
        title = soup.title.string.strip() if soup.title else ""

        article = soup.select_one('.article_body.markdown') or soup.select_one('.article__body.markdown')
        if not article:
            return {"title": title, "header": "", "content_text": "", "word_count": 0, "paragraph_count": 0, "list_count": 0, "heading_count": 0}

        content = []
        paragraph_count = 0
        list_count = 0
        heading_count = 0

        last_was_table = False

        for tag in article.find_all(['p', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table']):
            if tag.name.startswith('h'):
                heading_count += 1
                content.append(f"\n{tag.get_text(strip=True)}\n")
                last_was_table = False
            elif tag.name == 'p':
                text = tag.get_text(strip=True)
                if text:
                    paragraph_count += 1
                    content.append(f"{text}\n")
                last_was_table = False
            elif tag.name in ['ul', 'ol']:
                list_count += 1
                for li in tag.find_all('li'):
                    content.append(f"• {li.get_text(strip=True)}")
                content.append("")
                last_was_table = False
            elif tag.name == 'table':
                if not last_was_table:
                    content.append("")  # space before first table
                for row in tag.find_all('tr'):
                    cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                    content.append(" | ".join(cells))
                last_was_table = True
            else:
                last_was_table = False

        full_text = "\n".join(content).strip()
        word_count = len(full_text.split())

        return {
            "title": title,
            "header": "",
            "content_text": full_text,
            "word_count": word_count,
            "paragraph_count": paragraph_count,
            "list_count": list_count,
            "heading_count": heading_count
        }


    def close(self):
        if self.driver:
            self.driver.quit()
