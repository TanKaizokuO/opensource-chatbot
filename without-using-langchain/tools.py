from e2b_code_interpreter import Sandbox
from dotenv import load_dotenv
import os
import serpapi
import json


load_dotenv()

e2b_api_key = os.getenv("E2B_API_KEY")
serpai_api_key = os.getenv("SERPAPI_KEY")
serpai_api_key = os.getenv("SERPAPI_KEY")


def code_n_execute(prompt, client, CODER_MODEL):
    # Create OpenAI client
    system = "You are a helpful assistant that can execute python code in a Jupyter notebook. Only respond with the code to be executed and nothing else. Strip backticks in code blocks."

    # Send messages to OpenAI API
    response = client.chat.completions.create(
        model=CODER_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )

    # Extract the code from the response
    code = response.choices[0].message.content
    print("Code to execute: \n", code)
    # Execute code in E2B Sandbox
    if code:
        with Sandbox.create(api_key=e2b_api_key) as sandbox:
            execution = sandbox.run_code(code)
            result = execution.text

        print(result)

    return {"Code": code, "Result": result}


def google_search(query):
    client = serpapi.Client(api_key=serpai_api_key)
    results = client.search(
        {
            "engine": "google",
            "q": query,
            "location": "Austin, Texas, United States",
            "google_domain": "google.com",
            "hl": "en",
            "gl": "us",
        }
    )
    cleaned = [
        {
            "title": r["title"],
            "snippet": r["snippet"],
            "source": r.get("source"),
            "link": r["link"],
        }
        for r in results["organic_results"][:5]  # top 3 only
    ]

    content = json.dumps(cleaned)
    return content
