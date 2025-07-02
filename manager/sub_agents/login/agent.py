"""Linkedin Login Agent."""

import json
import os
from pathlib import Path

import aiofiles
from browser_use import Agent as BrowserAgent
from browser_use import BrowserSession
from browser_use.llm import ChatOpenAI
from google.adk.agents import Agent


async def linkedin_login() -> str:
    """Login to linkedin.com."""
    user = os.getenv("LINKEDIN_USER")
    pswd = os.getenv("LINKEDIN_PASSWORD")
    current_path = Path.cwd()
    state_path = current_path.joinpath("manager/data/state.json")

    if not state_path.exists():
        template = {"cookies": []}
        content = json.dumps(template)
        async with aiofiles.open(state_path.as_posix(), mode="w") as f:
            await f.write(content)

    session = BrowserSession(
        storage_state=state_path,
        user_data_dir=None,
        headless=True,
    )
    agent = BrowserAgent(
        task=f"""
        Go to linkedin.com and check if the user is logged in.
        If the user is not logged then log in using the following credentials:
        - Email: {user}
        - Password (inside the quotes): '{pswd}'
        If the user is already logged in do nothing.
        Your final message should explicitly state whether the user is logged in or not.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        browser_session=session,
    )
    history = await agent.run()
    r = history.final_result()
    if r is None:
        r = "There was no final result, consider this an error."
    return r


login_agent = Agent(
    name="login_agent",
    model="gemini-2.0-flash",
    description="Agent to login to linkedin",
    instruction="""
    You are a helpful assistant that uses the linkedin_login tool.
    The tool uses software to login to the linkedin.com website.
    You have to use the tool and wait for its final message.
    Evaluate the final message and check if it matches one of these scenarios:
    - The website login was successful.
    - The website login was not necessary.
    If the final message matches one of the scenarios do this:
    1. Tell the user a very short message about the scenario.
    2. Delegate the control back to the manager agent.
    If the final message does not match the listed scenarios do this:
    1. Tell the user that this task failed.
    2. Delegate the control back to the manager agent.
    """,
    tools=[linkedin_login],
)
