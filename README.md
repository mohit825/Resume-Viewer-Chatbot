# resume-ai

A learning project for building a chatbot that answers recruiters' questions
about my professional experience.

Ticket 002 sends each question to Google Gemini through LangChain and displays
the generated response. Each question is independent. Gemini has not been given
my résumé or career information yet.

## Setup

Use Python 3.13 for this setup. Run these commands from the project folder
(currently named `resume-chatbot`).

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, use `py -3 -m venv .venv` to create the environment and
`.\.venv\Scripts\Activate.ps1` to activate it instead.

The virtual environment keeps this project's packages separate from other
projects. Activation makes `python` use that environment. The `-m` option runs
a Python module; `pip install -r requirements.txt` installs the packages listed
in that file. There are three direct dependencies:

- `streamlit`: the browser interface and local web server.
- `langchain-google-genai`: LangChain's Gemini integration. Its dependencies
  include LangChain Core and Google's SDK; no separate `langchain` install is needed.
- `python-dotenv`: loads local environment variables from `.env`.

Create the environment once. Activate it again whenever you open a new terminal
to work on this project.

## API key

Create a local `.env` file alongside `app.py` if you do not already have one.
Its API key setting should use this name (the value below is a placeholder):

```dotenv
GOOGLE_API_KEY=your_gemini_api_key_here
```

Keep your real key in `.env`. The app reads it on the Python server and does
not display it. `load_dotenv()` loads the file into the process environment;
`os.getenv("GOOGLE_API_KEY")` reads the value. An already exported environment
variable takes precedence over the file. Restart Streamlit after changing a key
so the process starts with fresh environment values.

## Run and try it

With the environment active:

```bash
python -m streamlit run app.py
```

Open the local URL printed in the terminal, usually <http://localhost:8501>.
Check that the **resume-ai** heading and chat input appear. Submit a question
such as "Explain a Python list in two sentences." You should see **User:**,
a spinner while Gemini responds, and then **Gemini:** with the generated answer.
Submit another question; it replaces the previous exchange because this version
does not store or send chat history.

To check the missing-key message, temporarily rename `GOOGLE_API_KEY` in `.env`
and restart Streamlit. If you also exported it in your terminal, unset that
variable first. Restore the setting and restart afterward. Never print the key
to debug it.

Press `Ctrl+C` in the terminal to stop the server. Run `deactivate` to leave
the virtual environment.

## How the app works

Streamlit starts a local web server, runs `app.py` from top to bottom, and turns
the `st.*` calls into browser elements. Submitting a question reruns the script:

```text
Chat input -> Python question string -> llm.invoke(question)
           -> Google Gemini API -> AIMessage -> response.text -> Streamlit
```

- `import streamlit as st` imports the library with the shorter name `st`.
- `st.title(...)` displays the heading; `st.write(...)` displays text.
- `question = st.chat_input(...)` displays the input and assigns its result to
  the variable `question`. The result is `None` before submission, or a string
  containing the submitted text.
- `if question:` checks for a nonempty value. The colon and indentation make
  the following indented lines part of that conditional block.
- `ChatGoogleGenerativeAI(...)` creates an object configured to call Gemini.
  Named arguments such as `model=...` configure it. This is similar to creating
  a JavaScript object with `new`, but Python omits `new`.
- `llm.invoke(question)` sends the prompt and waits for a complete response.
  It returns a LangChain `AIMessage` with content and response metadata.
- `response.content` may be a string or a list of content blocks. Gemini 3
  uses blocks, so `response.text` extracts the text for display.
- `with st.spinner(...)` shows a spinner while the indented code runs and
  removes it when the block exits, including if an exception occurs.
- `try` / `except Exception` handles request or setup failures, like JavaScript's
  `try` / `catch`. The app displays a fixed message instead of raw exception details.

The request timeout is 30 seconds. In the installed integration, `max_retries=1`
means one attempt with no automatic retries. Creating the Python object does
not train or download Gemini; inference runs on Google's servers when invoked.

On a later rerun without a submission, `st.chat_input` returns `None` and the
API call is skipped. Ordinary variables are assigned again on each run; this
app does not persist the exchange.

## Model access and API errors

The configured model is `gemini-3.5-flash-lite`, and a live setup check succeeded
with the local key. Google currently lists a free tier for this model. Actual
access and quotas depend on your Google project.

If a request fails, check your connection, key restrictions, selected model,
and quota in [Google AI Studio](https://aistudio.google.com/). A missing or
inaccessible model differs from an exhausted quota: retrying will not fix a
wrong model name. For a model-access issue, `gemini-3.1-flash-lite` is another
model currently listed with a free tier; check access for your project before
changing the `model=` argument in `app.py`. The app does not switch models
automatically.

See the official [Streamlit execution guide](https://docs.streamlit.io/get-started/fundamentals/main-concepts)
and [LangChain Gemini integration](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai).
Model availability and free-tier terms are documented in
[Google's model list](https://ai.google.dev/gemini-api/docs/models)
and [API pricing](https://ai.google.dev/gemini-api/docs/pricing).

## Private files

Keep API keys and private résumé data out of version control. `.gitignore`
excludes `.env` files, Streamlit secrets, PDFs, and the `data/` and `private/`
folders. Store any future private career notes in one of those folders.
