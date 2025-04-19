
"""

## Making asynchronous API calls
When working with APIs like Google GenAI, we often need to manage asynchronous operations. Asynchronous programming allows other operations to continue while waiting for network requests, making your application more responsive. This is particularly important when dealing with high-latency operations such as network requests.
"""



import asyncio
from google import genai
from google.genai.types import HttpOptions
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the client
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
    http_options=HttpOptions(api_version="v1")
)

# Define an async function to process a single request
async def generate_content(prompt):
    # We need to run the synchronous API in a thread pool to make it non-blocking
    loop = asyncio.get_event_loop()
    
    # Define what will run in the thread pool
    def sync_generate():
        response_text = ""
        print(f"Processing: {prompt}")
        for chunk in client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents=prompt,
        ):
            if hasattr(chunk, 'text') and chunk.text:
                print(chunk.text, end="", flush=True)
                response_text += chunk.text
        print("\n---\n")
        return response_text
    
    # Run the synchronous code in a thread pool and await its completion
    response = await loop.run_in_executor(None, sync_generate)
    return response

# Define a function to run multiple requests concurrently
async def process_multiple_prompts(prompts):
    tasks = [generate_content(prompt) for prompt in prompts]
    results = await asyncio.gather(*tasks)
    return results

# Example prompts to process
prompts = [
    "Why is the sky blue?",
    "Explain how photosynthesis works.",
    "What is the theory of relativity?",
    "How do airplanes fly?"
]

# Run the async function
async def main():
    results = await process_multiple_prompts(prompts)
    return results

if __name__ == "__main__":
    all_results = asyncio.run(main())