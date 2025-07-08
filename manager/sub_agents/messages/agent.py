"""Linkedin Login Agent."""

from pathlib import Path

from browser_use import Agent as BrowserAgent
from browser_use import BrowserSession
from browser_use.llm import ChatOpenAI
from google.adk.agents import Agent


async def linkedin_messages() -> str:
    """Login to linkedin.com."""
    current_path = Path.cwd()
    # the state must exist if we are being run
    state_path = current_path.joinpath("manager/data/state.json")

    session = BrowserSession(
        # storage_state=state_path,
        user_data_dir=current_path.joinpath("manager/data/"),
        #user_data_dir=None,
        headless=False,
        chromium_sandbox=False,
    )
    agent = BrowserAgent(
        task="""
        Go to https://www.linkedin.com/messaging and wait for that page to load.
        On the messaging page you don't need to filter or select any kind of messages,
        just use the messages you see on the page.
        There on the left you'll see a list of Contacts that the user can chat with.
        Next to that list you'll see the messages of each chat.
        For each contact get the chat history and summarize the sentiment.
        Then your output should be formatted as:
        <Contact Name>: <Sentiment>
        Repeat that for every Contact.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        browser_session=session,
    )
    history = await agent.run()
    r = history.final_result()
    if r is None:
        r = "There was no final result, consider this an error."
    return r


messages_agent = Agent(
    name="messages_agent",
    model="gemini-2.0-flash",
    description="Agent to get messages on linkedin for a user",
    instruction="""
    You are a helpful assistant that uses the linkedin_messages tool.
    The tool uses software to go to the www.linkedin.com website and gather data.
    You have to use the tool and wait for its final message.
    Evaluate the final message and check if it matches one of these scenarios:
    - There's a report of names and sentiments.
    - There's no report or any sort of error message.
    If the final message matches the first scenario do this:
    1. Return the result to the user as is.
    2. Delegate the control back to the manager agent.
    If the result does not match the first scenario do this:
    1. Tell the user that this task failed.
    2. Delegate the control back to the manager agent.
    """,
    tools=[linkedin_messages],
)
