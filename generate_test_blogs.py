"""
Script to generate 3 test blog posts about different NLP topics.
This script bypasses the Streamlit UI and directly uses the BlogPostGenerator class.
"""
import os
import time
from blog_generator import BlogPostGenerator

# Ensure the projects directory exists
os.makedirs("projects", exist_ok=True)

# Define the topics for our test blogs
test_topics = [
    {
        "title": "Natural Language Processing (NLP) Fundamentals",
        "audience": "Technical professionals interested in AI and NLP",
        "tone": "educational and accessible",
        "competitors": [
            "https://aws.amazon.com/what-is/nlp/",
            "https://www.ibm.com/think/topics/natural-language-processing",
            "https://www.techtarget.com/searchenterpriseai/definition/natural-language-processing-NLP"
        ],
        "focus": [
            "Core NLP concepts and techniques",
            "Historical evolution and recent advancements",
            "Fundamental algorithms and approaches"
        ]
    },
    {
        "title": "Practical Applications of NLP in Business",
        "audience": "Business leaders and decision-makers",
        "tone": "professional and strategic",
        "competitors": [
            "https://aws.amazon.com/what-is/nlp/",
            "https://www.ibm.com/think/topics/natural-language-processing",
            "https://www.techtarget.com/searchenterpriseai/definition/natural-language-processing-NLP"
        ],
        "focus": [
            "Business use cases across industries",
            "ROI and implementation considerations",
            "Case studies of successful NLP deployments"
        ]
    },
    {
        "title": "The Future of NLP: Trends and Emerging Technologies",
        "audience": "AI researchers and technology enthusiasts",
        "tone": "forward-thinking and technical",
        "competitors": [
            "https://aws.amazon.com/what-is/nlp/",
            "https://www.ibm.com/think/topics/natural-language-processing",
            "https://www.techtarget.com/searchenterpriseai/definition/natural-language-processing-NLP"
        ],
        "focus": [
            "Latest research and breakthroughs in NLP",
            "Emerging models and architectures",
            "Future directions and potential applications"
        ]
    }
]

def generate_blog(topic_data):
    """Generate a single blog post based on the provided topic data."""
    print(f"\n\n{'='*80}")
    print(f"Generating blog: {topic_data['title']}")
    print(f"{'='*80}")
    
    # Initialize the generator
    generator = BlogPostGenerator()
    
    # Create a new project
    print(f"Creating project for: {topic_data['title']}")
    generator.create_new_project(
        topic=topic_data['title'],
        target_audience=topic_data['audience'],
        tone=topic_data['tone']
    )
    
    # Conduct research
    print("Conducting research...")
    generator.conduct_research(
        competitor_urls=topic_data['competitors'],
        focus_areas=topic_data['focus']
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
    
    # Return the paths to the generated files
    return save_paths

def main():
    """Generate all test blogs."""
    start_time = time.time()
    
    print(f"Starting generation of {len(test_topics)} test blogs...")
    
    results = []
    for i, topic_data in enumerate(test_topics, 1):
        print(f"\nGenerating test blog {i} of {len(test_topics)}...")
        result = generate_blog(topic_data)
        results.append(result)
    
    # Print summary of generated blogs
    print("\n\n" + "="*80)
    print("SUMMARY OF GENERATED BLOGS")
    print("="*80)
    for i, (topic_data, result) in enumerate(zip(test_topics, results), 1):
        print(f"{i}. {topic_data['title']}")
        print(f"   - Post: {result['post']}")
        print(f"   - Project data: {result['project']}")
    
    elapsed_time = time.time() - start_time
    print(f"\nTotal time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
    print("Done!")

if __name__ == "__main__":
    main()
