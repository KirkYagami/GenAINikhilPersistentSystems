import asyncio
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

from dotenv import load_dotenv

load_dotenv()


# Define your LangChain components
llm = ChatOpenAI(name='gpt-4o')

template = "Translate the following English text to Hindi: {text}"
prompt = PromptTemplate(template=template, input_variables=["text"])

# Combine them into a RunnableSequence
chain = RunnableSequence(first=prompt, last=llm)

# Define an async function to run the chain
async def run_chain(text):
    return await chain.ainvoke({"text": text})

# Define a function to run multiple chains concurrently
async def run_multiple_chains(texts):
    tasks = [run_chain(text) for text in texts]
    results = await asyncio.gather(*tasks)
    return results

# List of texts to process
texts = [
    "Hello, how are you?",
    "What is your name?",
    "Where are you from?",
    "What do you do?"
]

# Run the chains concurrently
results = asyncio.run(run_multiple_chains(texts))

# Print the results
for result in results:
    print(result)