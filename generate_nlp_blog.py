"""
Script to generate a high-quality blog post about Natural Language Processing Fundamentals
using the enhanced blog post generator with Perplexity API research.
"""
import os
import time
from blog_generator import BlogPostGenerator

# Define the blog topic
blog_topic = "Natural Language Processing (NLP) Fundamentals: A Comprehensive Guide"
target_audience = "Data scientists, software developers, and AI enthusiasts interested in NLP technologies"
tone = "informative, educational, and technically precise"

# Define competitor URLs for analysis
competitor_urls = [
    "https://www.ibm.com/topics/natural-language-processing",
    "https://monkeylearn.com/blog/natural-language-processing-basics/",
    "https://www.datacamp.com/blog/what-is-natural-language-processing"
]

# Define focus areas for the blog
focus_areas = [
    "Core NLP concepts and terminology",
    "Text preprocessing techniques (tokenization, stemming, lemmatization)",
    "Word embeddings and vector representations",
    "Sentiment analysis and emotion detection",
    "Named Entity Recognition (NER)",
    "Language models and their evolution",
    "Practical NLP applications and use cases",
    "Getting started with NLP libraries (NLTK, spaCy, HuggingFace)"
]

def generate_nlp_blog():
    """Generate a comprehensive blog post about NLP Fundamentals."""
    start_time = time.time()
    
    print(f"Generating blog: {blog_topic}")
    print("=" * 80)
    
    # Initialize the generator
    generator = BlogPostGenerator()
    
    # Create a new project
    print(f"Creating project for: {blog_topic}")
    generator.create_new_project(
        topic=blog_topic,
        target_audience=target_audience,
        tone=tone
    )
    
    # Conduct research using Perplexity API
    print("Conducting research with Perplexity API...")
    generator.conduct_research(
        competitor_urls=competitor_urls,
        focus_areas=focus_areas,
        use_perplexity=True  # Use Perplexity API for enhanced research
    )
    print("Research completed.")
    
    # Generate outline
    print("Generating outline...")
    generator.generate_outline()
    print("Outline generated.")
    
    # Extract sections from outline
    generator.extract_sections_from_outline()
    
    # Generate full post
    print("Generating full blog post...")
    generator.generate_full_post()
    print("Blog post generated.")
    
    # Generate strategy memo
    print("Generating strategy memo...")
    strategy_memo = generator.generate_strategy_memo()
    print("Strategy memo generated.")
    
    # Save project
    print("Saving project...")
    save_paths = generator.save_project()
    print(f"Project saved to: {save_paths['post']}")
    
    # Print summary of generated blog
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 80)
    print("BLOG GENERATION SUMMARY")
    print("=" * 80)
    print(f"Topic: {blog_topic}")
    print(f"Blog post path: {save_paths['post']}")
    print(f"Project data: {save_paths['project']}")
    print(f"Total time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
    
    # Return the paths to the generated files
    return save_paths

if __name__ == "__main__":
    generate_nlp_blog()
