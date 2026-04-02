from crewai import Crew, Process
from agents import researcher, writer, editor
from tasks import research_task, write_task, edit_task

def build_content_crew()->Crew:
    """ Assembles the 3 agent content generation crew.
    Process.sequential= agents run one after another in order:
    Researcher then Writer then Editor.

    Each agent's output is automatically passed as context to the next agent via task context[] definitions.
    """
    return Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, write_task, edit_task],
        process= Process.sequential
        verbose=True,
        memory=False,
        max_rpm=10

    )