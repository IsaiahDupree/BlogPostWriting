"""
Configuration module for the NLP Blog Post Generator application.
Responsible for loading environment variables and configuring the application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY or not OPENAI_API_KEY.startswith("sk-"):
    raise ValueError("Invalid or missing OpenAI API key. Please check your .env file.")

# Perplexity API configuration
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not PERPLEXITY_API_KEY:
    print("Warning: Perplexity API key not found. Some advanced research features may not be available.")

# Model configuration
DEFAULT_MODEL = "gpt-3.5-turbo"
TEXT_MODEL = "gpt-3.5-turbo"
RESEARCH_MODEL = "gpt-3.5-turbo"
OUTLINE_MODEL = "gpt-3.5-turbo"

# Temperature settings for different content types
RESEARCH_TEMP = 0.2  # Lower temperature for factual research
OUTLINE_TEMP = 0.5  # Moderate temperature for outlining
CONTENT_TEMP = 0.7  # Higher temperature for creative content generation

# Default prompts
DEFAULT_SYSTEM_PROMPT = """You are an expert blog writer specializing in AI, Machine Learning, and Natural Language 
Processing (NLP). You create comprehensive, educational content that is SEO-optimized, technically accurate, and 
engaging. Your writing should meet E-E-A-T standards (Experience, Expertise, Authoritativeness, Trustworthiness)."""

# Maximum token limits
MAX_TOKENS_RESEARCH = 1500
MAX_TOKENS_OUTLINE = 1000
MAX_TOKENS_SECTION = 2000
MAX_TOKENS_FULL_POST = 4000
