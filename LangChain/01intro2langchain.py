# Objective is to create an LLM application for summarizing text..


from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


# pip install --upgrade --quiet  langchain-google-genai pillow


information = """
How small world networks and skip lists improve search precision
A navigable small world graph is a network structure where most points, or "nodes," are connected in a way that allows for efficient movement between any two points with only a few steps. This characteristic, known as the "small world" property, means that even in large networks, it takes only a limited number of jumps to connect distant nodes. Think of it as a social network: Although you may have thousands of friends, you can often reach someone across the globe through just a few mutual acquaintances. This structure is essential for systems like social media and communication networks, where moving quickly between points is a priority. However, to make searches even more efficient, particularly in massive datasets, additional layering is sometimes introduced.

This is where skip lists come in. A skip list is a layered data structure that speeds up searches by organizing information so that higher layers provide broad, approximate connections, while lower layers contain specific, detailed links. This layered setup allows searches to bypass unnecessary steps, “skipping” over parts of the dataset to hone in on relevant information quickly.

HNSW graphs combine both the small world property and the skip list’s hierarchical layering. The algorithm takes advantage of the structure's gradation by using the higher layers for rapid, coarse-grained exploration, while the finer, lower layers handle detailed searches. By optimizing the path toward the most similar nodes, based on a data structure and distance metric among neighboring nodes, HNSW enables efficient, precise navigation through massive datasets. This combination of coarse-to-fine search capability makes HNSW a powerful tool for complex, high-dimensional search tasks that traditional algorithms may struggle to perform.

Background of HNSW
Hierarchical navigable small worlds are used for high-dimensional similarity search and stand out due to their ability to efficiently find the nearest neighbors in large, multi-dimensional datasets. Hierarchical navigable small worlds were first introduced in a 2016 HNSW paper and have multiple implementations, including one in the Apache Lucene project.


"""

summary_template = """

given the information {information} about an article, I want you to do:
1. Provide background information about this article's main Topic.
2. and provide a nice summary for this article
"""

summary_prompt_template = PromptTemplate(
    input_variables=["information" ],
    template= summary_template
)


gpt = ChatOpenAI(model="gpt-3.5-turbo",temperature=0)
gemini = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
llama = ChatOllama(model="llama3.2")


chain = summary_prompt_template | gpt | StrOutputParser()

ai_msg = chain.invoke(input={"information": information})

print(ai_msg)













