import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT
from call_function import available_functions
from call_function import function_names

def prompt_gemini(client, messages):
    return client.models.generate_content(
        model = 'gemini-2.0-flash-001',
        contents = messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT),
    )

def display_content(user_prompt, content, verbose):
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
    if not content.function_calls:
        return(content.text)
    for call_part in content.function_calls:
        function_response = call_function(call_part, verbose).parts[0].function_response.response
        if function_response:
            if verbose:
                print(f"-> {function_response}")
            return function_response["result"]
        else:
            raise Exception("Function failed to response")
def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    try:
        function = function_names[function_name]
        result = function("calculator", **function_call_part.args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": result},
                )
            ],
        )
    except Exception:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = list(filter(lambda x: not x.startswith("--"), sys.argv[1:]))

    if not args:
        print("Gemini Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    content = prompt_gemini(client, messages)
    print(f"Response:\n{display_content(user_prompt, content, verbose)}")

if __name__ == "__main__":
    main()
