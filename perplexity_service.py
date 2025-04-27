"""
Perplexity API Service module for enhanced research capabilities.
This module handles interactions with the Perplexity API to gather high-quality research data.
"""
import os
import json
import requests
from typing import Dict, List, Optional, Union
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Perplexity API configuration
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not PERPLEXITY_API_KEY:
    raise ValueError("Perplexity API key not found. Please check your .env file.")

class PerplexityService:
    """Service for interacting with Perplexity API to conduct advanced research."""
    
    API_URL = "https://api.perplexity.ai/chat/completions"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Perplexity service.
        
        Args:
            api_key (str, optional): The Perplexity API key. If not provided, uses environment variable.
        """
        self.api_key = api_key or PERPLEXITY_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def research_topic(self, 
                      topic: str, 
                      focus_areas: Optional[List[str]] = None,
                      competitor_urls: Optional[List[str]] = None,
                      model: str = "llama-3-sonar-large-32k",
                      max_tokens: int = 2000) -> str:
        """
        Conduct detailed research on a topic using the Perplexity API.
        
        Args:
            topic (str): The main topic to research
            focus_areas (list, optional): Specific areas to focus research on
            competitor_urls (list, optional): List of competitor article URLs to analyze
            model (str): Perplexity model to use
            max_tokens (int): Maximum tokens in response
            
        Returns:
            str: Research findings
        """
        # Construct a comprehensive research prompt
        prompt = self._construct_research_prompt(topic, focus_areas, competitor_urls)
        
        try:
            response = self._make_api_request(prompt, model, max_tokens)
            return response
        except Exception as e:
            print(f"Error conducting research with Perplexity API: {e}")
            return f"Error conducting research: {str(e)}"
    
    def analyze_competitors(self, 
                           urls: List[str], 
                           topic: str,
                           model: str = "llama-3-sonar-large-32k",
                           max_tokens: int = 2000) -> str:
        """
        Analyze competitor content to identify strengths, weaknesses, and gaps.
        
        Args:
            urls (list): URLs of competitor articles to analyze
            topic (str): Main topic for context
            model (str): Perplexity model to use
            max_tokens (int): Maximum tokens in response
            
        Returns:
            str: Analysis of competitor content
        """
        prompt = self._construct_competitor_analysis_prompt(urls, topic)
        
        try:
            response = self._make_api_request(prompt, model, max_tokens)
            return response
        except Exception as e:
            print(f"Error analyzing competitors with Perplexity API: {e}")
            return f"Error analyzing competitors: {str(e)}"
    
    def get_latest_trends(self, 
                         topic: str,
                         model: str = "llama-3-sonar-large-32k",
                         max_tokens: int = 1000) -> str:
        """
        Get the latest trends and developments on a topic.
        
        Args:
            topic (str): The topic to research trends on
            model (str): Perplexity model to use
            max_tokens (int): Maximum tokens in response
            
        Returns:
            str: Latest trends and developments
        """
        prompt = f"""
        Please provide the most recent trends, developments, and research findings in the field of {topic}.
        
        In your response, include:
        1. The latest breakthroughs and advancements in the last 1-2 years
        2. Current research directions and areas of focus
        3. Emerging applications and use cases
        4. Key statistics and market data
        5. Prominent researchers, companies, and organizations leading innovation
        
        Provide specific and factual information with citations where possible.
        """
        
        try:
            response = self._make_api_request(prompt, model, max_tokens)
            return response
        except Exception as e:
            print(f"Error getting latest trends with Perplexity API: {e}")
            return f"Error getting latest trends: {str(e)}"
    
    def generate_seo_keywords(self, 
                             topic: str,
                             model: str = "llama-3-sonar-large-32k",
                             max_tokens: int = 500) -> str:
        """
        Generate SEO keywords and search insights for a topic.
        
        Args:
            topic (str): The topic to generate keywords for
            model (str): Perplexity model to use
            max_tokens (int): Maximum tokens in response
            
        Returns:
            str: SEO keywords and search insights
        """
        prompt = f"""
        Please provide a comprehensive SEO analysis for content about "{topic}".
        
        In your response, include:
        1. Primary keywords with high search volume and relevance
        2. Secondary and long-tail keywords
        3. Current search trends related to this topic
        4. Questions people are asking about this topic
        5. Recommended title formats that would perform well in search
        
        Format your response in a structured way that can be easily parsed for implementation.
        """
        
        try:
            response = self._make_api_request(prompt, model, max_tokens)
            return response
        except Exception as e:
            print(f"Error generating SEO keywords with Perplexity API: {e}")
            return f"Error generating SEO keywords: {str(e)}"
    
    def _construct_research_prompt(self, 
                                  topic: str, 
                                  focus_areas: Optional[List[str]] = None, 
                                  competitor_urls: Optional[List[str]] = None) -> str:
        """
        Construct a comprehensive research prompt.
        
        Args:
            topic (str): The main topic to research
            focus_areas (list, optional): Specific areas to focus research on
            competitor_urls (list, optional): List of competitor article URLs
            
        Returns:
            str: Constructed research prompt
        """
        prompt = f"""
        Please conduct comprehensive research on the topic of "{topic}" for a detailed blog post.
        
        I need factual, up-to-date information that covers all important aspects of this topic.
        """
        
        if focus_areas:
            prompt += "\n\nPlease focus particularly on the following areas:\n"
            for i, area in enumerate(focus_areas, 1):
                prompt += f"{i}. {area}\n"
        
        if competitor_urls:
            prompt += "\n\nThese are competing articles on the same topic. Please identify their strengths, weaknesses, and content gaps:\n"
            for i, url in enumerate(competitor_urls, 1):
                prompt += f"{i}. {url}\n"
        
        prompt += """
        
        In your research, please include:
        1. Key concepts, definitions, and terminology
        2. Historical context and evolution
        3. Current state-of-the-art and latest developments
        4. Practical applications and use cases
        5. Future trends and directions
        6. Important statistics and data points with sources
        7. Authoritative sources and references
        8. Common misconceptions or areas of debate
        
        Please provide in-depth, technically accurate information that would demonstrate expertise (E-E-A-T: Experience, Expertise, Authoritativeness, Trustworthiness).
        """
        
        return prompt
    
    def _construct_competitor_analysis_prompt(self, urls: List[str], topic: str) -> str:
        """
        Construct a prompt for competitor content analysis.
        
        Args:
            urls (list): URLs of competitor articles to analyze
            topic (str): Main topic for context
            
        Returns:
            str: Constructed analysis prompt
        """
        prompt = f"""
        Please analyze the following competing articles about "{topic}":
        
        {chr(10).join([f"{i+1}. {url}" for i, url in enumerate(urls)])}
        
        For each article, please:
        1. Identify the main topics and subtopics covered
        2. Assess strengths (what they do well)
        3. Identify weaknesses and limitations
        4. Note any gaps or missing information
        5. Evaluate the technical depth and accuracy
        6. Analyze the structure and organization
        
        Then provide a summary of:
        1. Common patterns across all articles
        2. Key opportunities to create better content
        3. Unique angles or perspectives that could set new content apart
        4. Topics that should be included in a comprehensive article
        
        Your analysis will help create content that outperforms these competing articles in depth, breadth, and value to readers.
        """
        
        return prompt
    
    def _make_api_request(self, prompt: str, model: str, max_tokens: int) -> str:
        """
        Make a request to the Perplexity API.
        
        Args:
            prompt (str): The prompt to send
            model (str): Perplexity model to use
            max_tokens (int): Maximum tokens in response
            
        Returns:
            str: Response from the API
        """
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a research specialist providing comprehensive, factual, and well-organized information. Focus on accuracy, depth, and clarity in your responses."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens
        }
        
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
