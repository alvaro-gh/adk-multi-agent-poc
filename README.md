# Google ADK Multi-Agent POC

This is me testing the [Google ADK](https://google.github.io/adk-docs/) with [browser-use](https://github.com/browser-use/browser-use). This work uses both Gemini for the main agent functionality and GPT for browser-use.

## Requirements

In order to use this you need:

* A `GOOGLE_API_KEY` environment variable for Gemini, see [here](https://aistudio.google.com/app/apikey).
* Another Google related environment variable: `GOOGLE_GENAI_USE_VERTEXAI=FALSE`.
* An OpenAI account with credits, along with the `OPENAI_API_KEY` environment variable set with your key.
* If you want to use the linkedin agent then you need to have your user in the `LINKEDIN_USER` environment variable and the password in `LINKEDIN_PASSWORD` environment variable.

## Instructions

**Instal UV**

All of this work relies on uv which is an amazing tool to manage Python projects, install instructions [here](https://docs.astral.sh/uv/getting-started/installation/).

**Clone the code**

```
$ git clone https://github.com/alvaro-gh/adk-multi-agent-poc
```

**Change directory***

```
$ cd adk-multi-agent-poc
```

**Create data directory**

```
$ mkdir manager/data
```

**Create virtual environment, activate it and install dependencies**

You need to have Python 3.12 installed and that can also be done with UV, instructions [here](https://docs.astral.sh/uv/guides/install-python/).

```
$ uv venv -p 3.12
$ source .venv/bin/activate
$ uv sync
$ playwright install chromium --with-deps --no-shell
```

**Run adk web**

```
$ adk web
```

## Interactions

There are two agents:

* Linkedin Agent: you can ask `Can you please login to linkedin?`
* YouTube Agent: you can ask `Can you please analyze this YouTube video: <VIDEO_URL>`
