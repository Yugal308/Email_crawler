# Copy the entire EmailCrawler class from the original script.py
# (from the class definition to the get_results method) 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd
import csv

class EmailCrawler:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')  
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.visited_urls = set()
        self.emails = set()
        self.phone_numbers = set()
        
        # Improved regex patterns
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        # Enhanced phone pattern to catch more formats including Australian numbers
        self.phone_patterns = [
            r'(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # Standard US/CAN
            r'(?:\+\d{1,3}[-.\s]?)?\d{4}[-.\s]?\d{3}[-.\s]?\d{3}',  # Alternative format
            r'(?:\+\d{1,3}[-.\s]?)?\d{3,4}[-.\s]?\d{3}[-.\s]?\d{3}',  # Another common format
            r'(?:\+\d{1,3}[-.\s]?)?\d{4}[-.\s]?\d{4}',  # Shorter format
            r'(?:\+\d{1,3}[-.\s]?)?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}[-.\s]?\d{2}',  # European style
            r'\b\d{4}[-.\s]?\d{3}[-.\s]?\d{3}\b',  # Australian mobile
            r'\b\d{10}\b',  # Plain 10 digits
        ]
        
        # Alternative patterns for specific formats with "t:" or "tel:" prefixes
        self.special_phone_pattern = r'(?:t|tel|phone|p|mob|mobile|m|f|fax)(?::|;|\.|\s)+\s*(?:\+\d{1,3}[-.\s]?)?\d[\d\s\-\.]{7,15}\d'

    def is_valid_url(self, url):
        """Check if the URL is valid and belongs to the same domain."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def extract_emails_and_phones(self, text):
        """Extract emails and phone numbers from text."""
        emails = re.findall(self.email_pattern, text)
        
        # Extract phone numbers using multiple patterns
        phones = []
        for pattern in self.phone_patterns:
            found = re.findall(pattern, text)
            phones.extend(found)
        
        # Look for special format phones (with prefixes)
        special_phones = re.findall(self.special_phone_pattern, text, re.IGNORECASE)
        for phone in special_phones:
            # Extract just the number part after the prefix
            number_part = re.sub(r'(?:t|tel|phone|p|mob|mobile|m|f|fax)(?::|;|\.|\s)+\s*', '', phone, flags=re.IGNORECASE)
            phones.append(number_part.strip())
        
        # Normalize phone numbers (remove extra spaces, etc.)
        normalized_phones = []
        for phone in phones:
            # Clean up the phone number
            cleaned = re.sub(r'[^\d+]', '', phone)
            if len(cleaned) >= 8:  # Minimum length for a valid phone number
                normalized_phones.append(phone.strip())
        
        return emails, list(set(normalized_phones))

    def crawl_page(self, url, base_domain):
        """Crawl a single page and extract emails and phone numbers."""
        if url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        self.logger.info(f"Crawling: {url}")

        try:
            self.driver.get(url)
            time.sleep(2)  # Wait for JavaScript to load

            # Get page source and parse with BeautifulSoup
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Extract text content
            text_content = soup.get_text()
            
            # Find emails and phone numbers
            emails, phones = self.extract_emails_and_phones(text_content)
            self.emails.update(emails)
            self.phone_numbers.update(phones)
            
            # Also look for emails and phones in HTML attributes (like href="tel:..." or href="mailto:...")
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Check for mailto: links
                if href.startswith('mailto:'):
                    email = href.replace('mailto:', '').split('?')[0].strip()
                    if '@' in email and '.' in email.split('@')[1]:
                        self.emails.add(email)
                
                # Check for tel: links
                if href.startswith('tel:'):
                    phone = href.replace('tel:', '').strip()
                    if phone:
                        self.phone_numbers.add(phone)

            # Find all links on the page
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                full_url = urljoin(url, href)
                
                # Only follow links from the same domain
                if self.is_valid_url(full_url) and base_domain in full_url:
                    self.crawl_page(full_url, base_domain)

        except Exception as e:
            self.logger.error(f"Error crawling {url}: {str(e)}")

    def crawl_website(self, start_url):
        """Start crawling from the given URL."""
        try:
            # Make sure URL starts with http:// or https://
            if not start_url.startswith(('http://', 'https://')):
                start_url = 'https://' + start_url
                
            base_domain = urlparse(start_url).netloc
            self.crawl_page(start_url, base_domain)
        finally:
            self.driver.quit()

    def get_results(self):
        """Return the collected emails and phone numbers."""
        return {
            'emails': list(self.emails),
            'phone_numbers': list(self.phone_numbers)
        }

