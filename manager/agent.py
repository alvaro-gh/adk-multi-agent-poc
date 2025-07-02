"""Manager Agent."""

from google.adk.agents import Agent

from .sub_agents.login.agent import login_agent
from .sub_agents.youtube.agent import youtube_agent

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="Manager Agent",
    instruction="""
    You are a manager AI agent that directs the work of other AI agents.
    The direction is done by delegating the appropiate work to the appropiate agent.
    Use the other agents descriptions to learn which agent is appropiate.
    First of all greet the user and ask what needs to be done.

    The agents that you can delegate work to are:
    - login_agent
    - youtube_agent
    """,
    sub_agents=[login_agent, youtube_agent],
)
