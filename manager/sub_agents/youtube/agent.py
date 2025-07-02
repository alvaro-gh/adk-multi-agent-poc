"""YouTube Login Agent."""

from browser_use import Agent as BrowserAgent
from browser_use import BrowserSession
from browser_use.llm import ChatOpenAI
from google.adk.agents import Agent


async def analyze_youtube_comments(video: str) -> str:
    """Analyze YouTube video comments."""
    session = BrowserSession(
        user_data_dir=None,
    )
    agent = BrowserAgent(
        task=f"""
        Go to this YouTube URL: {video} and grab 5 comments.
        Summarize the comments and analyze the sentiment in no more than 100 words.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        browser_session=session,
    )
    history = await agent.run()
    r = history.final_result()
    if r is None:
        r = "There was no final result, consider this an error."
    return r


youtube_agent = Agent(
    name="youtube_agent",
    model="gemini-2.0-flash",
    description="Agent to analyze a YouTube video comments",
    instruction="""
    You are a helpful assistant that uses the analyze_youtube_comments tool.
    The tool uses software to login to analyze the comments on a YouTube video.
    You have to use the tool and wait for its final message.
    Pass the YouTube URL as a parameter for the tool.
    """,
    tools=[analyze_youtube_comments],
)
