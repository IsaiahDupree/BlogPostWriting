"""
Advanced Blog Post Generator
A flexible, all-in-one solution to generate blog posts on any topic with customizable parameters.

This generator can:
- Read requirements from client request files
- Customize content length, depth, and style
- Include suggestions for multimedia elements (images and videos)
- Work with both OpenAI and Perplexity API for enhanced research
- Create SEO-optimized content based on specific requirements
- Generate content in various formats (blog post, article, whitepaper)
- Optimize content for search engines with keyword analysis
- Adjust reading level based on target audience
- Estimate reading time for generated content
- Generate citations and references
- Create content summaries for different purposes
- Export content to various formats
"""
import os
import json
import re
import time
import math
import random
import datetime
from typing import Dict, List, Optional, Union, Tuple
from blog_generator import BlogPostGenerator
from ai_service import AIService
from perplexity_service import PerplexityService
from pathlib import Path

class AdvancedBlogGenerator:
    """An enhanced blog generator that can adapt to specific client requirements."""
    
    # Content format templates
    CONTENT_FORMATS = {
        "blog": "conversational, engaging, with personal insights",
        "article": "informative, structured, with supporting evidence",
        "whitepaper": "formal, technical, with detailed analysis and research"
    }
    
    # Reading level guidelines
    READING_LEVELS = {
        "basic": "simple vocabulary, short sentences, easy to understand concepts",
        "intermediate": "moderate vocabulary, varied sentence structure, some specialized terms",
        "advanced": "sophisticated vocabulary, complex sentence structures, technical terminology"
    }
    
    def __init__(self):
        """Initialize the advanced blog generator."""
        # Initialize base services
        self.blog_generator = BlogPostGenerator()
        self.ai_service = AIService()
        try:
            self.perplexity_service = PerplexityService()
            self.perplexity_available = True
        except ValueError:
            self.perplexity_available = False
            print("Perplexity API not available. Using OpenAI for all tasks.")
        
        # Default parameters
        self.default_params = {
            "content_length": "long",  # short, medium, long, comprehensive
            "content_depth": "intermediate",  # beginner, intermediate, advanced, expert
            "include_images": True,
            "include_videos": True,
            "tone": "informative and educational",
            "target_audience": "professionals and enthusiasts",
            "content_format": "blog",  # blog, article, whitepaper
            "reading_level": "intermediate",  # basic, intermediate, advanced
            "seo_optimization": True,
            "include_references": True,
            "include_summary": False,
            "export_format": "markdown"  # markdown, html, pdf
        }
        
        # Initialize project data
        self.project_data = {
            "client_request": {},
            "topic": "",
            "competitor_urls": [],
            "focus_areas": [],
            "params": self.default_params.copy(),
            "multimedia": {
                "image_suggestions": [],
                "video_suggestions": []
            },
            "seo": {
                "keywords": [],
                "meta_description": "",
                "title_suggestions": []
            },
            "references": [],
            "summary": "",
            "reading_time": 0,
            "content_stats": {
                "word_count": 0,
                "sentence_count": 0,
                "paragraph_count": 0,
                "reading_level_score": 0
            }
        }
    
    def load_client_request(self, file_path: str) -> Dict:
        """
        Parse client request file and extract requirements.
        
        Args:
            file_path (str): Path to the client request file
            
        Returns:
            Dict: Parsed client requirements
        """
        print(f"Loading client request from: {file_path}")
        
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            
            # Parse the client request content
            client_request = {}
            
            # Extract topic (first line usually contains the topic)
            lines = content.split('\n')
            client_request["topic"] = lines[0].strip()
            
            # Extract competitor URLs
            competitor_urls = []
            url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
            for line in lines:
                urls = re.findall(url_pattern, line)
                competitor_urls.extend(urls)
            client_request["competitor_urls"] = competitor_urls
            
            # Extract deliverables and requirements
            deliverables_section = False
            requirements_section = False
            deliverables = []
            requirements = []
            
            for line in lines:
                line = line.strip()
                if line == "Deliverables":
                    deliverables_section = True
                    requirements_section = False
                    continue
                elif line == "Requirements":
                    deliverables_section = False
                    requirements_section = True
                    continue
                elif line.startswith("Bonus Points") or line.startswith("🔎 To Apply"):
                    deliverables_section = False
                    requirements_section = False
                    continue
                
                if deliverables_section and line and line.startswith("-"):
                    deliverables.append(line[1:].strip())
                elif requirements_section and line and line.startswith("-"):
                    requirements.append(line[1:].strip())
            
            client_request["deliverables"] = deliverables
            client_request["requirements"] = requirements
            
            # Determine content parameters based on request content
            params = self.default_params.copy()
            
            # Determine content length
            if any("long-form" in d.lower() for d in deliverables):
                params["content_length"] = "long"
            elif any("comprehensive" in d.lower() for d in deliverables):
                params["content_length"] = "comprehensive"
            
            # Determine content depth
            if any("expert" in r.lower() or "advanced" in r.lower() for r in requirements):
                params["content_depth"] = "advanced"
            
            # Check for multimedia requirements
            params["include_images"] = any("illustration" in d.lower() or "visual" in d.lower() for d in deliverables)
            params["include_videos"] = any("video" in d.lower() for d in deliverables)
            
            client_request["params"] = params
            
            # Extract focus areas from deliverables
            focus_areas = []
            for item in deliverables:
                if "such as" in item:
                    part_after_such_as = item.split("such as")[1]
                    topics = [t.strip() for t in re.split(r',|\band\b', part_after_such_as)]
                    focus_areas.extend(topics)
            
            if not focus_areas and "topic" in client_request:
                # Generate focus areas based on the topic if none were found
                focus_areas = self._generate_focus_areas(client_request["topic"])
            
            client_request["focus_areas"] = focus_areas
            
            self.project_data["client_request"] = client_request
            self.project_data["topic"] = client_request["topic"]
            self.project_data["competitor_urls"] = client_request["competitor_urls"]
            self.project_data["focus_areas"] = client_request["focus_areas"]
            self.project_data["params"] = client_request["params"]
            
            print(f"Successfully parsed client request: {client_request['topic']}")
            return client_request
            
        except Exception as e:
            print(f"Error parsing client request: {e}")
            return {}
    
    def _generate_focus_areas(self, topic: str) -> List[str]:
        """
        Generate focus areas based on a topic.
        
        Args:
            topic (str): Main topic
            
        Returns:
            List[str]: Generated focus areas
        """
        prompt = f"""
        Based on the topic "{topic}", generate 6-8 key focus areas that should be covered in a comprehensive blog post.
        Each focus area should be specific and address an important aspect of the topic.
        Return the focus areas as a comma-separated list.
        """
        
        system_prompt = "You are an expert content strategist tasked with identifying key subtopics for comprehensive blog posts."
        
        result = self.ai_service.generate_content(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=500
        )
        
        # Parse the comma-separated list
        focus_areas = [area.strip() for area in result.split(',')]
        
        return focus_areas
    
    def set_parameters(self, 
                      topic: str = None,
                      competitor_urls: List[str] = None,
                      focus_areas: List[str] = None,
                      content_length: str = None,
                      content_depth: str = None,
                      include_images: bool = None,
                      include_videos: bool = None,
                      tone: str = None,
                      target_audience: str = None,
                      content_format: str = None,
                      reading_level: str = None,
                      seo_optimization: bool = None,
                      include_references: bool = None,
                      include_summary: bool = None,
                      export_format: str = None) -> None:
        """
        Set project parameters manually.
        
        Args:
            topic (str, optional): Main blog topic
            competitor_urls (List[str], optional): URLs of competing articles
            focus_areas (List[str], optional): Specific areas to focus on
            content_length (str, optional): short, medium, long, or comprehensive
            content_depth (str, optional): beginner, intermediate, advanced, or expert
            include_images (bool, optional): Whether to include image suggestions
            include_videos (bool, optional): Whether to include video suggestions
            tone (str, optional): Content tone (e.g., informative, conversational)
            target_audience (str, optional): Target audience description
        """
        if topic:
            self.project_data["topic"] = topic
        
        if competitor_urls:
            self.project_data["competitor_urls"] = competitor_urls
        
        if focus_areas:
            self.project_data["focus_areas"] = focus_areas
        
        # Update parameters if provided
        if content_length:
            self.project_data["params"]["content_length"] = content_length
        
        if content_depth:
            self.project_data["params"]["content_depth"] = content_depth
        
        if include_images is not None:
            self.project_data["params"]["include_images"] = include_images
        
        if include_videos is not None:
            self.project_data["params"]["include_videos"] = include_videos
        
        if tone:
            self.project_data["params"]["tone"] = tone
        
        if target_audience:
            self.project_data["params"]["target_audience"] = target_audience
            
        if content_format:
            self.project_data["params"]["content_format"] = content_format
            
        if reading_level:
            self.project_data["params"]["reading_level"] = reading_level
            
        if seo_optimization is not None:
            self.project_data["params"]["seo_optimization"] = seo_optimization
            
        if include_references is not None:
            self.project_data["params"]["include_references"] = include_references
            
        if include_summary is not None:
            self.project_data["params"]["include_summary"] = include_summary
            
        if export_format:
            self.project_data["params"]["export_format"] = export_format
        
        print("Project parameters updated successfully.")
    
    def generate_blog(self) -> Dict:
        """
        Generate a complete blog post based on project parameters.
        
        Returns:
            Dict: Paths to generated files and project data
        """
        if not self.project_data["topic"]:
            raise ValueError("No topic specified. Please load a client request or set parameters manually.")
        
        start_time = time.time()
        print(f"Generating blog: {self.project_data['topic']}")
        print("=" * 80)
        
        # Initialize the blog generator with project parameters
        self.blog_generator.create_new_project(
            topic=self.project_data["topic"],
            target_audience=self.project_data["params"]["target_audience"],
            tone=self.project_data["params"]["tone"]
        )
        
        # Configure token limits based on content length
        token_multiplier = {
            "short": 0.7,
            "medium": 1.0,
            "long": 1.5,
            "comprehensive": 2.0
        }.get(self.project_data["params"]["content_length"], 1.0)
        
        # Conduct research
        print("Conducting research...")
        use_perplexity = self.perplexity_available
        self.blog_generator.conduct_research(
            competitor_urls=self.project_data["competitor_urls"],
            focus_areas=self.project_data["focus_areas"],
            use_perplexity=use_perplexity
        )
        print("Research completed.")
        
        # Generate multimedia suggestions if required
        if self.project_data["params"]["include_images"]:
            print("Generating image suggestions...")
            self._generate_image_suggestions()
        
        if self.project_data["params"]["include_videos"]:
            print("Generating video suggestions...")
            self._generate_video_suggestions()
        
        # Generate outline with appropriate depth
        print("Generating outline...")
        self.blog_generator.generate_outline()
        print("Outline generated.")
        
        # Extract sections from outline
        self.blog_generator.extract_sections_from_outline()
        
        # Generate full post
        print("Generating full blog post...")
        self.blog_generator.generate_full_post()
        print("Blog post generated.")
        
        # Perform SEO optimization if required
        if self.project_data["params"]["seo_optimization"]:
            print("Optimizing content for SEO...")
            self._generate_seo_elements()
            print("SEO optimization completed.")
        
        # Integrate multimedia suggestions into content
        if self.project_data["params"]["include_images"] or self.project_data["params"]["include_videos"]:
            print("Integrating multimedia suggestions...")
            self._integrate_multimedia_suggestions()
            
        # Analyze content and calculate reading time
        print("Analyzing content statistics...")
        self._analyze_content()
        print(f"Estimated reading time: {self.project_data['reading_time']} minutes")
        
        # Adjust reading level if needed
        if self.project_data["params"]["reading_level"] != "intermediate":
            print(f"Adjusting content for {self.project_data['params']['reading_level']} reading level...")
            self._adjust_reading_level()
            print("Reading level adjustment completed.")
            
        # Generate references if required
        if self.project_data["params"]["include_references"]:
            print("Generating references and citations...")
            self._generate_references()
            print("References generated.")
            
        # Generate content summary if required
        if self.project_data["params"]["include_summary"]:
            print("Generating content summary...")
            self._generate_summary()
            print("Summary generated.")
        
        # Generate strategy memo
        print("Generating strategy memo...")
        strategy_memo = self.blog_generator.generate_strategy_memo()
        print("Strategy memo generated.")
        
        # Save project
        print("Saving project...")
        save_paths = self.blog_generator.save_project()
        
        # Add multimedia suggestions to project data for saving
        self.blog_generator.current_project["multimedia"] = self.project_data["multimedia"]
        
        # Add other advanced content elements to project data
        if "seo" in self.project_data and self.project_data["seo"]["keywords"]:
            self.blog_generator.current_project["seo"] = self.project_data["seo"]
        
        if "references" in self.project_data and self.project_data["references"]:
            self.blog_generator.current_project["references"] = self.project_data["references"]
            
        if "summaries" in self.project_data and self.project_data["summaries"]:
            self.blog_generator.current_project["summaries"] = self.project_data["summaries"]
            
        if "content_stats" in self.project_data:
            self.blog_generator.current_project["content_stats"] = self.project_data["content_stats"]
            self.blog_generator.current_project["reading_time"] = self.project_data["reading_time"]
        
        # Save updated project with all additions
        with open(save_paths["project"], 'w') as f:
            json.dump(self.blog_generator.current_project, f, indent=2)
            
        # Export in desired format if not markdown
        if self.project_data["params"]["export_format"] != "markdown":
            export_path = self._export_content(save_paths["post"])
            if export_path:
                save_paths["export"] = export_path
        
        # Print summary
        elapsed_time = time.time() - start_time
        print("\n" + "=" * 80)
        print("BLOG GENERATION SUMMARY")
        print("=" * 80)
        print(f"Topic: {self.project_data['topic']}")
        print(f"Content Length: {self.project_data['params']['content_length']}")
        print(f"Content Depth: {self.project_data['params']['content_depth']}")
        print(f"Blog post path: {save_paths['post']}")
        print(f"Project data: {save_paths['project']}")
        print(f"Total time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
        
        return {
            "paths": save_paths,
            "project_data": self.project_data,
            "elapsed_time": elapsed_time
        }
    
    def _generate_image_suggestions(self) -> List[Dict]:
        """
        Generate suggestions for images to include in the blog post.
        
        Returns:
            List[Dict]: Image suggestions with descriptions and placement
        """
        prompt = f"""
        For a blog post about "{self.project_data['topic']}", suggest 3-5 custom images or diagrams that would enhance the content.
        
        For each suggestion, provide:
        1. A detailed description of the image
        2. The recommended section where it should appear
        3. A brief explanation of why this visual would benefit readers
        
        Format each suggestion as:
        
        IMAGE [number]: [brief title]
        DESCRIPTION: [detailed description for designer/creator]
        PLACEMENT: [recommended section]
        RATIONALE: [why this image adds value]
        """
        
        system_prompt = """You are a visual content strategist who specializes in creating effective image suggestions
        for technical blog posts. Your suggestions should be specific, descriptive, and strategically valuable."""
        
        result = self.ai_service.generate_content(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=1000
        )
        
        # Parse the image suggestions
        image_blocks = re.split(r'IMAGE \d+:', result)[1:]
        image_suggestions = []
        
        for i, block in enumerate(image_blocks, 1):
            lines = block.strip().split('\n')
            suggestion = {
                "id": i,
                "title": lines[0].strip() if lines else f"Image {i}",
                "description": "",
                "placement": "",
                "rationale": ""
            }
            
            for line in lines:
                if line.startswith("DESCRIPTION:"):
                    suggestion["description"] = line.replace("DESCRIPTION:", "").strip()
                elif line.startswith("PLACEMENT:"):
                    suggestion["placement"] = line.replace("PLACEMENT:", "").strip()
                elif line.startswith("RATIONALE:"):
                    suggestion["rationale"] = line.replace("RATIONALE:", "").strip()
            
            image_suggestions.append(suggestion)
        
        self.project_data["multimedia"]["image_suggestions"] = image_suggestions
        return image_suggestions
    
    def _generate_video_suggestions(self) -> List[Dict]:
        """
        Generate suggestions for videos to embed in the blog post.
        
        Returns:
            List[Dict]: Video suggestions with topics and placement
        """
        prompt = f"""
        For a blog post about "{self.project_data['topic']}", suggest 2-3 types of videos that would enhance the content.
        
        For each suggestion, provide:
        1. The video topic/title
        2. Key content the video should contain
        3. The recommended section where it should be embedded
        4. Search terms to find a suitable video on platforms like YouTube
        
        Format each suggestion as:
        
        VIDEO [number]: [video topic/title]
        CONTENT: [what the video should explain/demonstrate]
        PLACEMENT: [recommended section]
        SEARCH TERMS: [keywords to find this video]
        """
        
        system_prompt = """You are a multimedia content strategist specializing in identifying effective video 
        content to complement blog posts. Your suggestions should enhance learning and increase time-on-page."""
        
        result = self.ai_service.generate_content(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=800
        )
        
        # Parse the video suggestions
        video_blocks = re.split(r'VIDEO \d+:', result)[1:]
        video_suggestions = []
        
        for i, block in enumerate(video_blocks, 1):
            lines = block.strip().split('\n')
            suggestion = {
                "id": i,
                "title": lines[0].strip() if lines else f"Video {i}",
                "content": "",
                "placement": "",
                "search_terms": ""
            }
            
            for line in lines:
                if line.startswith("CONTENT:"):
                    suggestion["content"] = line.replace("CONTENT:", "").strip()
                elif line.startswith("PLACEMENT:"):
                    suggestion["placement"] = line.replace("PLACEMENT:", "").strip()
                elif line.startswith("SEARCH TERMS:"):
                    suggestion["search_terms"] = line.replace("SEARCH TERMS:", "").strip()
            
            video_suggestions.append(suggestion)
        
        self.project_data["multimedia"]["video_suggestions"] = video_suggestions
        return video_suggestions
    
    def _integrate_multimedia_suggestions(self) -> None:
        """Integrate multimedia suggestions into the blog post content."""
        # Get current full post content
        full_post = self.blog_generator.current_project["full_post"]
        sections = self.blog_generator.current_project["sections"]
        
        # Build a map of section titles to their content
        section_map = {}
        for title, data in sections.items():
            section_map[title.lower()] = title
        
        # Placeholder for multimedia markdown to insert
        image_markers = []
        video_markers = []
        
        # Process image suggestions
        for img in self.project_data["multimedia"]["image_suggestions"]:
            placement = img["placement"].lower()
            
            # Find the best matching section
            best_match = None
            best_match_score = 0
            for section_lower, section_original in section_map.items():
                # Calculate simple matching score
                words_in_placement = set(placement.split())
                words_in_section = set(section_lower.split())
                common_words = words_in_placement.intersection(words_in_section)
                
                if len(common_words) > best_match_score:
                    best_match_score = len(common_words)
                    best_match = section_original
            
            if best_match:
                image_marker = f'\n\n<!-- IMAGE SUGGESTION {img["id"]}: "{img["title"]}" -->\n'
                image_marker += f'<!-- DESCRIPTION: {img["description"]} -->\n'
                image_marker += f'<!-- PLACEHOLDER: ![{img["title"]}](/path/to/image{img["id"]}.jpg) -->\n\n'
                
                image_markers.append((best_match, image_marker))
        
        # Process video suggestions
        for vid in self.project_data["multimedia"]["video_suggestions"]:
            placement = vid["placement"].lower()
            
            # Find the best matching section
            best_match = None
            best_match_score = 0
            for section_lower, section_original in section_map.items():
                # Calculate simple matching score
                words_in_placement = set(placement.split())
                words_in_section = set(section_lower.split())
                common_words = words_in_placement.intersection(words_in_section)
                
                if len(common_words) > best_match_score:
                    best_match_score = len(common_words)
                    best_match = section_original
            
            if best_match:
                video_marker = f'\n\n<!-- VIDEO SUGGESTION {vid["id"]}: "{vid["title"]}" -->\n'
                video_marker += f'<!-- CONTENT: {vid["content"]} -->\n'
                video_marker += f'<!-- SEARCH TERMS: {vid["search_terms"]} -->\n'
                video_marker += f'<!-- PLACEHOLDER: <iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID" frameborder="0" allowfullscreen></iframe> -->\n\n'
                
                video_markers.append((best_match, video_marker))
        
        # Insert markers into full post
        modified_post = full_post
        
        # Function to insert marker after a section heading
        def insert_after_heading(content, heading, marker):
            pattern = f"## {re.escape(heading)}"
            # Find the heading and get what comes after it until the next heading
            match = re.search(f"{pattern}.*?(?=\n## |$)", content, re.DOTALL)
            if match:
                heading_content = match.group(0)
                # Insert marker at the end of this section's content
                modified = content.replace(heading_content, heading_content + marker)
                return modified
            return content
        
        # Insert all image markers
        for section, marker in image_markers:
            modified_post = insert_after_heading(modified_post, section, marker)
        
        # Insert all video markers
        for section, marker in video_markers:
            modified_post = insert_after_heading(modified_post, section, marker)
        
        # Update the project with modified content
        self.blog_generator.current_project["full_post"] = modified_post

# Command-line interface for the advanced blog generator
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate a blog post based on client requirements")
    parser.add_argument("--request", help="Path to client request file")
    parser.add_argument("--topic", help="Blog topic")
    parser.add_argument("--competitors", help="Comma-separated list of competitor URLs")
    parser.add_argument("--focus", help="Comma-separated list of focus areas")
    parser.add_argument("--length", choices=["short", "medium", "long", "comprehensive"], help="Content length")
    parser.add_argument("--depth", choices=["beginner", "intermediate", "advanced", "expert"], help="Content depth")
    parser.add_argument("--images", type=bool, default=True, help="Include image suggestions")
    parser.add_argument("--videos", type=bool, default=True, help="Include video suggestions")
    parser.add_argument("--tone", help="Content tone")
    parser.add_argument("--audience", help="Target audience")
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = AdvancedBlogGenerator()
    
    # Load client request if provided
    if args.request:
        generator.load_client_request(args.request)
    
    # Set manual parameters if provided
    params = {}
    
    if args.topic:
        params["topic"] = args.topic
    
    if args.competitors:
        params["competitor_urls"] = args.competitors.split(",")
    
    if args.focus:
        params["focus_areas"] = args.focus.split(",")
    
    if args.length:
        params["content_length"] = args.length
    
    if args.depth:
        params["content_depth"] = args.depth
    
    if args.images is not None:
        params["include_images"] = args.images
    
    if args.videos is not None:
        params["include_videos"] = args.videos
    
    if args.tone:
        params["tone"] = args.tone
    
    if args.audience:
        params["target_audience"] = args.audience
    
    if params:
        generator.set_parameters(**params)
    
    # Generate blog post
    if generator.project_data["topic"]:
        generator.generate_blog()
    else:
        print("Error: No topic specified. Please provide either a client request file or a topic.")

    def _analyze_content(self) -> Dict:
        """
        Analyze content to extract statistics and calculate reading time.
        
        Returns:
            Dict: Content statistics
        """
        content = self.blog_generator.current_project["full_post"]
        
        # Calculate basic statistics
        words = re.findall(r'\w+', content)
        word_count = len(words)
        
        # Calculate sentence count (rough approximation)
        sentences = re.split(r'[.!?]+', content)
        sentence_count = len([s for s in sentences if len(s.strip()) > 0])
        
        # Calculate paragraph count
        paragraphs = [p for p in content.split('\n\n') if len(p.strip()) > 0]
        paragraph_count = len(paragraphs)
        
        # Calculate average words per sentence
        avg_words_per_sentence = word_count / max(1, sentence_count)
        
        # Calculate reading level using a simplified Flesch-Kincaid Grade Level formula
        syllable_count = sum(self._count_syllables(word) for word in words)
        if sentence_count > 0 and word_count > 0:
            reading_level_score = 0.39 * (word_count / sentence_count) + 11.8 * (syllable_count / word_count) - 15.59
        else:
            reading_level_score = 0
        
        # Estimate reading time (average reading speed: 200-250 words per minute)
        reading_time = math.ceil(word_count / 225)
        
        # Store the analysis in project data
        self.project_data["content_stats"] = {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count,
            "avg_words_per_sentence": avg_words_per_sentence,
            "reading_level_score": reading_level_score
        }
        self.project_data["reading_time"] = reading_time
        
        return self.project_data["content_stats"]
    
    def _count_syllables(self, word: str) -> int:
        """
        Count the number of syllables in a word (simplified approach).
        
        Args:
            word (str): Word to count syllables for
            
        Returns:
            int: Estimated syllable count
        """
        word = word.lower()
        # Remove common endings
        if word.endswith('e'):
            word = word[:-1]
        
        # Count vowel groups as syllables
        count = len(re.findall(r'[aeiouy]+', word))
        
        # Return at least 1 syllable per word
        return max(1, count)
    
    def _adjust_reading_level(self) -> str:
        """
        Adjust the content's reading level based on the target audience.
        
        Returns:
            str: Adjusted content
        """
        content = self.blog_generator.current_project["full_post"]
        target_level = self.project_data["params"]["reading_level"]
        reading_level_guidelines = self.READING_LEVELS[target_level]
        
        prompt = f"""
        Please rewrite the following content at a {target_level} reading level. 
        Guidelines for {target_level} reading level: {reading_level_guidelines}
        
        Original content:
        {content}
        
        Maintain all headings, structure, and information, but adjust the language complexity
        to match the {target_level} reading level. Ensure that any technical concepts are 
        explained appropriately for this reading level.
        """
        
        system_prompt = f"""You are an expert content editor specializing in adjusting content to specific reading levels 
        while preserving meaning and intent. Modify the language complexity while maintaining 
        all key information, headings, and structure. Aim for a {target_level} reading level."""
        
        result = self.ai_service.generate_content(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.4,
            max_tokens=4000
        )
        
        # Update the project with adjusted content
        self.blog_generator.current_project["full_post"] = result
        
        # Re-analyze content after adjustment
        self._analyze_content()
        
        return result
        
    def _generate_references(self) -> List[Dict]:
        """
        Generate references and citations for the blog post.
        
        Returns:
            List[Dict]: List of references with citation information
        """
        topic = self.project_data["topic"]
        content = self.blog_generator.current_project["full_post"]
        
        prompt = f"""
        For a blog post about "{topic}", generate a list of 8-10 high-quality references and citations.
        These should include academic papers, books, reputable websites, and industry reports that would
        strengthen the credibility of the content. Each reference should be relevant to the topic.
        
        Use the following content to identify appropriate reference topics:
        {content[:2000]}  # Using the first part of the content
        
        For each reference, provide:
        1. Full citation in APA format
        2. Brief description of why this source is valuable (1-2 sentences)
        3. A suggested inline citation location (quote a specific sentence from the content where this reference could be cited)
        
        Format each reference as:
        
        REFERENCE [number]: [Full APA citation]
        VALUE: [Brief description of source value]
        INLINE CITATION: [Sentence from the content where this could be cited]
        """
        
        system_prompt = """You are a research librarian and academic citation expert. Create high-quality, 
        relevant references that would strengthen the credibility of technical content. Focus on authoritative 
        sources including peer-reviewed journals, books by recognized experts, reports from reputable 
        organizations, and high-quality technical websites."""
        
        result = self.ai_service.generate_content(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=1500
        )
        
        # Parse the references
        reference_pattern = r'REFERENCE \d+: (.+?)\nVALUE: (.+?)\nINLINE CITATION: (.+?)(?=\n\n|$)'
        matches = re.findall(reference_pattern, result, re.DOTALL)
        
        references = []
        for i, (citation, value, inline) in enumerate(matches, 1):
            references.append({
                "id": i,
                "citation": citation.strip(),
                "value": value.strip(),
                "inline_citation": inline.strip()
            })
        
        # Store references in project data
        self.project_data["references"] = references
        
        # Add references section to the blog post
        if references:
            current_content = self.blog_generator.current_project["full_post"]
            references_section = "\n\n## References\n\n"
            for ref in references:
                references_section += f"{ref['id']}. {ref['citation']}\n\n"
            
            # Append references to the end of the content
            self.blog_generator.current_project["full_post"] = current_content + references_section
        
        return references
    
    def _generate_summary(self) -> str:
        """
        Generate a concise summary of the blog post content.
        
        Returns:
            str: Content summary
        """
        topic = self.project_data["topic"]
        content = self.blog_generator.current_project["full_post"]
        
        prompt = f"""
        Create three different summaries of the following blog post about "{topic}":
        
        {content[:3000]}  # Using the first part of the content
        
        Generate these summaries:
        
        1. EXECUTIVE SUMMARY (150-200 words): A comprehensive overview for busy professionals
        
        2. SOCIAL MEDIA SUMMARY (50 words): An engaging, shareable summary for social media
        
        3. EMAIL NEWSLETTER SUMMARY (100 words): A summary suitable for email newsletters with a call to action
        """
        
        system_prompt = """You are a content summarization expert. Create concise, accurate summaries that capture 
        the key points while maintaining the tone and intent of the original content. Each summary should be 
        tailored to its specific purpose and target audience."""
        
        result = self.ai_service.generate_content(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.4,
            max_tokens=1000
        )
        
        # Parse the summaries
        executive_match = re.search(r'EXECUTIVE SUMMARY.*?:(.*?)(?=\n\n\d\.\s|$)', result, re.DOTALL)
        social_match = re.search(r'SOCIAL MEDIA SUMMARY.*?:(.*?)(?=\n\n\d\.\s|$)', result, re.DOTALL)
        email_match = re.search(r'EMAIL NEWSLETTER SUMMARY.*?:(.*?)(?=$)', result, re.DOTALL)
        
        summaries = {
            "executive": executive_match.group(1).strip() if executive_match else "",
            "social": social_match.group(1).strip() if social_match else "",
            "email": email_match.group(1).strip() if email_match else ""
        }
        
        # Store summaries in project data
        self.project_data["summaries"] = summaries
        
        # Add executive summary to the beginning of the blog post
        if summaries["executive"]:
            current_content = self.blog_generator.current_project["full_post"]
            title_end = current_content.find('\n\n')
            if title_end > 0:
                # Insert after the title and meta description
                meta_desc_end = current_content.find('\n\n', title_end + 2)
                if meta_desc_end > 0:
                    insert_point = meta_desc_end + 2
                else:
                    insert_point = title_end + 2
                
                summary_section = f"**Executive Summary:** {summaries['executive']}\n\n"
                updated_content = current_content[:insert_point] + summary_section + current_content[insert_point:]
                self.blog_generator.current_project["full_post"] = updated_content
        
        return summaries
    
    def _generate_seo_elements(self) -> Dict:
        """
        Generate SEO elements for the blog post.
        
        Returns:
            Dict: SEO elements including keywords, meta description, and title suggestions
        """
        topic = self.project_data["topic"]
        content = self.blog_generator.current_project["full_post"]
        
        prompt = f"""
        For a blog post about "{topic}", generate comprehensive SEO elements including:
        
        1. A list of 10-15 primary and secondary keywords (provide these in a comma-separated list)
        2. A compelling meta description (155 characters max) that includes primary keywords
        3. 3 alternative SEO-optimized title suggestions that include primary keywords
        
        Use the following content to identify the most relevant keywords and themes:
        {content[:2000]}  # Using the first part of the content to keep prompt size reasonable
        
        Format your response as:
        
        KEYWORDS: keyword1, keyword2, keyword3, etc.
        
        META DESCRIPTION: Your 155-character meta description here
        
        TITLE SUGGESTIONS:
        1. First title suggestion
        2. Second title suggestion
        3. Third title suggestion
        """
        
        system_prompt = """You are an SEO expert specializing in creating highly optimized content elements. 
        Focus on relevance, search intent, and strategic keyword placement. Ensure meta descriptions
        are compelling and under 155 characters. Title suggestions should be attention-grabbing 
        while incorporating primary keywords."""
        
        result = self.ai_service.generate_content(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=800
        )
        
        # Parse the SEO elements
        keywords = []
        meta_description = ""
        title_suggestions = []
        
        keyword_match = re.search(r'KEYWORDS:\s*(.+?)\s*(?:\n|$)', result)
        if keyword_match:
            keywords_text = keyword_match.group(1)
            keywords = [kw.strip() for kw in keywords_text.split(',')]
        
        meta_match = re.search(r'META DESCRIPTION:\s*(.+?)\s*(?:\n|$)', result)
        if meta_match:
            meta_description = meta_match.group(1).strip()
        
        title_section = re.search(r'TITLE SUGGESTIONS:[\s\S]+', result)
        if title_section:
            title_text = title_section.group(0)
            title_matches = re.findall(r'\d+\.\s*(.+?)\s*(?:\n|$)', title_text)
            title_suggestions = [title.strip() for title in title_matches]
        
        # Store the SEO elements in project data
        self.project_data["seo"] = {
            "keywords": keywords,
            "meta_description": meta_description,
            "title_suggestions": title_suggestions
        }
        
        # Apply the meta description to the blog post content
        if meta_description and not "Meta Description:" in self.blog_generator.current_project["full_post"]:
            current_content = self.blog_generator.current_project["full_post"]
            first_line_end = current_content.find('\n')
            if first_line_end > 0:
                # Insert the meta description after the title
                updated_content = current_content[:first_line_end+1] + f"\n**Meta Description:** {meta_description}\n" + current_content[first_line_end+1:]
                self.blog_generator.current_project["full_post"] = updated_content
        
        return self.project_data["seo"]
        Returns:
            Dict: SEO elements including keywords, meta description, and title suggestions
        """
        topic = self.project_data["topic"]
        content = self.blog_generator.current_project["full_post"]
        
        prompt = f"""
        For a blog post about "{topic}", generate comprehensive SEO elements including:
        
        1. A list of 10-15 primary and secondary keywords (provide these in a comma-separated list)
        2. A compelling meta description (155 characters max) that includes primary keywords
        3. 3 alternative SEO-optimized title suggestions that include primary keywords
        
        Use the following content to identify the most relevant keywords and themes:
        {content[:2000]}  # Using the first part of the content to keep prompt size reasonable
        
        Format your response as:
        
        KEYWORDS: keyword1, keyword2, keyword3, etc.
        
        META DESCRIPTION: Your 155-character meta description here
        
        TITLE SUGGESTIONS:
        1. First title suggestion
        2. Second title suggestion
        3. Third title suggestion
        """
        
        system_prompt = """You are an SEO expert specializing in creating highly optimized content elements. 
        Focus on relevance, search intent, and strategic keyword placement. Ensure meta descriptions
        are compelling and under 155 characters. Title suggestions should be attention-grabbing 
        while incorporating primary keywords."""
        
        result = self.ai_service.generate_content(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=800
        )
        
        # Parse the SEO elements
        keywords = []
        meta_description = ""
        title_suggestions = []
        
        keyword_match = re.search(r'KEYWORDS:\s*(.+?)\s*(?:\n|$)', result)
        if keyword_match:
            keywords_text = keyword_match.group(1)
            keywords = [kw.strip() for kw in keywords_text.split(',')]
        
        meta_match = re.search(r'META DESCRIPTION:\s*(.+?)\s*(?:\n|$)', result)
        if meta_match:
            meta_description = meta_match.group(1).strip()
        
        title_section = re.search(r'TITLE SUGGESTIONS:[\s\S]+', result)
        if title_section:
            title_text = title_section.group(0)
            title_matches = re.findall(r'\d+\.\s*(.+?)\s*(?:\n|$)', title_text)
            title_suggestions = [title.strip() for title in title_matches]
        
        # Store the SEO elements in project data
        self.project_data["seo"] = {
            "keywords": keywords,
            "meta_description": meta_description,
            "title_suggestions": title_suggestions
        }
        
        # Apply the meta description to the blog post content
        if meta_description and not "Meta Description:" in self.blog_generator.current_project["full_post"]:
            current_content = self.blog_generator.current_project["full_post"]
            first_line_end = current_content.find('\n')
            if first_line_end > 0:
                # Insert the meta description after the title
                updated_content = current_content[:first_line_end+1] + f"\n**Meta Description:** {meta_description}\n" + current_content[first_line_end+1:]
                self.blog_generator.current_project["full_post"] = updated_content
        
        return self.project_data["seo"]
        
    def _export_content(self, markdown_path: str) -> str:
        """
        Export content to different formats based on user preference.
        
        Args:
            markdown_path (str): Path to the markdown file to export
            
        Returns:
            str: Path to the exported file or empty string if export failed
        """
        export_format = self.project_data["params"]["export_format"]
        content = self.blog_generator.current_project["full_post"]
        
        # Create the export path with appropriate extension
        export_path = Path(markdown_path)
        base_path = export_path.parent / export_path.stem
        
        if export_format == "html":
            # Convert markdown to HTML
            try:
                html_content = self._markdown_to_html(content)
                html_path = f"{base_path}.html"
                
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                    
                print(f"Exported HTML content to: {html_path}")
                return html_path
            except Exception as e:
                print(f"Error exporting to HTML: {e}")
                return ""
                
        elif export_format == "pdf":
            # For PDF export, we would typically use a library like weasyprint or pdfkit
            # For this implementation, we'll just create a wrapper HTML file with a note about PDF conversion
            try:
                html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{self.project_data['topic']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #444; margin-top: 20px; }}
        p {{ margin-bottom: 15px; }}
    </style>
</head>
<body>
    <div class="pdf-note" style="background: #f8f9fa; padding: 15px; margin-bottom: 20px; border-left: 4px solid #007bff;">
        <p><strong>PDF Export Note:</strong> A full PDF export implementation would use a library like WeasyPrint, pdfkit, or reportlab.</p>
    </div>
    {self._markdown_to_html(content)}
</body>
</html>"""
                
                html_path = f"{base_path}_for_pdf.html"
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                    
                print(f"Exported PDF-ready HTML content to: {html_path}")
                print("Note: To complete PDF conversion, install a PDF library like WeasyPrint or use a browser's print-to-PDF feature.")
                return html_path
            except Exception as e:
                print(f"Error preparing PDF export: {e}")
                return ""
        
        # If format is markdown or unrecognized, return empty string
        return ""
    
    def _markdown_to_html(self, markdown_content: str) -> str:
        """
        Convert markdown content to HTML.
        
        Args:
            markdown_content (str): Markdown content to convert
            
        Returns:
            str: HTML content
        """
        # Simple markdown to HTML conversion
        # In a real implementation, use a library like markdown or markdownify
        
        # Replace headers
        html = re.sub(r'# (.+?)\n', r'<h1>\1</h1>\n', markdown_content)
        html = re.sub(r'## (.+?)\n', r'<h2>\1</h2>\n', html)
        html = re.sub(r'### (.+?)\n', r'<h3>\1</h3>\n', html)
        
        # Replace emphasis
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        
        # Replace lists
        html = re.sub(r'^- (.+?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        
        # Replace paragraphs (simple approach)
        html = re.sub(r'\n\n(.+?)\n\n', r'\n<p>\1</p>\n\n', html)
        
        # Add basic HTML structure
        html = f"""<div class="blog-content">
{html}
</div>"""
        
        return html


if __name__ == "__main__":
    main()
