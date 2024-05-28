from bs4 import BeautifulSoup
import re

class HTMLContentExtractor:
    def __init__(self):
        pass

    @staticmethod
    def extract_main_content(html_content):
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'lxml')

        # Remove all script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        # Get the text from the HTML
        text = soup.get_text(separator=' ', strip=True)

        # Remove excessive whitespace
        cleaned_text = re.sub(r'\s+', ' ', text)
    
        return cleaned_text

# Example usage:
# extractor = HTMLContentExtractor()
# main_content = extractor.extract_main_content(html_content)
