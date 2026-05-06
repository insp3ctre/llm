import os
import sys
import argparse
from google import genai
from google.genai import types # type: ignore
from dotenv import load_dotenv # type: ignore
from prompts import system_prompt
from functions.call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Gemini")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

MAX_ITERATIONS = 20

for i in range(MAX_ITERATIONS):

    results = []

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )   
    )

    if len(response.candidates) >= 1:
        for can in response.candidates:
            messages.append(can.content)

    if response.usage_metadata is None:
        raise RuntimeError("no usage metadata found")

    prompt_token = response.usage_metadata.prompt_token_count
    response_token = response.usage_metadata.candidates_token_count


    if response.function_calls is None or len(response.function_calls) == 0:
        print("No more functions to call")
        break
    
    for call in response.function_calls:
        function_call_result = call_function(call, verbose=args.verbose)

    if function_call_result.parts is None:
        raise Exception("function_call_result parts is empty")
    elif function_call_result.parts[0].function_response is None:
        raise Exception("function_call_result parts function_response is empty")
    elif function_call_result.parts[0].function_response.response is None:
        raise Exception("function_call_result parts function_response response is empty")

    results.append(function_call_result.parts[0])
    if args.verbose:
        print(f"-> {function_call_result.parts[0].function_response.response}")
    
    messages.append(types.Content(role="user", parts=results))

print(response.text)