"""
AI Service module for interacting with the OpenAI API.
Provides methods for content generation, research, and other AI-assisted tasks.
"""
import openai
from config import (
    OPENAI_API_KEY, 
    DEFAULT_MODEL,
    RESEARCH_TEMP,
    OUTLINE_TEMP,
    CONTENT_TEMP,
    DEFAULT_SYSTEM_PROMPT,
    MAX_TOKENS_RESEARCH,
    MAX_TOKENS_OUTLINE,
    MAX_TOKENS_SECTION,
    MAX_TOKENS_FULL_POST
)

# Configure OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

class AIService:
    """Service for interacting with OpenAI API to generate content."""
    
    @staticmethod
    def generate_content(prompt, system_prompt=DEFAULT_SYSTEM_PROMPT, 
                         temperature=CONTENT_TEMP, max_tokens=MAX_TOKENS_SECTION, 
                         model=DEFAULT_MODEL):
        """
        Generate content using OpenAI API.
        
        Args:
            prompt (str): The prompt for content generation
            system_prompt (str): System instructions for the AI
            temperature (float): Controls randomness (0-1)
            max_tokens (int): Maximum tokens in response
            model (str): Model to use for generation
            
        Returns:
            str: Generated content
        """
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating content: {e}")
            return f"Error generating content: {str(e)}"
    
    @staticmethod
    def conduct_research(topic, competitor_urls=None, focus_areas=None):
        """
        Conduct research on a topic using AI.
        
        Args:
            topic (str): The main topic to research
            competitor_urls (list): List of competitor article URLs
            focus_areas (list): Specific areas to focus research on
            
        Returns:
            str: Research findings
        """
        # Construct a comprehensive research prompt
        research_prompt = f"Conduct thorough research on the topic of '{topic}'."
        
        if competitor_urls:
            research_prompt += "\n\nAnalyze the following competitor articles and identify their strengths, weaknesses, and gaps:"
            for url in competitor_urls:
                research_prompt += f"\n- {url}"
        
        if focus_areas:
            research_prompt += "\n\nFocus particularly on the following areas:"
            for area in focus_areas:
                research_prompt += f"\n- {area}"
        
        research_prompt += "\n\nProvide a detailed research summary that includes:\n"
        research_prompt += "1. Key subtopics that should be covered\n"
        research_prompt += "2. Current trends and developments\n"
        research_prompt += "3. Important statistics and data points\n"
        research_prompt += "4. Authoritative sources that should be referenced\n"
        research_prompt += "5. Content gaps in existing articles that we can exploit\n"
        research_prompt += "6. SEO considerations (keywords, search intent, etc.)"
        
        system_prompt = """You are an expert research analyst specializing in technical topics. 
        Your task is to conduct thorough research and provide factual, up-to-date information
        that will inform the creation of a high-quality, authoritative blog post. Include specific
        references, data points, and actionable insights that set this content apart from competitors."""
        
        return AIService.generate_content(
            prompt=research_prompt,
            system_prompt=system_prompt,
            temperature=RESEARCH_TEMP,
            max_tokens=MAX_TOKENS_RESEARCH
        )
    
    @staticmethod
    def generate_outline(topic, research_summary, target_audience=None, tone=None):
        """
        Generate a comprehensive outline for a blog post.
        
        Args:
            topic (str): The main topic of the blog post
            research_summary (str): Research findings to inform the outline
            target_audience (str): The intended audience for the content
            tone (str): Desired tone for the content
            
        Returns:
            str: Outline for the blog post
        """
        outline_prompt = f"Create a comprehensive, SEO-optimized outline for a blog post about '{topic}'."
        
        if target_audience:
            outline_prompt += f"\n\nTarget audience: {target_audience}"
        
        if tone:
            outline_prompt += f"\n\nTone: {tone}"
        
        outline_prompt += "\n\nBased on the following research findings:\n" + research_summary
        
        outline_prompt += """
        
        The outline should include:
        1. An SEO-optimized title, H1, and meta description
        2. An introduction section with a hook, definition, and overview
        3. Main sections with H2 headings
        4. Subsections with H3 headings
        5. For each section, a brief description of what it should cover
        6. Suggestions for visual elements, examples, and statistics to include
        7. A conclusion section
        
        Make sure the structure flows logically and covers all important aspects of the topic.
        """
        
        system_prompt = """You are an expert content strategist and SEO specialist. 
        Your task is to create a comprehensive outline for a high-performing blog post
        that will rank well on search engines and provide exceptional value to readers.
        Structure the content for maximum impact, engagement, and readability."""
        
        return AIService.generate_content(
            prompt=outline_prompt,
            system_prompt=system_prompt,
            temperature=OUTLINE_TEMP,
            max_tokens=MAX_TOKENS_OUTLINE
        )
    
    @staticmethod
    def generate_section(topic, section_title, section_description, research_data):
        """
        Generate content for a specific section of the blog post.
        
        Args:
            topic (str): The main topic of the blog post
            section_title (str): The title of the section
            section_description (str): Description of what the section should cover
            research_data (str): Research data relevant to this section
            
        Returns:
            str: Generated content for the section
        """
        section_prompt = f"""Write a comprehensive and engaging section for a blog post about '{topic}'.
        
        Section title: {section_title}
        
        This section should cover: {section_description}
        
        Relevant research and information to include:
        {research_data}
        
        The content should be:
        - Thorough and informative
        - Technically accurate
        - Engaging and well-structured
        - SEO-optimized with natural keyword usage
        - Include examples, analogies, or case studies where appropriate
        - Written in an authoritative tone demonstrating expertise (E-E-A-T)
        
        Format the content using Markdown. Use appropriate H3 subheadings where needed.
        """
        
        return AIService.generate_content(
            prompt=section_prompt,
            max_tokens=MAX_TOKENS_SECTION
        )
    
    @staticmethod
    def generate_full_post(outline, research_data, tone="authoritative and educational"):
        """
        Generate a complete blog post based on an outline and research data.
        
        Args:
            outline (str): The outline for the blog post
            research_data (str): Research findings to inform the content
            tone (str): Desired tone for the content
            
        Returns:
            str: Complete blog post content
        """
        post_prompt = f"""Based on the following outline and research data, write a comprehensive, 
        high-quality blog post in a {tone} tone.
        
        OUTLINE:
        {outline}
        
        RESEARCH DATA:
        {research_data}
        
        The blog post should be:
        - Formatted in Markdown
        - SEO-optimized with appropriate keyword usage
        - Written to E-E-A-T standards (Experience, Expertise, Authoritativeness, Trustworthiness)
        - Include suggestions for relevant images, diagrams, or videos
        - Include practical examples, case studies, and analogies to explain complex concepts
        - Cite authoritative sources where appropriate
        
        Generate the complete blog post with all sections as outlined.
        """
        
        system_prompt = """You are an expert blog writer specializing in technical topics.
        Your task is to create a comprehensive, educational, and engaging blog post that
        demonstrates expertise and provides exceptional value to the reader. Follow SEO
        best practices while maintaining a natural, authoritative voice."""
        
        return AIService.generate_content(
            prompt=post_prompt,
            system_prompt=system_prompt,
            max_tokens=MAX_TOKENS_FULL_POST
        )
