"""
Test script to demonstrate all the advanced features of the enhanced blog generator.
This creates a sample blog with all the new capabilities enabled.
"""
import argparse
import os
import time
from advanced_blog_generator import AdvancedBlogGenerator

def main():
    print("\n" + "=" * 80)
    print("ADVANCED BLOG GENERATOR - FEATURE DEMONSTRATION")
    print("=" * 80)
    
    # Create a test client request with all features
    print("\nCreating test demo request...")
    test_topic = "Artificial Intelligence in Healthcare: Transforming Patient Care"
    test_competitor_urls = [
        "https://www.ibm.com/topics/artificial-intelligence-healthcare",
        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6616181/",
        "https://builtin.com/artificial-intelligence/artificial-intelligence-healthcare"
    ]
    test_focus_areas = [
        "AI diagnostic tools and imaging analysis",
        "Natural language processing in clinical documentation",
        "Predictive analytics for patient outcomes",
        "Ethical considerations and privacy concerns",
        "Implementation challenges and success stories",
        "Future trends and emerging technologies"
    ]
    
    # Initialize the advanced blog generator
    generator = AdvancedBlogGenerator()
    
    # Set parameters to showcase all features
    print("Setting up all advanced features...")
    generator.set_parameters(
        topic=test_topic,
        competitor_urls=test_competitor_urls,
        focus_areas=test_focus_areas,
        content_length="long",
        content_depth="advanced",
        include_images=True,
        include_videos=True,
        tone="informative and authoritative",
        target_audience="healthcare professionals and technology enthusiasts",
        content_format="article",  # Using article format instead of blog
        reading_level="advanced",  # Using advanced reading level
        seo_optimization=True,     # Enable SEO optimization
        include_references=True,   # Include references and citations
        include_summary=True,      # Generate content summaries
        export_format="html"       # Export to HTML as well as markdown
    )
    
    # Generate the demo blog with all features
    print("\nGenerating comprehensive blog with all advanced features...\n")
    start_time = time.time()
    result = generator.generate_blog()
    elapsed_time = time.time() - start_time
    
    # Display results
    print("\n" + "=" * 80)
    print("ADVANCED FEATURE DEMONSTRATION COMPLETE")
    print("=" * 80)
    
    print("\nGenerated content with the following advanced features:")
    print("  ✓ SEO Optimization (keywords, meta description, title suggestions)")
    print("  ✓ Article format (more formal and structured than a blog)")
    print("  ✓ Advanced reading level adjustment")
    print("  ✓ Multimedia integration (image and video suggestions)")
    print("  ✓ References and citations")
    print("  ✓ Content summarization (executive, social, email)")
    print("  ✓ Content analysis and reading time estimation")
    print("  ✓ HTML export format")
    
    print("\nContent Statistics:")
    if 'content_stats' in result['project_data']:
        stats = result['project_data']['content_stats']
        print(f"  - Word count: {stats['word_count']}")
        print(f"  - Sentence count: {stats['sentence_count']}")
        print(f"  - Paragraph count: {stats['paragraph_count']}")
        print(f"  - Reading time: {result['project_data']['reading_time']} minutes")
        print(f"  - Reading level score: {stats['reading_level_score']:.1f}")
    
    print("\nFiles saved to:")
    print(f"  - Blog post: {result['paths']['post']}")
    print(f"  - Project data: {result['paths']['project']}")
    if 'export' in result['paths']:
        print(f"  - HTML export: {result['paths']['export']}")
    
    print(f"\nTotal generation time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
    
    print("\nTIP: To compare with basic blog generation, generate a blog without these advanced features")
    print("     using the standard format or disabling the advanced options.")
    
    # Display a sample of the social media summary if available
    if 'summaries' in result['project_data'] and result['project_data']['summaries'].get('social'):
        print("\nSample Social Media Summary:")
        print(f"  \"{result['project_data']['summaries']['social']}\"")

if __name__ == "__main__":
    main()
