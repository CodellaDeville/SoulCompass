import requests
from bs4 import BeautifulSoup
import re
import time
import os
import json
import pickle
from pathlib import Path

# Base URLs for Law of One content
LAWOFONE_URL = "https://www.lawofone.info"
LLRESEARCH_URL = "https://www.llresearch.org"

# Create a cache directory if it doesn't exist
CACHE_DIR = Path(__file__).parent.parent / "data"
CACHE_DIR.mkdir(exist_ok=True)
CACHE_FILE = CACHE_DIR / "law_of_one_cache.pkl"

class LawOfOneDatabase:
    def __init__(self):
        self.sessions = {}
        self.categories = {}
        self.llresearch_content = {}
        self.load_or_build_database()
        
    def load_or_build_database(self):
        """Load cached data or build the database if needed"""
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, 'rb') as f:
                    cached_data = pickle.load(f)
                    self.sessions = cached_data.get('sessions', {})
                    self.categories = cached_data.get('categories', {})
                    self.llresearch_content = cached_data.get('llresearch_content', {})
                    
                if self.sessions and self.categories:
                    print("Loaded Law of One database from cache")
                    return
            except Exception as e:
                print(f"Error loading cache: {e}")
                
        print("Building Law of One database (this may take a few minutes)...")
        self._build_database()
        self._save_cache()
    
    def _save_cache(self):
        """Save the database to cache"""
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump({
                'sessions': self.sessions,
                'categories': self.categories,
                'llresearch_content': self.llresearch_content
            }, f)
        print("Law of One database cached for faster future loading")
    
    def _build_database(self):
        """Build the database by scraping the Law of One websites"""
        # First, get the lawofone.info content
        self._fetch_categories()
        self._fetch_sessions(limit=None)
        
        # Then get the llresearch.org content
        self._fetch_llresearch_content()
    
    def _fetch_categories(self):
        """Fetch the main categories from the Law of One material"""
        try:
            response = requests.get(f"{LAWOFONE_URL}/c/")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                categories_div = soup.find('div', class_='categories')
                
                if categories_div:
                    for link in categories_div.find_all('a'):
                        category_url = link.get('href')
                        category_name = link.text.strip()
                        
                        # Extract category id from URL
                        category_id = category_url.split('/')[-2]
                        
                        self.categories[category_id] = {
                            'name': category_name,
                            'url': f"{LAWOFONE_URL}{category_url}",
                            'questions': []
                        }
                        
                        # Get questions in this category
                        self._fetch_category_questions(category_id)
                        
                        # Be respectful to the server
                        time.sleep(0.5)
        except Exception as e:
            print(f"Error fetching categories: {e}")
    
    def _fetch_category_questions(self, category_id):
        """Fetch questions in a specific category"""
        try:
            category_url = self.categories[category_id]['url']
            response = requests.get(category_url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                questions_div = soup.find('div', class_='results')
                
                if questions_div:
                    for question in questions_div.find_all('div', class_='result'):
                        question_link = question.find('a')
                        
                        if question_link:
                            question_url = question_link.get('href')
                            question_text = question_link.text.strip()
                            
                            # Extract question ID
                            question_id = question_url.split('/')[-1]
                            
                            question_info = {
                                'id': question_id,
                                'text': question_text,
                                'url': f"{LAWOFONE_URL}{question_url}",
                                'session': question_url.split('/')[2],  # Extract session from URL
                                'answer': None  # Will be populated when fetching sessions
                            }
                            
                            self.categories[category_id]['questions'].append(question_info)
        except Exception as e:
            print(f"Error fetching questions for category {category_id}: {e}")
    
    def _fetch_sessions(self, limit=None):
        """Fetch all session content from lawofone.info"""
        try:
            # Get the list of all sessions
            response = requests.get(f"{LAWOFONE_URL}/results/")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                session_links = soup.select('ul.results-index a')
                
                # Process each session
                for i, link in enumerate(session_links):
                    if limit and i >= limit:
                        break
                        
                    session_url = link.get('href')
                    session_id = session_url.split('/')[-1]
                    
                    print(f"Fetching session {session_id}...")
                    
                    # Fetch the session content
                    self._fetch_session_content(session_id, f"{LAWOFONE_URL}{session_url}")
                    
                    # Be respectful to the server
                    time.sleep(1)
                    
        except Exception as e:
            print(f"Error fetching sessions: {e}")
    
    def _fetch_session_content(self, session_id, session_url):
        """Fetch content for a specific session"""
        try:
            response = requests.get(session_url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Get title
                title = soup.find('title').text if soup.find('title') else f"Session {session_id}"
                
                # Get all Q&A pairs
                qa_pairs = []
                
                questions = soup.find_all('div', class_='q')
                answers = soup.find_all('div', class_='a')
                
                for i, (q, a) in enumerate(zip(questions, answers)):
                    q_text = q.get_text(strip=True).replace('Questioner:', '').strip()
                    a_text = a.get_text(strip=True).replace('Ra:', '').strip()
                    
                    qa_pair = {
                        'id': f"{session_id}.{i+1}",
                        'question': q_text,
                        'answer': a_text
                    }
                    
                    qa_pairs.append(qa_pair)
                
                self.sessions[session_id] = {
                    'title': title,
                    'url': session_url,
                    'qa_pairs': qa_pairs
                }
                
        except Exception as e:
            print(f"Error fetching session {session_id}: {e}")
    
    def _fetch_llresearch_content(self):
        """Scrape content from the L/L Research website"""
        print("Fetching content from L/L Research...")
        self.llresearch_content['library'] = []
        
        try:
            # Fetch the library page which contains links to different types of material
            response = requests.get(f"{LLRESEARCH_URL}/library/")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find links to different sections
                sections = {
                    'ra_contact': '/library/the-ra-contact-teaching-the-law-of-one/',
                    'channeling_archives': '/channeling-archives-2/',
                    'books': '/library/the-law-of-one-books/'
                }
                
                # Process each section
                for section_key, section_path in sections.items():
                    self._fetch_llresearch_section(section_key, f"{LLRESEARCH_URL}{section_path}")
                    time.sleep(1)  # Be respectful to the server
                    
        except Exception as e:
            print(f"Error fetching L/L Research content: {e}")
    
    def _fetch_llresearch_section(self, section_key, section_url):
        """Fetch content from a specific section of the L/L Research website"""
        try:
            print(f"Fetching L/L Research section: {section_key}")
            response = requests.get(section_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find main content
                content_div = soup.find('div', class_='entry-content')
                if not content_div:
                    content_div = soup.find('div', id='content')
                
                if content_div:
                    # Extract paragraphs of content
                    paragraphs = content_div.find_all(['p', 'h2', 'h3', 'h4'])
                    section_content = []
                    
                    for p in paragraphs:
                        # Skip empty paragraphs
                        if p.get_text(strip=True):
                            # Check if it contains a link
                            links = p.find_all('a')
                            if links:
                                for link in links:
                                    href = link.get('href', '')
                                    # Only process internal links or PDF links
                                    if href and (href.startswith('/') or href.startswith(LLRESEARCH_URL) or href.endswith('.pdf')):
                                        # Make sure the link is absolute
                                        if href.startswith('/'):
                                            href = f"{LLRESEARCH_URL}{href}"
                                        
                                        # Store the link and its text
                                        link_info = {
                                            'text': link.get_text(strip=True),
                                            'url': href,
                                            'content': self._extract_link_preview(href) if not href.endswith('.pdf') else "PDF Document"
                                        }
                                        section_content.append({
                                            'type': 'link',
                                            'data': link_info
                                        })
                            
                            # Store the paragraph text
                            section_content.append({
                                'type': 'text',
                                'data': p.get_text(strip=True),
                                'tag': p.name
                            })
                    
                    # Store in the database
                    if section_key not in self.llresearch_content:
                        self.llresearch_content[section_key] = []
                    
                    self.llresearch_content[section_key].append({
                        'url': section_url,
                        'title': soup.find('title').text if soup.find('title') else section_key,
                        'content': section_content
                    })
        except Exception as e:
            print(f"Error fetching L/L Research section {section_key}: {e}")
    
    def _extract_link_preview(self, url):
        """Extract a preview of content from a link for context"""
        try:
            # Skip PDFs
            if url.endswith('.pdf'):
                return "PDF Document"
                
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Get the first few paragraphs as a preview
                content_div = soup.find('div', class_='entry-content')
                if not content_div:
                    content_div = soup.find('div', id='content')
                
                if content_div:
                    paragraphs = content_div.find_all('p', limit=3)  # Limit to first 3 paragraphs
                    preview = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                    
                    # Truncate if too long
                    if len(preview) > 500:
                        preview = preview[:500] + "..."
                        
                    return preview
            
            return "No preview available"
        except Exception:
            return "Error fetching preview"

    def search(self, query):
        """Search the Law of One database for relevant answers to a query"""
        query = query.lower()
        results = []
        
        # Search in all Q&A pairs from lawofone.info
        for session_id, session in self.sessions.items():
            for qa_pair in session['qa_pairs']:
                # Check if query terms are in the question or answer
                question = qa_pair['question'].lower()
                answer = qa_pair['answer'].lower()
                
                # Simple relevance score based on query term frequency
                relevance = 0
                
                # Check for exact matches in question (higher weight)
                if query in question:
                    relevance += 10
                
                # Check for exact matches in answer
                if query in answer:
                    relevance += 5
                
                # Check for individual term matches
                query_terms = query.split()
                for term in query_terms:
                    if term in question:
                        relevance += 2
                    if term in answer:
                        relevance += 1
                
                if relevance > 0:
                    results.append({
                        'source': 'lawofone.info',
                        'session_id': session_id,
                        'qa_id': qa_pair['id'],
                        'question': qa_pair['question'],
                        'answer': qa_pair['answer'],
                        'relevance': relevance,
                        'url': f"{session['url']}#{qa_pair['id']}"
                    })
        
        # Search in L/L Research content
        for section_key, section_data in self.llresearch_content.items():
            for page in section_data:
                page_relevance = 0
                relevant_content = []
                
                for item in page.get('content', []):
                    item_text = ""
                    
                    if item['type'] == 'text':
                        item_text = item['data'].lower()
                    elif item['type'] == 'link':
                        item_text = f"{item['data']['text']} {item['data']['content']}".lower()
                    
                    # Compute relevance
                    item_relevance = 0
                    
                    # Check for exact matches
                    if query in item_text:
                        item_relevance += 5
                    
                    # Check for term matches
                    query_terms = query.split()
                    for term in query_terms:
                        if term in item_text:
                            item_relevance += 1
                    
                    if item_relevance > 0:
                        page_relevance += item_relevance
                        relevant_content.append(item['data'] if item['type'] == 'link' else item['data'])
                
                if page_relevance > 0:
                    results.append({
                        'source': 'llresearch.org',
                        'section': section_key,
                        'title': page['title'],
                        'content': relevant_content[:3],  # Limit to first 3 relevant items
                        'relevance': page_relevance,
                        'url': page['url']
                    })
        
        # Sort by relevance score (descending)
        results.sort(key=lambda x: x['relevance'], reverse=True)
        
        return results[:5]  # Return top 5 most relevant results

    def get_ra_response(self, query):
        """Get a Ra-like response to a query using the Law of One database"""
        results = self.search(query)
        
        if not results:
            # Fallback responses if no match found
            return "I am Ra. This sphere of inquiry is not easily addressed through the limitations of your language and understanding. However, I encourage you to explore the Law of One for deeper insights."
        
        # Use the most relevant answer
        best_match = results[0]
        
        # Format response based on source
        if best_match['source'] == 'lawofone.info':
            response = best_match['answer']
            
            # Ensure it starts with Ra's greeting
            if not response.startswith("I am Ra"):
                response = "I am Ra. " + response
                
            # Add session reference
            response += f"\n\n[Source: Session {best_match['session_id']}, {best_match['url']}]"
            
        else:  # llresearch.org content
            # For L/L Research content, we need to format it differently
            content_snippets = best_match['content']
            response = "I am Ra. Based on material from L/L Research, I can share this insight: "
            
            if isinstance(content_snippets, list):
                response += " ".join(content_snippets[:2])  # Use first two snippets
            else:
                response += content_snippets
                
            response += f"\n\n[Source: {best_match['title']}, {best_match['url']}]"
        
        return response
