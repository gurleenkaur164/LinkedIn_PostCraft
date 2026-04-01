
from crewai import Task
from agents import researcher, writer, editor



research_task = Task(
    description=(
        "Research the following topic for a LinkedIn post:\n"
        "TOPIC: {topic}\n\n"
        "Your research output MUST include:\n"
        "1. THREE to FIVE compelling angles or counterintuitive insights\n"
        "2. At least TWO relevant statistics or data points (search for them)\n"
        "3. The top THREE pain points professionals face around this topic\n"
        "4. ONE real-world story or scenario that could anchor the post\n"
        "5. Tone recommendation: choose ONE from:\n"
        "   [Inspirational | Educational | Controversial | Personal Story | List-based]\n"
        "6. Target audience: who specifically will resonate with this post?\n\n"
        "Search the web to find current, accurate information. "
        "Do NOT make up statistics. If you cannot find data, say so."
    ),
    expected_output=(
        "A structured research brief with:\n"
        "- 3-5 compelling angles\n"
        "- 2+ real statistics with context\n"
        "- 3 professional pain points\n"
        "- 1 anchor story or scenario\n"
        "- Recommended tone\n"
        "- Target audience description"
    ),
    agent=researcher
)



write_task = Task(
    description=(
        "Using the research brief provided, write a LinkedIn post about:\n"
        "TOPIC: {topic}\n\n"
        "STRICT REQUIREMENTS:\n"
        "1. HOOK: First line must be under 12 words and make the reader STOP scrolling.\n"
        "   Good hook examples:\n"
        "   - 'I got fired. Best thing that ever happened to me.'\n"
        "   - 'Nobody talks about the dark side of being a developer.'\n"
        "   - '5 years ago I made $18/hr. Today I make $180/hr. Here's exactly what changed.'\n\n"
        "2. BODY:\n"
        "   - Short paragraphs: max 2 sentences each\n"
        "   - Use line breaks between every paragraph\n"
        "   - Include one specific story, example, or data point\n"
        "   - Build tension or curiosity — make each line earn the next\n\n"
        "3. CLOSING:\n"
        "   - End with ONE open-ended question that's easy to answer\n"
        "   - The question should invite personal opinions, not yes/no answers\n\n"
        "4. STYLE:\n"
        "   - First person ('I', 'my', 'me')\n"
        "   - Conversational, zero jargon\n"
        "   - No bullet points in the post itself\n"
        "   - Under 1300 characters total\n\n"
        "Output ONLY the post text. No titles, no explanations, no markdown."
    ),
    expected_output=(
        "A complete LinkedIn post draft:\n"
        "- Powerful first-line hook (under 12 words)\n"
        "- Short paragraph body with story/data\n"
        "- Open-ended closing question\n"
        "- Under 1300 characters\n"
        "- Plain text only, no markdown"
    ),
    agent=writer,
    context=[research_task]    
)



edit_task = Task(
    description=(
        "Edit and finalize the LinkedIn post draft about:\n"
        "TOPIC: {topic}\n\n"
        "YOUR EDITING CHECKLIST:\n\n"
        "1. HOOK AUDIT:\n"
        "   - Is the first line under 12 words? If not, cut it down.\n"
        "   - Does it create curiosity, shock, or instant relatability?\n"
        "   - If the hook is weak, REWRITE it entirely.\n\n"
        "2. FLOW & CLARITY:\n"
        "   - Remove any redundant sentences\n"
        "   - Ensure each paragraph flows naturally to the next\n"
        "   - Replace any jargon with plain language\n\n"
        "3. EMOJIS (add 3-5 total):\n"
        "   - Place naturally within the text, not randomly\n"
        "   - Use to emphasize key points, not decorate\n"
        "   - Do NOT put emojis in the hook line\n\n"
        "4. HASHTAGS (add at the very end, after a blank line):\n"
        "   - Include exactly 6-8 hashtags\n"
        "   - Mix broad (#Leadership) and niche (#CareerAdvice) tags\n"
        "   - All lowercase with camelCase for readability (#SoftwareEngineering)\n\n"
        "5. FINAL CHECK:\n"
        "   - Main post body under 1300 characters (count carefully)\n"
        "   - Closing question is open-ended and genuinely interesting\n"
        "   - Overall tone feels human, not AI-generated\n\n"
        "Output ONLY the final post. No explanations or meta-commentary."
    ),
    expected_output=(
        "The final publication-ready LinkedIn post:\n"
        "- Sharpened hook\n"
        "- Polished body with natural emoji placement\n"
        "- Engaging closing question\n"
        "- 6-8 hashtags on a new line at the end\n"
        "- Under 1300 characters (body only)\n"
        "- Ready to copy-paste and publish"
    ),
    agent=editor,
    context=[write_task]       
)