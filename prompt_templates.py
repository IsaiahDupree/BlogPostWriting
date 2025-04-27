"""
Prompt templates for the NLP Blog Post Generator.
These templates guide the AI in generating different components of the blog post.
"""

# System prompts
RESEARCH_SYSTEM_PROMPT = """
You are an expert research analyst specializing in technical topics like Natural Language Processing (NLP), 
AI, and machine learning. Your task is to conduct thorough research and provide factual, up-to-date information
that will inform the creation of a high-quality, authoritative blog post.

Include specific references, data points, and actionable insights that set this content apart from competitors.
Focus on accuracy, comprehensiveness, and identifying content gaps that can be exploited.

Your analysis should demonstrate deep expertise (E-E-A-T) while remaining accessible to technical professionals.
"""

OUTLINE_SYSTEM_PROMPT = """
You are an expert content strategist and SEO specialist with expertise in technical topics like Natural Language Processing (NLP). 
Your task is to create a comprehensive outline for a high-performing blog post that will rank well on search engines and 
provide exceptional value to readers.

Structure the content for maximum impact, engagement, and readability. Your outline should include a logical progression 
of ideas that builds from fundamentals to advanced concepts, includes practical applications, and addresses the reader's 
search intent.

Follow E-E-A-T principles (Experience, Expertise, Authoritativeness, Trustworthiness) throughout your outline design.
"""

CONTENT_SYSTEM_PROMPT = """
You are an expert blog writer specializing in technical topics like Natural Language Processing (NLP) and AI.
Your task is to create comprehensive, educational, and engaging blog content that demonstrates expertise and 
provides exceptional value to the reader.

Your writing should:
- Follow SEO best practices while maintaining a natural, authoritative voice
- Explain complex concepts clearly with analogies and examples
- Include practical applications and real-world examples
- Maintain technical accuracy while being accessible to the target audience
- Demonstrate E-E-A-T standards (Experience, Expertise, Authoritativeness, Trustworthiness)

Format your content using Markdown and create a reading experience that flows logically and engages the reader.
"""

STRATEGY_SYSTEM_PROMPT = """
You are a strategic content marketing expert specializing in technical content like Natural Language Processing (NLP) blogs.
Provide a concise but thorough explanation of how this content is positioned to succeed against competing articles, 
with specific reference to its unique value approach, and structural advantages.

Your strategy memo should highlight competitive differentiators and explain exactly how the content meets or exceeds
the requirements specified in the original project brief.
"""

# Prompt templates
RESEARCH_PROMPT_TEMPLATE = """
Conduct thorough research on the topic of '{topic}'.

COMPETITOR ANALYSIS:
Analyze the following competitor articles and identify their strengths, weaknesses, and content gaps:
{competitor_urls}

FOCUS AREAS:
Pay particular attention to these specific areas:
{focus_areas}

RESEARCH DELIVERABLES:
Provide a detailed research summary that includes:

1. Key subtopics that must be covered in a comprehensive NLP article
   - Include both fundamental concepts and cutting-edge developments
   - Identify topics competitors are missing or covering inadequately

2. Important statistics, data points, and facts that should be included
   - Include quantitative information that demonstrates the impact and growth of NLP
   - Reference authoritative sources where possible

3. Content gaps and opportunities for differentiation
   - Identify what the competing articles are missing
   - Suggest unique angles or perspectives that could set our content apart

4. SEO considerations
   - Key primary and secondary keywords to target
   - Search intent analysis for NLP-related queries
   - Content structure recommendations for SEO optimization

5. Recommendations for visual elements and multimedia
   - Suggest diagrams, charts, or illustrations that would enhance understanding
   - Recommend video content that could be embedded to increase engagement

Your research should be comprehensive, factual, and strategically focused on creating content that surpasses
the competition in both quality and depth.
"""

OUTLINE_PROMPT_TEMPLATE = """
Create a comprehensive, SEO-optimized outline for a blog post about '{topic}'.

TARGET AUDIENCE:
{target_audience}

TONE:
{tone}

RESEARCH CONTEXT:
Based on the following research findings:
{research_summary}

OUTLINE REQUIREMENTS:
The outline should include:

1. SEO-optimized metadata:
   - Title tag (compelling, includes target keyword, under 60 characters)
   - Meta description (compelling summary, includes target keyword, under 160 characters)
   - Primary and secondary keywords to target throughout the content

2. Blog structure:
   - A compelling introduction with a hook, definition of NLP, and overview
   - Main sections with H2 headings that cover all essential aspects of NLP
   - Subsections with H3 headings that break down complex topics
   - A strong conclusion that summarizes key points and provides next steps or a call to action

3. For each section:
   - A clear heading that includes relevant keywords
   - A brief description of what the section should cover
   - Key points, facts, or concepts to include
   - Suggestions for examples, case studies, or real-world applications
   - Recommendations for visual elements or multimedia

4. Visual element recommendations:
   - Information architecture diagrams
   - Process flows or flowcharts
   - Comparison charts for different NLP approaches/models
   - Suggestion for code snippets or interactive elements

The outline should flow logically, progressively building understanding, and cover all important aspects
of NLP in a way that surpasses competitor articles in both depth and breadth.
"""

SECTION_CONTENT_PROMPT_TEMPLATE = """
Write a comprehensive and engaging section for a blog post about '{topic}'.

SECTION TITLE:
{section_title}

SECTION DESCRIPTION:
{section_description}

RELEVANT RESEARCH AND INFORMATION:
{research_data}

CONTENT REQUIREMENTS:
The content should be:
- Thorough and informative, covering the topic in depth
- Technically accurate with precise terminology and concepts
- Engaging and well-structured with a logical flow
- SEO-optimized with natural keyword usage
- Include examples, analogies, or case studies where appropriate
- Written in an authoritative tone demonstrating expertise (E-E-A-T)
- Accessible to the target audience: {target_audience}

FORMAT:
- Use Markdown formatting
- Include appropriate H3 subheadings where needed
- Suggest placement of visual elements or diagrams where helpful
- Include code snippets if relevant (especially for implementation sections)
- Recommend related resources or tools if applicable

The section should stand as a comprehensive treatment of its topic while fitting
seamlessly into the larger blog post structure.
"""

FULL_POST_PROMPT_TEMPLATE = """
Based on the following outline and research data, write a comprehensive, high-quality blog post about Natural Language Processing (NLP) in a {tone} tone.

OUTLINE:
{outline}

RESEARCH DATA:
{research_data}

CONTENT REQUIREMENTS:
The blog post should:
- Be formatted in Markdown with appropriate heading hierarchy
- Be SEO-optimized with strategic keyword usage
- Adhere to E-E-A-T standards (Experience, Expertise, Authoritativeness, Trustworthiness)
- Include suggestions for relevant images, diagrams, or videos at appropriate points
- Use practical examples, case studies, and analogies to explain complex concepts
- Cite authoritative sources where appropriate
- Have a compelling introduction that hooks the reader
- Include a strong conclusion with key takeaways
- Maintain a consistent tone and voice throughout

VISUAL ELEMENT RECOMMENDATIONS:
Throughout the post, include [IMAGE SUGGESTION] or [DIAGRAM SUGGESTION] or [VIDEO SUGGESTION] placeholders
with brief descriptions of what the visual should illustrate.

Target audience: {target_audience}

The final blog post should significantly outperform competing articles in depth, breadth, technical accuracy,
and overall value to the reader.
"""

STRATEGY_MEMO_PROMPT_TEMPLATE = """
Based on the research and outline for our blog post on "{topic}", create a brief strategy memo that explains:

1. How this content will outperform competitor articles
   - Specific competitive advantages over the AWS, IBM, and TechTarget articles
   - Areas where our coverage is more comprehensive or technically superior
   - Content elements that set our article apart

2. Unique angles or value our post adds
   - Novel perspectives or approaches not found in competitor content
   - Enhanced educational value through better explanations or examples
   - More comprehensive or up-to-date coverage of NLP technologies and applications

3. Novel structure or formatting elements
   - How our content organization improves reader experience
   - Use of visual elements, code snippets, or interactive components
   - Any innovative content presentation approaches

4. SEO advantage
   - How our keyword strategy positions the article for visibility
   - E-E-A-T signals incorporated into the content
   - Content depth and comprehensiveness advantages

Include specific points of differentiation with reference to the competitor articles and explain
how our approach specifically satisfies the project requirements.
"""
