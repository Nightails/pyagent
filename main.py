import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import MAX_ITER
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


def iterate_gemini(client, user_prompt, verbose=False):
    final_result = ""
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    iter_count = 0
    while iter_count < MAX_ITER:
        content = prompt_gemini(client, messages)
        if verbose:
                final_result += f"User prompt: {messages[iter_count].parts[0].text}"
                final_result += f"\nPrompt tokens: {content.usage_metadata.prompt_token_count}"
                final_result += f"\nResponse tokens: {content.usage_metadata.candidates_token_count}"
        if not content.function_calls:
            final_result += f"\n{content.text}"
            break

        for candidate in content.candidates:
            messages.append(candidate.content)

        for call_part in content.function_calls:
            function_content = call_function(call_part, verbose)
            messages.append(function_content)
            function_response = function_content.parts[0].function_response.response
            if function_response:
                if verbose:
                    final_result += f"\n-> {function_response}"
                final_result += function_response["result"]
            else:
                break

        iter_count += 1
    return final_result


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
    print(iterate_gemini(client, user_prompt, verbose))


if __name__ == "__main__":
    main()
