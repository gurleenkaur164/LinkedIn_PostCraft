import os
import gradio as gr
from dotenv import load_dotenv
from crew import build_content_crew
from linkedin_publisher import publish_to_linkedin

load_dotenv()


def generate_post(topic):
    """Run the 3-agent crew and return the generated post."""
    if not topic.strip():
        return "", " Please enter a topic."

    try:
        crew = build_content_crew()
        result = crew.kickoff(inputs={"topic": topic})
        final_post = str(result).strip()

        # Save locally as backup
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(final_post)

        return final_post, " Post generated successfully!"

    except Exception as e:
        return "", f" Error: {str(e)}"


def publish_post(post_content):
    """Publish the generated post to LinkedIn."""
    if not post_content.strip():
        return " No post to publish. Generate one first."

    if not os.getenv("LINKEDIN_ACCESS_TOKEN", "").strip():
        return " LINKEDIN_ACCESS_TOKEN missing. Run: python auth/get_token.py"

    try:
        post_id = publish_to_linkedin(post_content)
        return f" Published successfully!\n📎 Post ID: {post_id}\n🔗 https://www.linkedin.com/feed/"
    except Exception as e:
        return f" Publishing failed: {str(e)}"



with gr.Blocks(title="ScrollStopper", theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    #  ScrollStopper
    ### AI-Powered LinkedIn Post Generator & Publisher
    Powered by **CrewAI + Groq (LLaMA 3)** — 100% Free
    
    ---
    """)

 
    with gr.Row():
        with gr.Column(scale=2):
            topic_input = gr.Textbox(
                label=" Enter Your Topic",
                placeholder="e.g. Lessons learned from failing my first startup",
                lines=2
            )
        with gr.Column(scale=1):
            gr.Markdown("""
            **How it works:**
            1.  Researcher finds angles & data
            2.  Writer drafts the post
            3.  Editor polishes & adds hashtags
            4.  You publish with one click
            """)

    generate_btn = gr.Button(" Generate Post", variant="primary", size="lg")

    
    status_box = gr.Textbox(
        label="Status",
        interactive=False,
        lines=1
    )

    
    post_output = gr.Textbox(
        label="Generated LinkedIn Post",
        placeholder="Your AI-generated post will appear here...",
        lines=12,
        show_copy_button=True   
    )

    
    gr.Markdown("---")
    gr.Markdown(" Publish to LinkedIn")
    gr.Markdown("_Review the post above, then click publish when ready._")

    publish_btn = gr.Button(" Publish to LinkedIn", variant="secondary", size="lg")

    publish_status = gr.Textbox(
        label="Publish Status",
        interactive=False,
        lines=3
    )

    
    gr.Examples(
        examples=[
            ["Lessons learned from failing my first startup"],
            ["How to overcome imposter syndrome as a developer"],
            ["Why I quit my 9-5 to freelance full time"],
            ["The biggest mistake junior developers make"],
            ["How AI is changing the job market in 2025"],
        ],
        inputs=topic_input,
        label=" Try these example topics"
    )

    
    gr.Markdown("""
    ---
    <center><small>Built with CrewAI · Groq LLaMA 3 · LinkedIn API · Gradio &nbsp;|&nbsp; <b>ScrollStopper</b></small></center>
    """)

    
    generate_btn.click(
        fn=generate_post,
        inputs=topic_input,
        outputs=[post_output, status_box]
    )

    publish_btn.click(
        fn=publish_post,
        inputs=post_output,
        outputs=publish_status
    )


if __name__ == "__main__":
    demo.launch(
        share=False,        
        server_port=7860,   
        inbrowser=True      
    )