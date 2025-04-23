import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# pip install azure-ai-inference

load_dotenv()

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

response = client.complete(
    messages=[
        SystemMessage("You are one of the best programmers in the world. You have deep knowledge of all the software paradigms and you love to help others by providing your knowledge, writing the best technical content for beginners. "),
        UserMessage("What is the difference between python requests and httpx?"),
    ],
    temperature=0.1,
    # top_p=1,
    model=model,
    max_tokens=1000,
    )

print(response.choices[0].message.content)

