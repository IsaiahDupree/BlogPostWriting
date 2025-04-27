"""
Generate a blog post based on a client request file using the Advanced Blog Generator.

Example usage:
python generate_client_blog.py --request client_request.txt
"""
import os
import argparse
import time
from advanced_blog_generator import AdvancedBlogGenerator

def main():
    parser = argparse.ArgumentParser(description="Generate a blog post based on client requirements")
    parser.add_argument("--request", required=True, help="Path to client request file")
    parser.add_argument("--length", choices=["short", "medium", "long", "comprehensive"], 
                        help="Override content length from request")
    parser.add_argument("--depth", choices=["beginner", "intermediate", "advanced", "expert"], 
                        help="Override content depth from request")
    parser.add_argument("--format", choices=["blog", "article", "whitepaper"],
                        help="Content format style")
    parser.add_argument("--reading-level", choices=["basic", "intermediate", "advanced"],
                        help="Target reading level for the content")
    parser.add_argument("--no-images", action="store_true", help="Disable image suggestions")
    parser.add_argument("--no-videos", action="store_true", help="Disable video suggestions")
    parser.add_argument("--no-seo", action="store_true", help="Disable SEO optimization")
    parser.add_argument("--references", action="store_true", help="Include references and citations")
    parser.add_argument("--summary", action="store_true", help="Include content summaries")
    parser.add_argument("--export", choices=["markdown", "html", "pdf"],
                        help="Export format for the generated content")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.request):
        print(f"Error: Client request file not found at '{args.request}'")
        return
    
    # Initialize the advanced blog generator
    print(f"Initializing Advanced Blog Generator...")
    generator = AdvancedBlogGenerator()
    
    # Load client request
    generator.load_client_request(args.request)
    
    # Apply any override parameters
    params = {}
    if args.length:
        params["content_length"] = args.length
    if args.depth:
        params["content_depth"] = args.depth
    if args.format:
        params["content_format"] = args.format
    if args.reading_level:
        params["reading_level"] = args.reading_level
    if args.no_images:
        params["include_images"] = False
    if args.no_videos:
        params["include_videos"] = False
    if args.no_seo:
        params["seo_optimization"] = False
    if args.references:
        params["include_references"] = True
    if args.summary:
        params["include_summary"] = True
    if args.export:
        params["export_format"] = args.export
    
    if params:
        generator.set_parameters(**params)
    
    # Generate the blog post
    print("\nGenerating blog post...\n")
    start_time = time.time()
    result = generator.generate_blog()
    
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 80)
    print("BLOG GENERATION COMPLETE")
    print("=" * 80)
    print(f"Files saved to:")
    print(f"  - Blog post: {result['paths']['post']}")
    print(f"  - Project data: {result['paths']['project']}")
    
    # Display any additional export paths
    if 'export' in result['paths']:
        print(f"  - Exported format: {result['paths']['export']}")
    
    # Display content statistics if available
    if 'content_stats' in result['project_data']:
        stats = result['project_data']['content_stats']
        print("\nContent Statistics:")
        print(f"  - Word count: {stats['word_count']}")
        print(f"  - Reading time: {result['project_data']['reading_time']} minutes")
        print(f"  - Reading level score: {stats['reading_level_score']:.1f}")
    
    # Display summary info if available
    if 'summaries' in result['project_data'] and result['project_data']['summaries'].get('social'):
        print("\nSocial Media Summary:")
        print(f"  \"{result['project_data']['summaries']['social']}\"")
    
    print(f"\nTotal generation time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
    print("\nBlog generation complete! You can find the generated files in the locations above.")

if __name__ == "__main__":
    main()
