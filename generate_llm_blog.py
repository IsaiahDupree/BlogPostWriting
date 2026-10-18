"""
Script to generate a high-quality blog post about Large Language Models
using the enhanced blog post generator with Perplexity API research.
"""
import os
import time
from blog_generator import BlogPostGenerator

# Define the blog topic
blog_topic = "Large Language Models (LLMs): The Future of NLP"
target_audience = "Technical professionals, AI researchers, and business leaders interested in NLP and AI"
tone = "informative, educational, and technically authoritative"

# Define competitor URLs for analysis
competitor_urls = [
    "https://aws.amazon.com/what-is/nlp/",
    "https://www.ibm.com/think/topics/natural-language-processing",
    "https://www.techtarget.com/searchenterpriseai/definition/natural-language-processing-NLP"
]

# Define focus areas for the blog
focus_areas = [
    "Evolution and development of LLMs",
    "Current state-of-the-art LLM architectures and capabilities",
    "Key differences between major LLMs like GPT, BERT, LLaMA, etc.",
    "Practical applications of LLMs in business and industry",
    "Ethical considerations and limitations of LLMs",
    "Future trends and directions in LLM development"
]

def generate_llm_blog():
    """Generate a comprehensive blog post about Large Language Models."""
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
    generate_llm_blog()
