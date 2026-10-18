"""
Blog Post Generator module that coordinates the overall content creation workflow.
"""
import json
import os
from ai_service import AIService
from perplexity_service import PerplexityService

class BlogPostGenerator:
    """Main class for generating blog posts with AI assistance."""
    
    def __init__(self):
        """Initialize the blog post generator."""
        self.ai_service = AIService()
        try:
            self.perplexity_service = PerplexityService()
            self.perplexity_available = True
        except ValueError:
            # If Perplexity API key is not available, continue without it
            self.perplexity_available = False
            print("Perplexity API not available. Using OpenAI for all research tasks.")
            
        self.current_project = {
            "topic": "",
            "research": "",
            "outline": "",
            "sections": {},
            "full_post": "",
            "meta": {
                "title": "",
                "meta_description": "",
                "keywords": [],
                "target_audience": "",
                "tone": "authoritative and educational"
            }
        }
    
    def create_new_project(self, topic, target_audience=None, tone=None):
        """
        Create a new blog post project.
        
        Args:
            topic (str): The main topic for the blog post
            target_audience (str): The intended audience for the content
            tone (str): Desired tone for the content
        """
        self.current_project = {
            "topic": topic,
            "research": "",
            "outline": "",
            "sections": {},
            "full_post": "",
            "meta": {
                "title": "",
                "meta_description": "",
                "keywords": [],
                "target_audience": target_audience or "",
                "tone": tone or "authoritative and educational"
            }
        }
        return self.current_project
    
    def conduct_research(self, competitor_urls=None, focus_areas=None, use_perplexity=True):
        """
        Conduct research for the current project.
        
        Args:
            competitor_urls (list): List of competitor article URLs
            focus_areas (list): Specific areas to focus research on
            use_perplexity (bool): Whether to use Perplexity API for research if available
            
        Returns:
            str: Research findings
        """
        if not self.current_project["topic"]:
            raise ValueError("No active project. Please create a new project first.")
        
        # Use Perplexity API for research if available and requested
        if use_perplexity and self.perplexity_available:
            try:
                print("Using Perplexity API for enhanced research...")
                research_data = self.perplexity_service.research_topic(
                    self.current_project["topic"],
                    focus_areas,
                    competitor_urls
                )
                
                # Get latest trends as additional research
                try:
                    latest_trends = self.perplexity_service.get_latest_trends(self.current_project["topic"])
                    research_data += "\n\n## LATEST TRENDS AND DEVELOPMENTS\n" + latest_trends
                except Exception as e:
                    print(f"Error getting latest trends: {e}")
                
                # Get SEO keywords as additional research
                try:
                    seo_keywords = self.perplexity_service.generate_seo_keywords(self.current_project["topic"])
                    research_data += "\n\n## SEO KEYWORDS AND SEARCH INSIGHTS\n" + seo_keywords
                except Exception as e:
                    print(f"Error generating SEO keywords: {e}")
                
                # Competitor analysis if URLs provided
                if competitor_urls and len(competitor_urls) > 0:
                    try:
                        competitor_analysis = self.perplexity_service.analyze_competitors(
                            competitor_urls,
                            self.current_project["topic"]
                        )
                        research_data += "\n\n## COMPETITOR ANALYSIS\n" + competitor_analysis
                    except Exception as e:
                        print(f"Error analyzing competitors: {e}")
                
                self.current_project["research"] = research_data
                return self.current_project["research"]
            except Exception as e:
                print(f"Error using Perplexity API: {e}. Falling back to OpenAI.")
                # Fall back to OpenAI if Perplexity fails
        
        # Use OpenAI for research if Perplexity is not available or failed
        print("Using OpenAI for research...")
        self.current_project["research"] = self.ai_service.conduct_research(
            self.current_project["topic"],
            competitor_urls,
            focus_areas
        )
        return self.current_project["research"]
    
    def generate_outline(self):
        """
        Generate an outline based on research.
        
        Returns:
            str: Generated outline
        """
        if not self.current_project["research"]:
            raise ValueError("No research data. Please conduct research first.")
        
        self.current_project["outline"] = self.ai_service.generate_outline(
            self.current_project["topic"],
            self.current_project["research"],
            self.current_project["meta"]["target_audience"],
            self.current_project["meta"]["tone"]
        )
        
        # Try to extract meta information from the outline
        try:
            lines = self.current_project["outline"].split('\n')
            for i, line in enumerate(lines):
                if "title:" in line.lower() or "title :" in line.lower():
                    self.current_project["meta"]["title"] = line.split(':', 1)[1].strip()
                if "meta description:" in line.lower() or "meta description :" in line.lower():
                    self.current_project["meta"]["meta_description"] = line.split(':', 1)[1].strip()
                if "keywords:" in line.lower() or "keywords :" in line.lower():
                    keyword_text = line.split(':', 1)[1].strip()
                    self.current_project["meta"]["keywords"] = [k.strip() for k in keyword_text.split(',')]
        except Exception as e:
            print(f"Error extracting meta information: {e}")
        
        return self.current_project["outline"]
    
    def extract_sections_from_outline(self):
        """
        Extract section titles and descriptions from the outline.
        
        Returns:
            dict: Dictionary of section titles and descriptions
        """
        if not self.current_project["outline"]:
            raise ValueError("No outline. Please generate an outline first.")
        
        # Simple extraction logic - can be enhanced for better accuracy
        sections = {}
        current_section = None
        description_lines = []
        
        lines = self.current_project["outline"].split('\n')
        for line in lines:
            line = line.strip()
            # Look for H2 headings (## Section Title)
            if line.startswith('## '):
                # Save previous section if exists
                if current_section:
                    sections[current_section] = '\n'.join(description_lines).strip()
                    description_lines = []
                
                current_section = line.replace('## ', '').strip()
            # If we have a current section, add description lines
            elif current_section and line and not line.startswith('#'):
                description_lines.append(line)
        
        # Add the last section
        if current_section and description_lines:
            sections[current_section] = '\n'.join(description_lines).strip()
        
        self.current_project["sections"] = {
            title: {"description": desc, "content": ""} 
            for title, desc in sections.items()
        }
        
        return self.current_project["sections"]
    
    def generate_section_content(self, section_title):
        """
        Generate content for a specific section.
        
        Args:
            section_title (str): The title of the section
            
        Returns:
            str: Generated content for the section
        """
        if section_title not in self.current_project["sections"]:
            raise ValueError(f"Section '{section_title}' not found in outline.")
        
        section_data = self.current_project["sections"][section_title]
        
        section_data["content"] = self.ai_service.generate_section(
            self.current_project["topic"],
            section_title,
            section_data["description"],
            self.current_project["research"]
        )
        
        return section_data["content"]
    
    def generate_all_sections(self):
        """
        Generate content for all sections in the outline.
        
        Returns:
            dict: Dictionary of section titles and their content
        """
        if not self.current_project["sections"]:
            self.extract_sections_from_outline()
        
        for section_title in self.current_project["sections"]:
            self.generate_section_content(section_title)
        
        return {
            title: data["content"] 
            for title, data in self.current_project["sections"].items()
        }
    
    def generate_full_post(self):
        """
        Generate the complete blog post.
        
        Returns:
            str: Complete blog post content
        """
        # Option 1: Generate full post from scratch
        self.current_project["full_post"] = self.ai_service.generate_full_post(
            self.current_project["outline"],
            self.current_project["research"],
            self.current_project["meta"]["tone"]
        )
        
        return self.current_project["full_post"]
    
    def assemble_full_post_from_sections(self):
        """
        Assemble the full post from individual sections.
        
        Returns:
            str: Assembled blog post content
        """
        if not self.current_project["sections"]:
            raise ValueError("No sections generated. Please generate sections first.")
        
        # Extract title from meta or use topic
        title = self.current_project["meta"]["title"] or f"# {self.current_project['topic']}"
        
        # Start with title
        post_content = [title]
        
        # Add introduction if it exists as a section
        intro_section = None
        for title, data in self.current_project["sections"].items():
            if "introduction" in title.lower() or "intro" in title.lower():
                intro_section = title
                break
        
        if intro_section:
            post_content.append(self.current_project["sections"][intro_section]["content"])
        
        # Add remaining sections
        for title, data in self.current_project["sections"].items():
            if title != intro_section:  # Skip intro as we already added it
                post_content.append(f"## {title}")
                post_content.append(data["content"])
        
        # Combine into single document
        self.current_project["full_post"] = "\n\n".join(post_content)
        return self.current_project["full_post"]
    
    def save_project(self, directory="projects"):
        """
        Save the current project to files.
        
        Args:
            directory (str): Directory to save files in
            
        Returns:
            dict: Paths to saved files
        """
        if not self.current_project["topic"]:
            raise ValueError("No active project. Please create a new project first.")
        
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        
        # Create slug from topic
        slug = self.current_project["topic"].lower().replace(" ", "-")
        
        # Save project metadata
        project_path = os.path.join(directory, f"{slug}-project.json")
        with open(project_path, 'w') as f:
            json.dump(self.current_project, f, indent=2)
        
        # Save full post
        post_path = os.path.join(directory, f"{slug}-post.md")
        with open(post_path, 'w') as f:
            f.write(self.current_project["full_post"])
        
        return {"project": project_path, "post": post_path}
    
    def load_project(self, project_file):
        """
        Load a project from a file.
        
        Args:
            project_file (str): Path to project file
            
        Returns:
            dict: Loaded project data
        """
        with open(project_file, 'r') as f:
            self.current_project = json.load(f)
        
        return self.current_project
    
    def generate_strategy_memo(self):
        """
        Generate a strategy memo explaining how the content will outperform competitors.
        
        Returns:
            str: Strategy memo content
        """
        prompt = f"""
        Based on the research and outline for our blog post on "{self.current_project["topic"]}", 
        create a brief strategy memo that explains:
        
        1. How this content will outperform competitor articles
        2. What unique angles or value it adds
        3. Any novel structure or formatting elements that enhance the content
        
        Include specific points of differentiation and competitive advantage.
        """
        
        system_prompt = """
        You are a strategic content marketing expert. Provide a concise but thorough explanation 
        of how this content is positioned to succeed against competing articles, with specific 
        reference to its unique value, approach, and structural advantages.
        """
        
        return self.ai_service.generate_content(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1000,
            temperature=0.5
        )
