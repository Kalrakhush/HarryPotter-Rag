from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
import yaml
import traceback
from dotenv import load_dotenv
from pathlib import Path

from src.utils.tools import PDFVectorSearchTool

@CrewBase
class HarryPotterRAGCrew:
    """Minimal Harry Potter RAG Crew with semantic retrieval + memory."""

    def __init__(self, pdf_path: str = None, config_dir: str = None):
        load_dotenv()
        # PROJECT_ROOT = D:/Harry_Potter_RAG
        project_root = Path(__file__).parents[2]

        # PDF path (overrideable)
        self.pdf_path = pdf_path or str(project_root / "data" / "harry_potter.pdf")

        # CONFIG DIR overrideable, else default to src/agents/config
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            # Path to <project_root>/src/agents/config
            self.config_dir = project_root / "src" / "agents" / "config"

        # load YAMLs
        try:
            with open(self.config_dir / "agents.yaml") as f:
                self.agents_config = yaml.safe_load(f)
            with open(self.config_dir / "tasks.yaml") as f:
                self.tasks_config = yaml.safe_load(f)
        except Exception:
            traceback.print_exc()
            self.agents_config = {}
            self.tasks_config = {}
    @agent
    def retrieval_agent(self):
        """Agent that uses semantic PDF search."""
        rag_tool = PDFVectorSearchTool(pdf_path=self.pdf_path)
        return Agent(
            config=self.agents_config["retrieval_agent"],
            verbose=True,
            tools=[rag_tool],
        )

    @agent
    def character_analysis_agent(self):
        """Agent that analyzes character style from context."""
        return Agent(
            config=self.agents_config["character_analysis_agent"],
            verbose=True,
        )

    @agent
    def response_generation_agent(self):
        """Agent that generates final response, with memory."""
        return Agent(
            config=self.agents_config["response_generation_agent"],
            verbose=True,
        )

    @task
    def retrieve_context(self):
        return Task(config=self.tasks_config["retrieve_context"])

    @task
    def analyze_character(self):
        return Task(config=self.tasks_config["analyze_character"])

    @task
    def generate_response(self):
        return Task(config=self.tasks_config["generate_response"])
    

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
