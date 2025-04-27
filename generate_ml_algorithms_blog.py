"""
Script to generate a high-quality blog post about Machine Learning Algorithms
using the enhanced blog post generator with Perplexity API research.
"""
import os
import time
from blog_generator import BlogPostGenerator

# Define the blog topic
blog_topic = "Machine Learning Algorithms: From Basic to Advanced"
target_audience = "Data scientists, AI practitioners, and software developers interested in machine learning implementation"
tone = "informative, educational, and technically detailed"

# Define competitor URLs for analysis
competitor_urls = [
    "https://www.ibm.com/topics/machine-learning",
    "https://www.geeksforgeeks.org/machine-learning-algorithms/",
    "https://towardsdatascience.com/all-machine-learning-algorithms-you-should-know-in-2022-db5b4ccdf32f"
]

# Define focus areas for the blog
focus_areas = [
    "Supervised Learning Algorithms (Linear Regression, Decision Trees, Random Forests, etc.)",
    "Unsupervised Learning Algorithms (K-means, Hierarchical Clustering, etc.)",
    "Reinforcement Learning Fundamentals",
    "Ensemble Methods and Their Advantages",
    "Algorithm Selection Guidelines and Best Practices",
    "Performance Metrics and Evaluation Techniques",
    "Hyperparameter Tuning Strategies",
    "Practical Implementation Examples with Popular Libraries"
]

def generate_ml_algorithms_blog():
    """Generate a comprehensive blog post about Machine Learning Algorithms."""
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
    generate_ml_algorithms_blog()
