import requests
from bs4 import BeautifulSoup
import re
import time
import os
import json
import pickle
from pathlib import Path

# Base URL for Law of One content
BASE_URL = "https://www.lawofone.info"

# Create a cache directory if it doesn't exist
CACHE_DIR = Path(__file__).parent.parent / "data"
CACHE_DIR.mkdir(exist_ok=True)
CACHE_FILE = CACHE_DIR / "law_of_one_cache.pkl"

class LawOfOneDatabase:
    def __init__(self):
        self.sessions = {}
        self.categories = {}
        self.load_or_build_database()
        
    def load_or_build_database(self):
        """Load cached data or build the database if needed"""
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, 'rb') as f:
                    cached_data = pickle.load(f)
                    self.sessions = cached_data.get('sessions', {})
                    self.categories = cached_data.get('categories', {})
                    
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
                'categories': self.categories
            }, f)
        print("Law of One database cached for faster future loading")
    
    def _build_database(self):
        """Build the database by scraping the Law of One website"""
        # First, get the category pages
        self._fetch_categories()
        
        # Then get all session content (limited to first 20 sessions for testing)
        self._fetch_sessions(limit=None)
    
    def _fetch_categories(self):
        """Fetch the main categories from the Law of One material"""
        try:
            response = requests.get(f"{BASE_URL}/c/")
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
                            'url': f"{BASE_URL}{category_url}",
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
                                'url': f"{BASE_URL}{question_url}",
                                'session': question_url.split('/')[2],  # Extract session from URL
                                'answer': None  # Will be populated when fetching sessions
                            }
                            
                            self.categories[category_id]['questions'].append(question_info)
        except Exception as e:
            print(f"Error fetching questions for category {category_id}: {e}")
    
    def _fetch_sessions(self, limit=None):
        """Fetch all session content"""
        try:
            # Get the list of all sessions
            response = requests.get(f"{BASE_URL}/results/")
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
                    self._fetch_session_content(session_id, f"{BASE_URL}{session_url}")
                    
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

    def search(self, query):
        """Search the Law of One database for relevant answers to a query"""
        query = query.lower()
        results = []
        
        # Search in all Q&A pairs
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
                        'session_id': session_id,
                        'qa_id': qa_pair['id'],
                        'question': qa_pair['question'],
                        'answer': qa_pair['answer'],
                        'relevance': relevance,
                        'url': f"{session['url']}#{qa_pair['id']}"
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
        response = best_match['answer']
        
        # Ensure it starts with Ra's greeting
        if not response.startswith("I am Ra"):
            response = "I am Ra. " + response
            
        # Add session reference
        session_info = f"\n\n[From Session {best_match['session_id']}]"
        
        return response + session_info
