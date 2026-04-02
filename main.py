
import os
from dotenv import load_dotenv
from crew import build_content_crew
from linkedin_publisher import publish_to_linkedin

load_dotenv()


def save_post(content: str, filename: str = "output.txt"):
    """Save the generated post to a local file as a backup."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f" Post saved to: {filename}")


def generate_and_publish(topic: str, auto_publish: bool = False):
    """
    Full pipeline:
    1. Build the 3-agent crew (Researcher + Writer + Editor)
    2. Run the crew with the given topic
    3. Show the generated post
    4. Ask for approval (unless auto_publish=True)
    5. Publish to LinkedIn

    Args:
        topic: The subject for the LinkedIn post
        auto_publish: If True, skips approval and posts immediately
    """

    print("\n" + "=" * 60)
    print("  SCROLLSTOPPER — AI LinkedIn Post Generator")
    print("=" * 60)
    print(f" Topic: {topic}")
    print("=" * 60 + "\n")

    
    print("Assembling AI crew...\n")
    crew = build_content_crew()

    
    result = crew.kickoff(inputs={"topic": topic})

    
    final_post = str(result).strip()

    
    print("\n" + "=" * 60)
    print(" GENERATED POST PREVIEW:")
    print("=" * 60)
    print(final_post)
    print("=" * 60)

    
    lines = final_post.split("\n")
    body_lines = [l for l in lines if not l.startswith("#")]
    body_text = "\n".join(body_lines).strip()
    char_count = len(body_text)
    print(f"\n Character count (body): {char_count}/1300")

    
    save_post(final_post)

    
    if not auto_publish:
        print("\n" + "-" * 60)
        approval = input(" Publish this post to LinkedIn now? (yes/no): ").strip().lower()
        if approval not in ("yes", "y"):
            print("\n Publishing cancelled.")
            print("   Your post has been saved to output.txt")
            print("   You can publish it manually anytime.\n")
            return final_post

    print("\n Connecting to LinkedIn API...")
    try:
        post_id = publish_to_linkedin(final_post)
        print("\n Done! Your post is now LIVE on LinkedIn!")
        print(f"   Post ID: {post_id}")
    except Exception as e:
        print(f"\n Publishing failed: {e}")
        print("   Your post has been saved to output.txt")
        print("   You can copy-paste it manually to LinkedIn.")

    return final_post


def main():
    print("\n Welcome to ScrollStopper!")
    print("   AI-powered LinkedIn posts, published in seconds.\n")

    
    topic = input(" Enter a topic for your LinkedIn post:\n> ").strip()

    if not topic:
        print(" No topic entered. Exiting.")
        return

    
    mode = input("\n Mode:\n  [1] Review before publishing (recommended)\n  [2] Auto-publish immediately\nChoose (1 or 2): ").strip()
    auto_publish = mode == "2"

    if auto_publish:
        print("\n Auto-publish mode: post will go live WITHOUT your review!")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        if confirm not in ("yes", "y"):
            auto_publish = False
            print("Switched to review mode.")

    generate_and_publish(topic, auto_publish=auto_publish)


if __name__ == "__main__":
    main()