"""
Main application file for the NLP Blog Post Generator.
Provides a Streamlit interface for generating high-quality blog posts.
"""
import streamlit as st
import os
import json
from blog_generator import BlogPostGenerator

# Initialize the blog post generator
generator = BlogPostGenerator()

# Page configuration
st.set_page_config(
    page_title="NLP Blog Post Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #e6ffe6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #fff8e6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state if not already done
if 'project_initialized' not in st.session_state:
    st.session_state.project_initialized = False
    st.session_state.research_done = False
    st.session_state.outline_generated = False
    st.session_state.sections_extracted = False
    st.session_state.full_post_generated = False
    st.session_state.strategy_memo_generated = False
    st.session_state.current_stage = "setup"
    st.session_state.project_data = {}
    st.session_state.competitor_urls = [
        "https://aws.amazon.com/what-is/nlp/",
        "https://www.ibm.com/think/topics/natural-language-processing",
        "https://www.techtarget.com/searchenterpriseai/definition/natural-language-processing-NLP"
    ]
    st.session_state.focus_areas = [
        "Latest NLP models and frameworks",
        "Real-world applications across industries",
        "Implementation approaches and best practices"
    ]

# Function to load existing projects
def load_existing_project():
    try:
        # List projects in the projects directory
        project_dir = "projects"
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        
        project_files = [f for f in os.listdir(project_dir) if f.endswith("-project.json")]
        
        if not project_files:
            st.warning("No existing projects found.")
            return
        
        selected_project = st.selectbox("Select a project to load:", project_files)
        
        if st.button("Load Selected Project"):
            project_path = os.path.join(project_dir, selected_project)
            project_data = generator.load_project(project_path)
            
            # Update session state
            st.session_state.project_initialized = True
            st.session_state.project_data = project_data
            
            # Set appropriate flags based on loaded project
            st.session_state.research_done = bool(project_data.get("research"))
            st.session_state.outline_generated = bool(project_data.get("outline"))
            st.session_state.sections_extracted = bool(project_data.get("sections"))
            st.session_state.full_post_generated = bool(project_data.get("full_post"))
            
            st.success(f"Project '{project_data['topic']}' loaded successfully!")
            st.session_state.current_stage = "view_post" if st.session_state.full_post_generated else "research"
    
    except Exception as e:
        st.error(f"Error loading project: {str(e)}")

# Main application header
st.markdown("<h1 class='main-header'>NLP Blog Post Generator</h1>", unsafe_allow_html=True)
st.markdown("Generate high-quality, SEO-optimized blog posts about Natural Language Processing (NLP) that outperform competing content.")

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    
    if not st.session_state.project_initialized:
        navigation = "Project Setup"
    else:
        navigation = st.radio(
            "Go to:",
            ["Project Setup", "Research", "Outline", "Content Generation", "View Post", "Strategy Memo", "Load Existing Project"]
        )
    
    st.session_state.current_stage = navigation.lower().replace(" ", "_")
    
    # Display project status if initialized
    if st.session_state.project_initialized:
        st.markdown("---")
        st.subheader("Project Status")
        st.write(f"Topic: {st.session_state.project_data.get('topic', 'Not set')}")
        
        # Status indicators
        if st.session_state.research_done:
            st.success("✅ Research completed")
        else:
            st.warning("⚠️ Research pending")
            
        if st.session_state.outline_generated:
            st.success("✅ Outline generated")
        else:
            st.warning("⚠️ Outline pending")
            
        if st.session_state.full_post_generated:
            st.success("✅ Full post generated")
        else:
            st.warning("⚠️ Full post pending")
            
        if st.session_state.strategy_memo_generated:
            st.success("✅ Strategy memo generated")
        else:
            st.warning("⚠️ Strategy memo pending")

# Main content area based on navigation
if st.session_state.current_stage == "project_setup":
    st.markdown("<h2 class='sub-header'>Project Setup</h2>", unsafe_allow_html=True)
    
    with st.form("project_setup_form"):
        topic = st.text_input(
            "Blog Post Topic",
            value="Natural Language Processing (NLP)",
            help="The main topic of your blog post"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            target_audience = st.text_input(
                "Target Audience",
                value="Technical professionals interested in AI and NLP",
                help="Who will be reading this content?"
            )
        
        with col2:
            tone = st.text_input(
                "Content Tone",
                value="authoritative and educational",
                help="The tone and style of writing"
            )
        
        competitor_urls = st.text_area(
            "Competitor URLs (one per line)",
            value="\n".join(st.session_state.competitor_urls),
            help="URLs of competing articles to analyze"
        )
        
        focus_areas = st.text_area(
            "Focus Areas (one per line)",
            value="\n".join(st.session_state.focus_areas),
            help="Specific areas or aspects to focus on"
        )
        
        submitted = st.form_submit_button("Start Project")
        
        if submitted:
            try:
                # Parse inputs
                competitor_urls_list = [url.strip() for url in competitor_urls.split('\n') if url.strip()]
                focus_areas_list = [area.strip() for area in focus_areas.split('\n') if area.strip()]
                
                # Initialize project
                project_data = generator.create_new_project(
                    topic=topic,
                    target_audience=target_audience,
                    tone=tone
                )
                
                # Update session state
                st.session_state.project_initialized = True
                st.session_state.competitor_urls = competitor_urls_list
                st.session_state.focus_areas = focus_areas_list
                st.session_state.project_data = project_data
                st.session_state.current_stage = "research"
                
                st.success("Project initialized successfully! Proceed to the Research stage.")
            except Exception as e:
                st.error(f"Error initializing project: {str(e)}")

elif st.session_state.current_stage == "research":
    st.markdown("<h2 class='sub-header'>Research</h2>", unsafe_allow_html=True)
    
    if not st.session_state.project_initialized:
        st.warning("Please set up a project first.")
        st.button("Go to Project Setup", on_click=lambda: setattr(st.session_state, 'current_stage', 'project_setup'))
    else:
        st.markdown("<div class='info-box'>In this stage, we'll analyze competitor content and conduct research to inform your blog post.</div>", unsafe_allow_html=True)
        
        # Display and edit competitor URLs
        st.subheader("Competitor URLs")
        competitor_urls = st.text_area(
            "One URL per line",
            value="\n".join(st.session_state.competitor_urls),
            key="research_competitor_urls"
        )
        
        # Display and edit focus areas
        st.subheader("Focus Areas")
        focus_areas = st.text_area(
            "One area per line",
            value="\n".join(st.session_state.focus_areas),
            key="research_focus_areas"
        )
        
        # Research API options
        st.subheader("Research Options")
        col1, col2 = st.columns(2)
        
        with col1:
            use_perplexity = st.checkbox(
                "Use Perplexity API for enhanced research", 
                value=True,
                help="Perplexity API provides more up-to-date information and enhanced competitor analysis"
            )
        
        with col2:
            st.info("💡 Perplexity API provides more comprehensive research with SEO insights and latest trends")
        
        if st.button("Conduct Research"):
            with st.spinner("Researching... This may take a minute or two."):
                # Parse inputs
                competitor_urls_list = [url.strip() for url in competitor_urls.split('\n') if url.strip()]
                focus_areas_list = [area.strip() for area in focus_areas.split('\n') if area.strip()]
                
                # Update session state
                st.session_state.competitor_urls = competitor_urls_list
                st.session_state.focus_areas = focus_areas_list
                
                # Conduct research with selected API
                if use_perplexity:
                    st.info("Using Perplexity API for enhanced research capabilities...")
                else:
                    st.info("Using OpenAI for research...")
                    
                research_results = generator.conduct_research(
                    competitor_urls=competitor_urls_list,
                    focus_areas=focus_areas_list,
                    use_perplexity=use_perplexity
                )
                
                # Update session state
                st.session_state.research_done = True
                st.session_state.project_data = generator.current_project
                
                st.success("Research completed successfully!")
        
        # Display research results if available
        if st.session_state.research_done:
            st.subheader("Research Results")
            st.markdown(st.session_state.project_data.get("research", ""))
            
            if st.button("Proceed to Outline"):
                st.session_state.current_stage = "outline"

elif st.session_state.current_stage == "outline":
    st.markdown("<h2 class='sub-header'>Outline Generation</h2>", unsafe_allow_html=True)
    
    if not st.session_state.research_done:
        st.warning("Please complete the research stage first.")
        st.button("Go to Research", on_click=lambda: setattr(st.session_state, 'current_stage', 'research'))
    else:
        st.markdown("<div class='info-box'>We'll create a comprehensive outline for your blog post based on the research findings.</div>", unsafe_allow_html=True)
        
        if not st.session_state.outline_generated:
            if st.button("Generate Outline"):
                with st.spinner("Generating outline... This may take a minute."):
                    # Generate outline
                    outline = generator.generate_outline()
                    
                    # Extract sections
                    sections = generator.extract_sections_from_outline()
                    
                    # Update session state
                    st.session_state.outline_generated = True
                    st.session_state.sections_extracted = True
                    st.session_state.project_data = generator.current_project
                    
                    st.success("Outline generated successfully!")
        
        # Display outline if available
        if st.session_state.outline_generated:
            st.subheader("Blog Post Outline")
            st.markdown(st.session_state.project_data.get("outline", ""))
            
            # Display extracted sections if available
            if st.session_state.sections_extracted:
                st.subheader("Extracted Sections")
                sections = st.session_state.project_data.get("sections", {})
                
                for i, (title, data) in enumerate(sections.items()):
                    with st.expander(f"Section {i+1}: {title}"):
                        st.write("Description:")
                        st.write(data.get("description", ""))
            
            if st.button("Proceed to Content Generation"):
                st.session_state.current_stage = "content_generation"

elif st.session_state.current_stage == "content_generation":
    st.markdown("<h2 class='sub-header'>Content Generation</h2>", unsafe_allow_html=True)
    
    if not st.session_state.outline_generated:
        st.warning("Please generate an outline first.")
        st.button("Go to Outline", on_click=lambda: setattr(st.session_state, 'current_stage', 'outline'))
    else:
        st.markdown("<div class='info-box'>Choose how you want to generate your blog post content.</div>", unsafe_allow_html=True)
        
        generation_method = st.radio(
            "Content Generation Method",
            ["Generate Full Post at Once", "Generate Section by Section"],
            index=0
        )
        
        if generation_method == "Generate Full Post at Once":
            if st.button("Generate Full Post"):
                with st.spinner("Generating full blog post... This may take several minutes."):
                    # Generate full post
                    full_post = generator.generate_full_post()
                    
                    # Update session state
                    st.session_state.full_post_generated = True
                    st.session_state.project_data = generator.current_project
                    
                    st.success("Blog post generated successfully!")
                    
                    # Save project automatically
                    try:
                        save_paths = generator.save_project()
                        st.success(f"Project saved to {save_paths['post']}")
                    except Exception as e:
                        st.error(f"Error saving project: {str(e)}")
                    
                    st.session_state.current_stage = "view_post"
        
        else:  # Section by Section
            st.subheader("Section Generation")
            
            sections = st.session_state.project_data.get("sections", {})
            
            for i, (title, data) in enumerate(sections.items()):
                with st.expander(f"Section {i+1}: {title}"):
                    st.write("Description:")
                    st.write(data.get("description", ""))
                    
                    if not data.get("content"):
                        if st.button(f"Generate Content for '{title}'", key=f"btn_gen_{i}"):
                            with st.spinner(f"Generating content for '{title}'..."):
                                # Generate section content
                                content = generator.generate_section_content(title)
                                
                                # Update session state
                                st.session_state.project_data = generator.current_project
                                
                                st.success(f"Content for '{title}' generated successfully!")
                                st.experimental_rerun()
                    else:
                        st.subheader("Generated Content")
                        st.markdown(data.get("content", ""))
            
            # Check if all sections have content
            all_sections_done = all(data.get("content") for data in sections.values())
            
            if all_sections_done:
                if st.button("Assemble Full Post"):
                    with st.spinner("Assembling full blog post..."):
                        # Assemble full post from sections
                        full_post = generator.assemble_full_post_from_sections()
                        
                        # Update session state
                        st.session_state.full_post_generated = True
                        st.session_state.project_data = generator.current_project
                        
                        st.success("Blog post assembled successfully!")
                        
                        # Save project automatically
                        try:
                            save_paths = generator.save_project()
                            st.success(f"Project saved to {save_paths['post']}")
                        except Exception as e:
                            st.error(f"Error saving project: {str(e)}")
                        
                        st.session_state.current_stage = "view_post"

elif st.session_state.current_stage == "view_post":
    st.markdown("<h2 class='sub-header'>View Generated Blog Post</h2>", unsafe_allow_html=True)
    
    if not st.session_state.full_post_generated:
        st.warning("No blog post has been generated yet.")
        st.button("Go to Content Generation", on_click=lambda: setattr(st.session_state, 'current_stage', 'content_generation'))
    else:
        st.markdown("<div class='success-box'>Your blog post has been generated successfully! You can view, download, or edit it below.</div>", unsafe_allow_html=True)
        
        # Display meta information
        with st.expander("Meta Information", expanded=True):
            meta = st.session_state.project_data.get("meta", {})
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Title")
                st.write(meta.get("title") or st.session_state.project_data.get("topic"))
                
                st.subheader("Target Audience")
                st.write(meta.get("target_audience", ""))
            
            with col2:
                st.subheader("Meta Description")
                st.write(meta.get("meta_description", ""))
                
                st.subheader("Keywords")
                st.write(", ".join(meta.get("keywords", [])))
        
        # Display full post
        st.subheader("Blog Post Content")
        full_post = st.session_state.project_data.get("full_post", "")
        st.markdown(full_post)
        
        # Download options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Download as Markdown"):
                topic_slug = st.session_state.project_data["topic"].lower().replace(" ", "-")
                download_path = f"projects/{topic_slug}-post.md"
                with open(download_path, "w") as f:
                    f.write(full_post)
                st.success(f"Blog post saved to {download_path}")
        
        with col2:
            if st.button("Generate Strategy Memo"):
                with st.spinner("Generating strategy memo..."):
                    strategy_memo = generator.generate_strategy_memo()
                    
                    # Update session state
                    st.session_state.strategy_memo_generated = True
                    st.session_state.strategy_memo = strategy_memo
                    
                    st.success("Strategy memo generated successfully!")
                    st.session_state.current_stage = "strategy_memo"

elif st.session_state.current_stage == "strategy_memo":
    st.markdown("<h2 class='sub-header'>Strategy Memo</h2>", unsafe_allow_html=True)
    
    if not st.session_state.full_post_generated:
        st.warning("Please generate a blog post first.")
        st.button("Go to Content Generation", on_click=lambda: setattr(st.session_state, 'current_stage', 'content_generation'))
    elif not hasattr(st.session_state, 'strategy_memo'):
        with st.spinner("Generating strategy memo..."):
            strategy_memo = generator.generate_strategy_memo()
            
            # Update session state
            st.session_state.strategy_memo_generated = True
            st.session_state.strategy_memo = strategy_memo
            
            st.success("Strategy memo generated successfully!")
    
    # Display strategy memo
    if hasattr(st.session_state, 'strategy_memo'):
        st.markdown("<div class='info-box'>This strategy memo explains how your blog post is positioned to outperform competing content.</div>", unsafe_allow_html=True)
        
        st.subheader("Strategy Memo")
        st.markdown(st.session_state.strategy_memo)
        
        # Download option
        if st.button("Download Strategy Memo"):
            topic_slug = st.session_state.project_data["topic"].lower().replace(" ", "-")
            download_path = f"projects/{topic_slug}-strategy-memo.md"
            with open(download_path, "w") as f:
                f.write(st.session_state.strategy_memo)
            st.success(f"Strategy memo saved to {download_path}")

elif st.session_state.current_stage == "load_existing_project":
    st.markdown("<h2 class='sub-header'>Load Existing Project</h2>", unsafe_allow_html=True)
    load_existing_project()

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by Your Blog Post Generator | Powered by OpenAI API")

if __name__ == "__main__":
    # This will only be executed when the script is run directly
    pass
