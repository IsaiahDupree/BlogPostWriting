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
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Store original request for reference
            self.project_data["client_request"] = {"file_path": file_path, "content": content}
            
            # Extract topic (assumed to be in format "Topic: <topic>")
            topic_match = re.search(r'\bTopic\s*:\s*(.+)\n', content, re.IGNORECASE)
            if topic_match:
                self.project_data["topic"] = topic_match.group(1).strip()
            
            # Extract competitor URLs
            competitors = []
            competitor_section = re.search(r'\bCompetitor\s+(?:URLs|Articles)\s*:\s*(.+?)(?:\n\n|\n[A-Z])', content + '\n\n', re.DOTALL | re.IGNORECASE)
            if competitor_section:
                competitor_text = competitor_section.group(1).strip()
                competitors = [url.strip() for url in re.split(r'\n-|,\s*', competitor_text) if url.strip()]
                
            self.project_data["competitor_urls"] = competitors
            
            # Extract parameters from the request
            # Content length
            length_match = re.search(r'\bContent\s+Length\s*:\s*(short|medium|long|comprehensive)\b', content, re.IGNORECASE)
            if length_match:
                self.project_data["params"]["content_length"] = length_match.group(1).lower()
            
            # Content depth
            depth_match = re.search(r'\bContent\s+Depth\s*:\s*(beginner|intermediate|advanced|expert)\b', content, re.IGNORECASE)
            if depth_match:
                self.project_data["params"]["content_depth"] = depth_match.group(1).lower()
            
            # Multimedia elements
            image_match = re.search(r'\bImages\s*:\s*(yes|no|true|false)\b', content, re.IGNORECASE)
            if image_match:
                self.project_data["params"]["include_images"] = image_match.group(1).lower() in ["yes", "true"]
                
            video_match = re.search(r'\bVideos\s*:\s*(yes|no|true|false)\b', content, re.IGNORECASE)
            if video_match:
                self.project_data["params"]["include_videos"] = video_match.group(1).lower() in ["yes", "true"]
            
            # Tone
            tone_match = re.search(r'\bTone\s*:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
            if tone_match:
                self.project_data["params"]["tone"] = tone_match.group(1).strip()
            
            # Target audience
            audience_match = re.search(r'\bTarget\s+Audience\s*:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
            if audience_match:
                self.project_data["params"]["target_audience"] = audience_match.group(1).strip()
                
            # Content format
            format_match = re.search(r'\bContent\s+Format\s*:\s*(blog|article|whitepaper)\b', content, re.IGNORECASE)
            if format_match:
                self.project_data["params"]["content_format"] = format_match.group(1).lower()
                
            # Reading level
            reading_match = re.search(r'\bReading\s+Level\s*:\s*(basic|intermediate|advanced)\b', content, re.IGNORECASE)
            if reading_match:
                self.project_data["params"]["reading_level"] = reading_match.group(1).lower()
                
            # SEO optimization
            seo_match = re.search(r'\bSEO\s+Optimization\s*:\s*(yes|no|true|false)\b', content, re.IGNORECASE)
            if seo_match:
                self.project_data["params"]["seo_optimization"] = seo_match.group(1).lower() in ["yes", "true"]
                
            # References
            references_match = re.search(r'\bReferences\s*:\s*(yes|no|true|false)\b', content, re.IGNORECASE)
            if references_match:
                self.project_data["params"]["include_references"] = references_match.group(1).lower() in ["yes", "true"]
                
            # Summary
            summary_match = re.search(r'\bSummary\s*:\s*(yes|no|true|false)\b', content, re.IGNORECASE)
            if summary_match:
                self.project_data["params"]["include_summary"] = summary_match.group(1).lower() in ["yes", "true"]
                
            # Export format
            export_match = re.search(r'\bExport\s+Format\s*:\s*(markdown|html|pdf)\b', content, re.IGNORECASE)
            if export_match:
                self.project_data["params"]["export_format"] = export_match.group(1).lower()
            
            # Generate focus areas if we have a topic but no explicit focus areas
            if self.project_data["topic"] and not self.project_data["focus_areas"]:
                self.project_data["focus_areas"] = self._generate_focus_areas(self.project_data["topic"])
            
            return self.project_data
            
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
        try:
            prompt = f"Generate 3-5 key focus areas or subtopics for a blog post about '{topic}'. Each focus area should be 3-10 words and cover an important aspect of the main topic. Return them as a comma-separated list without numbering."
            
            response = self.ai_service.text_completion(prompt)
            focus_areas = [area.strip() for area in response.split(",") if area.strip()]
            
            return focus_areas[:5]  # Limit to maximum 5 focus areas
        except Exception as e:
            print(f"Error generating focus areas: {e}")
            return []
    
    def set_parameters(self, topic: str = None, competitor_urls: List[str] = None, 
                      focus_areas: List[str] = None, content_length: str = None,
                      content_depth: str = None, include_images: bool = None,
                      include_videos: bool = None, tone: str = None,
                      target_audience: str = None, content_format: str = None,
                      reading_level: str = None, seo_optimization: bool = None,
                      include_references: bool = None, include_summary: bool = None,
                      export_format: str = None):
        """
        Set project parameters manually.
        
        Args:
            topic (str, optional): Main blog topic
            competitor_urls (List[str], optional): URLs of competing articles
            focus_areas (List[str], optional): Key areas to focus on
            content_length (str, optional): Content length (short, medium, long, comprehensive)
            content_depth (str, optional): Content depth (beginner, intermediate, advanced, expert)
            include_images (bool, optional): Whether to include image suggestions
            include_videos (bool, optional): Whether to include video suggestions
            tone (str, optional): Content tone
            target_audience (str, optional): Target audience
            content_format (str, optional): Content format (blog, article, whitepaper)
            reading_level (str, optional): Reading level (basic, intermediate, advanced)
            seo_optimization (bool, optional): Whether to optimize for SEO
            include_references (bool, optional): Whether to include references
            include_summary (bool, optional): Whether to include summary
            export_format (str, optional): Export format (markdown, html, pdf)
        """
        if topic:
            self.project_data["topic"] = topic
            
            # Generate focus areas if not provided
            if not focus_areas and not self.project_data["focus_areas"]:
                self.project_data["focus_areas"] = self._generate_focus_areas(topic)
        
        if competitor_urls is not None:
            self.project_data["competitor_urls"] = competitor_urls
            
        if focus_areas is not None:
            self.project_data["focus_areas"] = focus_areas
            
        # Update parameters if provided
        if content_length is not None:
            self.project_data["params"]["content_length"] = content_length
            
        if content_depth is not None:
            self.project_data["params"]["content_depth"] = content_depth
            
        if include_images is not None:
            self.project_data["params"]["include_images"] = include_images
            
        if include_videos is not None:
            self.project_data["params"]["include_videos"] = include_videos
            
        if tone is not None:
            self.project_data["params"]["tone"] = tone
            
        if target_audience is not None:
            self.project_data["params"]["target_audience"] = target_audience
            
        if content_format is not None:
            self.project_data["params"]["content_format"] = content_format
            
        if reading_level is not None:
            self.project_data["params"]["reading_level"] = reading_level
            
        if seo_optimization is not None:
            self.project_data["params"]["seo_optimization"] = seo_optimization
            
        if include_references is not None:
            self.project_data["params"]["include_references"] = include_references
            
        if include_summary is not None:
            self.project_data["params"]["include_summary"] = include_summary
            
        if export_format is not None:
            self.project_data["params"]["export_format"] = export_format
    
    def generate_blog(self) -> Dict:
        """
        Generate a complete blog post based on project parameters.
        
        Returns:
            Dict: Paths to generated files and project data
        """
        try:
            # Initialize basic blog generator data
            self.blog_generator.current_project = {
                "topic": self.project_data["topic"],
                "competitor_urls": self.project_data["competitor_urls"],
                "focus_areas": self.project_data["focus_areas"]
            }
            
            # Set up project configuration
            print(f"Generating blog post on '{self.project_data['topic']}'...")
            print(f"Focus areas: {', '.join(self.project_data['focus_areas'])}")
            print(f"Configuration: {json.dumps(self.project_data['params'], indent=2)}")
            
            # Perform research
            print("\nResearching topic...")
            if self.perplexity_available:
                try:
                    # Try using Perplexity for enhanced research
                    print("Using Perplexity for enhanced research...")
                    research_results = self.perplexity_service.perform_research(
                        self.project_data["topic"],
                        self.project_data["focus_areas"]
                    )
                    self.blog_generator.current_project["research"] = research_results
                except Exception as e:
                    print(f"Perplexity research failed: {e}\nFalling back to OpenAI...")
                    self._perform_openai_research()
            else:
                self._perform_openai_research()
            
            # Generate blog outline
            print("\nGenerating blog outline...")
            self._generate_blog_outline()
            
            # Generate blog sections
            print("\nGenerating blog sections...")
            self._generate_blog_sections()
            
            # Generate blog introduction
            print("\nGenerating introduction...")
            self._generate_blog_intro()
            
            # Generate blog conclusion
            print("\nGenerating conclusion...")
            self._generate_blog_conclusion()
            
            # Combine all sections
            print("\nCombining all sections...")
            self._combine_blog_sections()
            
            # Generate multimedia suggestions if enabled
            if self.project_data["params"]["include_images"] or self.project_data["params"]["include_videos"]:
                print("\nGenerating multimedia suggestions...")
                if self.project_data["params"]["include_images"]:
                    self.project_data["multimedia"]["image_suggestions"] = self._generate_image_suggestions()
                    
                if self.project_data["params"]["include_videos"]:
                    self.project_data["multimedia"]["video_suggestions"] = self._generate_video_suggestions()
                
                # Integrate multimedia suggestions into content
                self._integrate_multimedia_suggestions()
            
            # Apply reading level adjustments
            if self.project_data["params"]["reading_level"]:
                print(f"\nAdjusting content for {self.project_data['params']['reading_level']} reading level...")
                adjusted_content = self._adjust_reading_level()
                if adjusted_content:
                    self.blog_generator.current_project["full_post"] = adjusted_content
            
            # Analyze content statistics
            print("\nAnalyzing content statistics...")
            self.project_data["content_stats"] = self._analyze_content()
            print(f"Word count: {self.project_data['content_stats']['word_count']}")
            print(f"Estimated reading time: {self.project_data['reading_time']} minutes")
            
            # Generate SEO elements if enabled
            if self.project_data["params"]["seo_optimization"]:
                print("\nGenerating SEO elements...")
                self.project_data["seo"] = self._generate_seo_elements()
            
            # Generate references if enabled
            if self.project_data["params"]["include_references"]:
                print("\nGenerating references...")
                self.project_data["references"] = self._generate_references()
                
                # Add references to blog post
                if self.project_data["references"]:
                    references_md = "\n\n## References\n\n"
                    for i, ref in enumerate(self.project_data["references"]):
                        references_md += f"{i+1}. {ref['citation']}\n"
                    
                    self.blog_generator.current_project["full_post"] += references_md
            
            # Generate summary if enabled
            if self.project_data["params"]["include_summary"]:
                print("\nGenerating content summary...")
                summary_result = self._generate_summary()
                self.project_data["summary"] = summary_result
            
            # Save the blog post
            print("\nSaving blog post...")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_topic = re.sub(r'[^\w\s-]', '', self.project_data["topic"]).strip().replace(' ', '_')
            
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            markdown_path = output_dir / f"{safe_topic}_{timestamp}.md"
            
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(self.blog_generator.current_project["full_post"])
            
            print(f"\nBlog post saved to: {markdown_path}")
            
            # Export to other formats if requested
            export_path = ""
            if self.project_data["params"]["export_format"] != "markdown":
                export_path = self._export_content(markdown_path)
            
            result = {
                "markdown_path": str(markdown_path),
                "export_path": export_path,
                "project_data": self.project_data,
                "blog_generator_data": self.blog_generator.current_project
            }
            
            return result
            
        except Exception as e:
            print(f"Error generating blog: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
    
    def _perform_openai_research(self):
        """
        Perform research using the OpenAI service.
        """
        research_results = {}
        
        # Research the main topic
        main_research = self.ai_service.research_topic(
            topic=self.project_data["topic"],
            depth=self.project_data["params"]["content_depth"]
        )
        research_results["main_topic"] = main_research
        
        # Research focus areas
        focus_research = {}
        for focus in self.project_data["focus_areas"]:
            focus_research[focus] = self.ai_service.research_topic(
                topic=f"{self.project_data['topic']} - {focus}",
                depth=self.project_data["params"]["content_depth"]
            )
        
        research_results["focus_areas"] = focus_research
        
        # Research competitors if URLs provided
        if self.project_data["competitor_urls"]:
            competitor_analysis = self.ai_service.analyze_competitors(
                self.project_data["competitor_urls"],
                self.project_data["topic"]
            )
            research_results["competitor_analysis"] = competitor_analysis
        
        self.blog_generator.current_project["research"] = research_results
    
    def _generate_blog_outline(self):
        """
        Generate the blog post outline.
        """
        content_length = self.project_data["params"]["content_length"]
        content_depth = self.project_data["params"]["content_depth"]
        
        # Determine number of sections based on content length
        section_counts = {
            "short": (3, 5),  # 3-5 sections
            "medium": (5, 7),  # 5-7 sections
            "long": (7, 10),  # 7-10 sections
            "comprehensive": (10, 15)  # 10-15 sections
        }
        
        min_sections, max_sections = section_counts.get(content_length, (5, 7))
        num_sections = random.randint(min_sections, max_sections)
        
        # Get content format template
        content_format = self.project_data["params"]["content_format"]
        format_template = self.CONTENT_FORMATS.get(content_format, self.CONTENT_FORMATS["blog"])
        
        # Create prompt for outline generation
        outline_prompt = f"""Create an outline for a {content_length} {content_format} about '{self.project_data['topic']}' with {num_sections} main sections. The content should be {format_template} and appropriate for {self.project_data['params']['target_audience']} at a {content_depth} level of depth. Use the following focus areas as guidance: {', '.join(self.project_data['focus_areas'])}.

The tone should be {self.project_data['params']['tone']}.

Return the outline as a list of section titles without numbering or formatting."""
        
        outline_response = self.ai_service.text_completion(outline_prompt)
        
        # Parse the outline into a list of sections
        sections = [section.strip() for section in outline_response.split("\n") if section.strip()]
        
        # Remove any numbering or bullets that might be present
        sections = [re.sub(r'^\d+\.\s*|^-\s*|^\*\s*', '', section) for section in sections]
        
        # Store the outline
        self.blog_generator.current_project["outline"] = sections
    
    def _generate_blog_sections(self):
        """
        Generate the content for each section in the outline.
        """
        # Get parameters for content generation
        content_length = self.project_data["params"]["content_length"]
        content_depth = self.project_data["params"]["content_depth"]
        target_audience = self.project_data["params"]["target_audience"]
        tone = self.project_data["params"]["tone"]
        
        # Determine word count per section based on content length
        word_counts = {
            "short": (150, 250),  # 150-250 words per section
            "medium": (250, 400),  # 250-400 words per section
            "long": (400, 600),  # 400-600 words per section
            "comprehensive": (600, 900)  # 600-900 words per section
        }
        
        min_words, max_words = word_counts.get(content_length, (300, 500))
        
        # Get content format template
        content_format = self.project_data["params"]["content_format"]
        format_template = self.CONTENT_FORMATS.get(content_format, self.CONTENT_FORMATS["blog"])
        
        # Generate content for each section
        sections_content = {}
        research = self.blog_generator.current_project.get("research", {})
        
        for section_title in self.blog_generator.current_project["outline"]:
            # Find most relevant research for this section
            relevant_research = ""
            
            # Check main topic research
            if "main_topic" in research:
                relevant_research += research["main_topic"] + "\n\n"
            
            # Check focus area research
            if "focus_areas" in research:
                # Find most relevant focus area for this section
                most_relevant_focus = None
                highest_relevance = 0
                
                for focus, focus_research in research["focus_areas"].items():
                    # Simple relevance scoring by word overlap
                    focus_words = set(focus.lower().split())
                    section_words = set(section_title.lower().split())
                    relevance = len(focus_words.intersection(section_words))
                    
                    if relevance > highest_relevance:
                        highest_relevance = relevance
                        most_relevant_focus = focus
                
                if most_relevant_focus and most_relevant_focus in research["focus_areas"]:
                    relevant_research += research["focus_areas"][most_relevant_focus]
            
            # Generate section content
            target_words = random.randint(min_words, max_words)
            
            section_prompt = f"""Write a {target_words}-word section for a {content_format} about '{self.project_data['topic']}' with the section title '{section_title}'.

The content should be {format_template} and appropriate for {target_audience} at a {content_depth} level of depth. The tone should be {tone}.

Use the following research as reference if helpful: {relevant_research}

Write the content in markdown format without including the section title (as it will be added separately). Do not include any introduction or conclusion statements about the section itself."""
            
            section_content = self.ai_service.text_completion(section_prompt)
            sections_content[section_title] = section_content.strip()
        
        # Store the sections
        self.blog_generator.current_project["sections"] = sections_content
    
    def _generate_blog_intro(self):
        """
        Generate the introduction for the blog post.
        """
        content_format = self.project_data["params"]["content_format"]
        format_template = self.CONTENT_FORMATS.get(content_format, self.CONTENT_FORMATS["blog"])
        target_audience = self.project_data["params"]["target_audience"]
        tone = self.project_data["params"]["tone"]
        
        outline_str = "\n".join([f"- {section}" for section in self.blog_generator.current_project["outline"]])
        
        intro_prompt = f"""Write an engaging introduction for a {content_format} about '{self.project_data['topic']}'. The content should be {format_template} and appropriate for {target_audience}. The tone should be {tone}.

The blog will cover the following sections:\n{outline_str}

Write the introduction in markdown format. It should be attention-grabbing, establish the importance of the topic, and briefly outline what the reader will learn, without explicitly listing the sections. The introduction should be approximately 150-200 words."""
        
        intro_content = self.ai_service.text_completion(intro_prompt)
        
        # Store the introduction
        self.blog_generator.current_project["introduction"] = intro_content.strip()
    
    def _generate_blog_conclusion(self):
        """
        Generate the conclusion for the blog post.
        """
        content_format = self.project_data["params"]["content_format"]
        format_template = self.CONTENT_FORMATS.get(content_format, self.CONTENT_FORMATS["blog"])
        target_audience = self.project_data["params"]["target_audience"]
        tone = self.project_data["params"]["tone"]
        
        # Create a summary of the main points
        main_points = "\n".join([f"- {section}" for section in self.blog_generator.current_project["outline"]])
        
        conclusion_prompt = f"""Write a conclusion for a {content_format} about '{self.project_data['topic']}'. The content should be {format_template} and appropriate for {target_audience}. The tone should be {tone}.

The blog covered these main sections:\n{main_points}

Write the conclusion in markdown format. It should summarize the key points, provide final thoughts, and possibly include a call to action or recommendations for further reading or next steps. The conclusion should be approximately 150-200 words."""
        
        conclusion_content = self.ai_service.text_completion(conclusion_prompt)
        
        # Store the conclusion
        self.blog_generator.current_project["conclusion"] = conclusion_content.strip()
    
    def _combine_blog_sections(self):
        """
        Combine all blog sections into a complete post.
        """
        # Create title
        title = f"# {self.project_data['topic']}"
        
        # Add introduction
        introduction = self.blog_generator.current_project["introduction"]
        
        # Add sections with headings
        sections_content = ""
        for section_title, section_content in self.blog_generator.current_project["sections"].items():
            sections_content += f"\n\n## {section_title}\n\n{section_content}"
        
        # Add conclusion
        conclusion = f"\n\n## Conclusion\n\n{self.blog_generator.current_project['conclusion']}"
        
        # Combine all parts
        full_post = f"{title}\n\n{introduction}{sections_content}{conclusion}"
        
        # Store the full post
        self.blog_generator.current_project["full_post"] = full_post
    
    def _generate_image_suggestions(self) -> List[Dict]:
        """
        Generate suggestions for images to include in the blog post.
        
        Returns:
            List[Dict]: Image suggestions with descriptions and placement
        """
        topic = self.project_data["topic"]
        content_format = self.project_data["params"]["content_format"]
        outline = self.blog_generator.current_project.get("outline", [])
        
        # Determine number of image suggestions based on content format and length
        content_length = self.project_data["params"]["content_length"]
        num_images = {
            "short": 1,
            "medium": 2,
            "long": 3,
            "comprehensive": 5
        }.get(content_length, 2)
        
        # Generate image suggestions
        prompt = f"""Suggest {num_images} images that would enhance a {content_format} about '{topic}'.

For each image, provide:
1. A detailed description
2. The purpose it serves
3. Where in the content it would be best placed (after which section)
4. Any specific style recommendations

Return your suggestions as a list of {num_images} distinct image ideas, each with the above attributes. Be specific and creative."""
        
        response = self.ai_service.text_completion(prompt)
        
        # Parse the response into structured image suggestions
        # For simplicity, we'll extract each image suggestion and parse it
        image_suggestions = []
        
        # Simple parser for the AI response
        image_blocks = re.split(r'\n\s*\d+\.\s*|\n\s*Image\s*\d+:\s*', response)
        image_blocks = [block.strip() for block in image_blocks if block.strip()]
        
        for i, block in enumerate(image_blocks[:num_images]):
            lines = block.split('\n')
            
            # Extract description
            description = lines[0] if lines else f"Image related to {topic}"
            
            # Extract purpose and placement
            purpose = ""
            placement = ""
            style = ""
            
            for line in lines[1:]:
                if re.search(r'purpose|serves|function', line, re.IGNORECASE):
                    purpose = line
                elif re.search(r'placement|place|location|after|section', line, re.IGNORECASE):
                    placement = line
                elif re.search(r'style|design|aesthetic', line, re.IGNORECASE):
                    style = line
            
            # Determine the section to place after
            target_section = ""
            if outline:
                # If we have specific placement information, try to match it to a section
                if placement:
                    for section in outline:
                        if any(word in section.lower() for word in placement.lower().split()):
                            target_section = section
                            break
                
                # If no match found, distribute evenly through the content
                if not target_section:
                    idx = min(i, len(outline) - 1)
                    target_section = outline[idx]
            
            image_suggestions.append({
                "description": description,
                "purpose": purpose,
                "placement": target_section,
                "style": style,
                "suggested_alt_text": re.sub(r'[^\w\s]', '', description).strip()
            })
        
        return image_suggestions
    
    def _generate_video_suggestions(self) -> List[Dict]:
        """
        Generate suggestions for videos to embed in the blog post.
        
        Returns:
            List[Dict]: Video suggestions with topics and placement
        """
        topic = self.project_data["topic"]
        content_format = self.project_data["params"]["content_format"]
        outline = self.blog_generator.current_project.get("outline", [])
        
        # Determine number of video suggestions based on content format and length
        content_length = self.project_data["params"]["content_length"]
        num_videos = {
            "short": 0,
            "medium": 1,
            "long": 1,
            "comprehensive": 2
        }.get(content_length, 1)
        
        if num_videos == 0:
            return []
        
        # Generate video suggestions
        prompt = f"""Suggest {num_videos} videos that would enhance a {content_format} about '{topic}'.

For each video:
1. Suggest a specific topic/focus
2. Explain why it would be valuable to the reader
3. Suggest where in the content it should be placed
4. Estimate an ideal duration
5. Suggest possible sources (YouTube, etc.)

Be specific and ensure each video suggestion directly relates to the content."""
        
        response = self.ai_service.text_completion(prompt)
        
        # Parse the response into structured video suggestions
        video_suggestions = []
        
        # Simple parser for the AI response
        video_blocks = re.split(r'\n\s*\d+\.\s*|\n\s*Video\s*\d+:\s*', response)
        video_blocks = [block.strip() for block in video_blocks if block.strip()]
        
        for i, block in enumerate(video_blocks[:num_videos]):
            lines = block.split('\n')
            
            # Extract topic
            topic_focus = lines[0] if lines else f"Video about {topic}"
            
            # Extract other information
            value = ""
            placement = ""
            duration = ""
            source = ""
            
            for line in lines[1:]:
                if re.search(r'value|benefit|why', line, re.IGNORECASE):
                    value = line
                elif re.search(r'placement|place|location|after|section', line, re.IGNORECASE):
                    placement = line
                elif re.search(r'duration|length|time', line, re.IGNORECASE):
                    duration = line
                elif re.search(r'source|platform|youtube|vimeo', line, re.IGNORECASE):
                    source = line
            
            # Determine the section to place after
            target_section = ""
            if outline:
                # If we have specific placement information, try to match it to a section
                if placement:
                    for section in outline:
                        if any(word in section.lower() for word in placement.lower().split()):
                            target_section = section
                            break
                
                # If no match found, distribute evenly through the content
                if not target_section:
                    idx = min(i, len(outline) - 1)
                    target_section = outline[idx]
            
            video_suggestions.append({
                "topic": topic_focus,
                "value": value,
                "placement": target_section,
                "duration": duration,
                "source": source
            })
        
        return video_suggestions
    
    def _integrate_multimedia_suggestions(self):
        """
        Integrate multimedia suggestions into the blog post content.
        """
        if not self.blog_generator.current_project.get("full_post"):
            return
        
        content = self.blog_generator.current_project["full_post"]
        modified_content = content
        
        # Helper function to insert after a heading
        def insert_after_heading(content, heading, marker):
            pattern = f"## {re.escape(heading)}\n\n"
            if pattern in content:
                return content.replace(pattern, f"## {heading}\n\n{marker}\n\n")
            return content
        
        # Insert image suggestions
        image_suggestions = self.project_data["multimedia"]["image_suggestions"]
        for i, img in enumerate(image_suggestions):
            placement = img.get("placement", "")
            if placement:
                image_marker = f"<!-- Image suggestion {i+1}: {img['description']} -->\n**Suggested image:** {img['description']}"  
                if img.get("purpose"):
                    image_marker += f"\n**Purpose:** {img['purpose']}"
                if img.get("style"):
                    image_marker += f"\n**Style:** {img['style']}"
                
                modified_content = insert_after_heading(modified_content, placement, image_marker)
        
        # Insert video suggestions
        video_suggestions = self.project_data["multimedia"]["video_suggestions"]
        for i, vid in enumerate(video_suggestions):
            placement = vid.get("placement", "")
            if placement:
                video_marker = f"<!-- Video suggestion {i+1}: {vid['topic']} -->\n**Suggested video:** {vid['topic']}"  
                if vid.get("value"):
                    video_marker += f"\n**Value:** {vid['value']}"
                if vid.get("duration"):
                    video_marker += f"\n**Duration:** {vid['duration']}"
                if vid.get("source"):
                    video_marker += f"\n**Source:** {vid['source']}"
                
                modified_content = insert_after_heading(modified_content, placement, video_marker)
        
        # Update the content
        if modified_content != content:
            self.blog_generator.current_project["full_post"] = modified_content
    
    def _analyze_content(self) -> Dict:
        """
        Analyze content to extract statistics and calculate reading time.
        
        Returns:
            Dict: Content statistics
        """
        content = self.blog_generator.current_project.get("full_post", "")
        
        if not content:
            return {
                "word_count": 0,
                "sentence_count": 0,
                "paragraph_count": 0,
                "reading_level_score": 0
            }
        
        # Count words
        words = re.findall(r'\b\w+\b', content)
        word_count = len(words)
        
        # Count sentences using simple heuristic
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)
        
        # Count paragraphs
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        paragraph_count = len(paragraphs)
        
        # Calculate average sentence length
        if sentence_count > 0:
            avg_sentence_length = word_count / sentence_count
        else:
            avg_sentence_length = 0
        
        # Calculate syllable count for a sample of words
        sample_size = min(100, len(words))
        sample_words = random.sample(words, sample_size) if sample_size > 0 else []
        syllable_count = sum(self._count_syllables(word) for word in sample_words)
        
        # Calculate simplified reading level score (based on Flesch-Kincaid)
        if sample_size > 0 and sentence_count > 0:
            avg_syllables_per_word = syllable_count / sample_size
            reading_level_score = 0.39 * (avg_sentence_length) + 11.8 * (avg_syllables_per_word) - 15.59
        else:
            reading_level_score = 0
        
        # Calculate estimated reading time (average reading speed: 200-250 words per minute)
        reading_time = math.ceil(word_count / 225)  # rounded up to the nearest minute
        self.project_data["reading_time"] = reading_time
        
        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count,
            "reading_level_score": round(reading_level_score, 2)
        }
    
    def _count_syllables(self, word: str) -> int:
        """
        Count the number of syllables in a word (simplified approach).
        
        Args:
            word (str): Word to count syllables for
            
        Returns:
            int: Estimated syllable count
        """
        word = word.lower()
        
        # Remove non-alpha characters
        word = re.sub(r'[^a-z]', '', word)
        
        if not word:
            return 0
            
        # Special cases
        if len(word) <= 3:
            return 1
            
        # Count vowel groups
        count = 0
        vowels = "aeiouy"
        prev_is_vowel = False
        
        for i, char in enumerate(word):
            is_vowel = char in vowels
            
            # Count vowel groups (consecutive vowels count as one syllable)
            if is_vowel and not prev_is_vowel:
                count += 1
                
            prev_is_vowel = is_vowel
            
        # Handle silent e at the end
        if word.endswith('e') and len(word) > 2 and word[-2] not in vowels:
            count -= 1
            
        # Ensure at least one syllable
        return max(1, count)
    
    def _adjust_reading_level(self) -> str:
        """
        Adjust the content's reading level based on the target audience.
        
        Returns:
            str: Adjusted content
        """
        content = self.blog_generator.current_project.get("full_post", "")
        reading_level = self.project_data["params"]["reading_level"]
        
        if not content or not reading_level:
            return content
        
        # Get reading level guidelines
        reading_level_template = self.READING_LEVELS.get(reading_level, self.READING_LEVELS["intermediate"])
        
        # Check current reading level from content stats
        current_stats = self.project_data.get("content_stats", {})
        current_score = current_stats.get("reading_level_score", 0)
        
        # Determine target scores based on reading level
        target_scores = {
            "basic": (5, 8),       # Grade 5-8 level
            "intermediate": (9, 12),  # Grade 9-12 level
            "advanced": (13, 18)    # College/Graduate level
        }
        
        target_min, target_max = target_scores.get(reading_level, (9, 12))
        
        # Only adjust if the current score is significantly different from the target range
        if target_min <= current_score <= target_max:
            return content  # Already in the correct range
        
        # Create prompt for content adjustment
        prompt = f"""Rewrite the following content to adjust its reading level to be {reading_level} ({reading_level_template}).

The current reading level score is approximately {current_score}, and the target range is {target_min}-{target_max}.

Maintain all the original information and structure, including headings, but adjust vocabulary, sentence complexity, and explanation depth to match the target reading level. Return the entire content with the adjusted reading level.

Here's the content to adjust:

{content}"""
        
        try:
            adjusted_content = self.ai_service.text_completion(prompt)
            return adjusted_content
        except Exception as e:
            print(f"Error adjusting reading level: {e}")
            return content  # Return original content if adjustment fails
    
    def _generate_references(self) -> List[Dict]:
        """
        Generate references and citations for the blog post.
        
        Returns:
            List[Dict]: List of references with citation information
        """
        topic = self.project_data["topic"]
        content = self.blog_generator.current_project.get("full_post", "")
        research = self.blog_generator.current_project.get("research", {})
        
        if not content:
            return []
        
        # Determine number of references based on content length
        content_length = self.project_data["params"]["content_length"]
        num_references = {
            "short": 3,
            "medium": 5,
            "long": 8,
            "comprehensive": 12
        }.get(content_length, 5)
        
        # Extract potential sources from research
        potential_sources = []
        
        # Get competitor URLs if available
        if self.project_data["competitor_urls"]:
            potential_sources.extend(self.project_data["competitor_urls"])
        
        # Try to extract URLs from research content
        if "competitor_analysis" in research:
            comp_analysis = research["competitor_analysis"]
            urls = re.findall(r'https?://[^\s)"]+', comp_analysis)
            potential_sources.extend(urls)
        
        # Generate prompt for reference creation
        prompt = f"""Generate {num_references} academic-style references for a blog post on '{topic}'.

For each reference, provide:
1. A realistic title
2. Author name(s)
3. Publication/source name
4. Year published (between 2015 and 2023)
5. URL (if applicable)
6. A proper citation in APA format

Make the references diverse but relevant to the topic. If the following potential sources seem relevant, you may incorporate some of them: {', '.join(potential_sources[:5])}.

Format each reference as a JSON-like structure, numbered from 1 to {num_references}."""
        
        try:
            response = self.ai_service.text_completion(prompt)
            
            # Parse the response to extract references
            references = []
            
            # Split the response into individual references
            ref_blocks = re.split(r'\n\s*\d+\.\s*|\n\s*Reference\s*\d+:\s*', response)
            ref_blocks = [block.strip() for block in ref_blocks if block.strip()]
            
            for i, block in enumerate(ref_blocks[:num_references]):
                lines = block.split('\n')
                
                ref = {
                    "id": i + 1,
                    "title": "",
                    "authors": "",
                    "source": "",
                    "year": "",
                    "url": "",
                    "citation": ""
                }
                
                # Extract information from the reference block
                for line in lines:
                    line = line.strip()
                    if re.search(r'^title:|^title[^:]*:', line, re.IGNORECASE):
                        ref["title"] = re.sub(r'^title:|^title[^:]*:', '', line, flags=re.IGNORECASE).strip()
                    elif re.search(r'^author|^authors:', line, re.IGNORECASE):
                        ref["authors"] = re.sub(r'^author[^:]*:', '', line, flags=re.IGNORECASE).strip()
                    elif re.search(r'^source|^publication:', line, re.IGNORECASE):
                        ref["source"] = re.sub(r'^source:|^publication:', '', line, flags=re.IGNORECASE).strip()
                    elif re.search(r'^year:', line, re.IGNORECASE):
                        year_match = re.search(r'\b(19|20)\d{2}\b', line)
                        if year_match:
                            ref["year"] = year_match.group(0)
                    elif re.search(r'^url:|^link:', line, re.IGNORECASE):
                        url_match = re.search(r'https?://[^\s)"]+', line)
                        if url_match:
                            ref["url"] = url_match.group(0)
                    elif re.search(r'^citation|^apa:', line, re.IGNORECASE):
                        ref["citation"] = re.sub(r'^citation:|^apa:', '', line, flags=re.IGNORECASE).strip()
                
                # If no explicit citation was found, construct a basic one
                if not ref["citation"] and ref["authors"] and ref["title"] and ref["year"]:
                    if ref["url"]:
                        ref["citation"] = f"{ref['authors']} ({ref['year']}). {ref['title']}. {ref['source']}. {ref['url']}"
                    else:
                        ref["citation"] = f"{ref['authors']} ({ref['year']}). {ref['title']}. {ref['source']}."
                
                if ref["citation"]:
                    references.append(ref)
            
            return references
            
        except Exception as e:
            print(f"Error generating references: {e}")
            return []
    
    def _generate_summary(self) -> Dict:
        """
        Generate a concise summary of the blog post content.
        
        Returns:
            Dict: Different types of summaries
        """
        content = self.blog_generator.current_project.get("full_post", "")
        topic = self.project_data["topic"]
        
        if not content:
            return {}
        
        # Generate executive summary
        exec_prompt = f"""Create a concise executive summary of the following blog post about '{topic}'.

The summary should be approximately 150-200 words and capture the key points and insights from the post.

Blog post content:
{content[:2000]}..."""
        
        # Generate social media summary
        social_prompt = f"""Create 3 engaging social media posts (Twitter/X, LinkedIn, and Facebook) to promote a blog post about '{topic}'.

For each platform:
1. Keep within character limits (280 for Twitter, ~1200 for LinkedIn, ~500 for Facebook)
2. Use appropriate tone and hashtags
3. Include a compelling call-to-action

Blog post content:
{content[:1000]}..."""
        
        # Generate email newsletter summary
        email_prompt = f"""Create an email newsletter blurb (200-250 words) to promote a blog post about '{topic}'.

Include:
1. An attention-grabbing subject line
2. Brief introduction that highlights the value
3. 2-3 key points from the blog
4. Clear call-to-action

Blog post content:
{content[:1500]}..."""
        
        try:
            # Generate all summaries in parallel (in a real implementation)
            # For simplicity, we'll do them sequentially
            exec_summary = self.ai_service.text_completion(exec_prompt)
            social_posts = self.ai_service.text_completion(social_prompt)
            email_blurb = self.ai_service.text_completion(email_prompt)
            
            return {
                "executive_summary": exec_summary.strip(),
                "social_media_posts": social_posts.strip(),
                "email_newsletter": email_blurb.strip()
            }
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return {}
    
    def _generate_seo_elements(self) -> Dict:
        """
        Generate SEO elements for the blog post.
        
        Returns:
            Dict: SEO elements including keywords, meta description, and title suggestions
        """
        topic = self.project_data["topic"]
        content = self.blog_generator.current_project["full_post"]
        
        prompt = f"""For a blog post about "{topic}", generate comprehensive SEO elements:

1. Primary keyword
2. 10 related long-tail keywords (with search volume estimates)
3. 3 alternative title suggestions optimized for SEO
4. Meta description (under 160 characters)
5. 5 suggested H2 subheadings that incorporate keywords

Analyze the following content to extract the most relevant SEO elements:

{content[:1500]}..."""
        
        try:
            response = self.ai_service.text_completion(prompt)
            
            # Parse the response to extract SEO elements
            seo_elements = {
                "keywords": [],
                "meta_description": "",
                "title_suggestions": [],
                "suggested_headings": []
            }
            
            # Extract primary keyword
            primary_match = re.search(r'(?:primary|main)\s+keyword[^:]*:\s*(.+?)(?:\n|$)', response, re.IGNORECASE)
            if primary_match:
                seo_elements["keywords"].append({"keyword": primary_match.group(1).strip(), "primary": True})
            
            # Extract long-tail keywords
            longtail_section = re.search(r'(?:related|long.?tail)\s+keywords?[^:]*:(.+?)(?:\n\s*\d+\.|\n\s*[A-Za-z])', response + '\n A', re.DOTALL | re.IGNORECASE)
            if longtail_section:
                lt_text = longtail_section.group(1).strip()
                lt_keywords = re.findall(r'(?:\d+\.\s*|-)\s*(.+?)(?:\s*\([^)]+\)|\s*–|\s*-|\s*:|\n|$)', lt_text)
                
                for kw in lt_keywords:
                    # Extract volume if available
                    volume_match = re.search(r'\(([^)]+)\)', kw)
                    volume = volume_match.group(1) if volume_match else ""
                    
                    # Clean up keyword
                    clean_kw = re.sub(r'\([^)]+\)', '', kw).strip()
                    
                    if clean_kw:
                        seo_elements["keywords"].append({"keyword": clean_kw, "volume": volume, "primary": False})
            
            # Extract meta description
            meta_match = re.search(r'meta\s+description[^:]*:\s*(.+?)(?:\n|$)', response, re.IGNORECASE)
            if meta_match:
                seo_elements["meta_description"] = meta_match.group(1).strip()[:160]  # Limit to 160 chars
            
            # Extract title suggestions
            title_section = re.search(r'title\s+suggestions?[^:]*:(.+?)(?:\n\s*\d+\.|\n\s*[A-Za-z])', response + '\n A', re.DOTALL | re.IGNORECASE)
            if title_section:
                title_text = title_section.group(1).strip()
                titles = re.findall(r'(?:\d+\.\s*|-)\s*(.+?)(?:\n|$)', title_text)
                seo_elements["title_suggestions"] = [title.strip() for title in titles if title.strip()]
            
            # Extract suggested headings
            heading_section = re.search(r'(?:suggested|h2)\s+(?:sub)?headings?[^:]*:(.+?)(?:\n\s*\d+\.|\n\s*[A-Za-z])', response + '\n A', re.DOTALL | re.IGNORECASE)
            if heading_section:
                heading_text = heading_section.group(1).strip()
                headings = re.findall(r'(?:\d+\.\s*|-)\s*(.+?)(?:\n|$)', heading_text)
                seo_elements["suggested_headings"] = [heading.strip() for heading in headings if heading.strip()]
            
            return seo_elements
            
        except Exception as e:
            print(f"Error generating SEO elements: {e}")
            return {
                "keywords": [],
                "meta_description": "",
                "title_suggestions": [],
                "suggested_headings": []
            }
    
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
    parser.add_argument("--format", choices=["blog", "article", "whitepaper"], help="Content format")
    parser.add_argument("--reading-level", choices=["basic", "intermediate", "advanced"], help="Reading level")
    parser.add_argument("--no-seo", action="store_true", help="Disable SEO optimization")
    parser.add_argument("--references", action="store_true", help="Include references")
    parser.add_argument("--summary", action="store_true", help="Include summary")
    parser.add_argument("--export", choices=["markdown", "html", "pdf"], help="Export format")
    
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
        
    if args.format:
        params["content_format"] = args.format
        
    if args.reading_level:
        params["reading_level"] = args.reading_level
        
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
    
    # Generate blog post
    if generator.project_data["topic"]:
        generator.generate_blog()
    else:
        print("Error: No topic specified. Please provide either a client request file or a topic.")

if __name__ == "__main__":
    main()
