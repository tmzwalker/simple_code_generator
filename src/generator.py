# for easier type hinting
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI


# Define the prompt template
template = """
You are an AI assistant that generates code snippets based on user descriptions.

User Description:
{description}

Please generate a code snippet in Python that addresses the user's description.

Code Snippet:
"""

prompt = PromptTemplate(template=template, input_variables=["description"])

def generate_code(query: str, model_name: str = "gpt-3.5-turbo") -> str:
    """
    Generate code snippet using the LLMChain.
    args:
    - query: str: The user's description of the code snippet they want to generate.
    - model_name: str: The name of the language model to use.
    return:
    - code_snippet: str: The generated code snippet.
    """
    # Initialize the LLMChain
    llm = ChatOpenAI(model_name = model_name)
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    
    # Generate code snippet using the LLMChain
    code_snippet = llm_chain.run(query)
    return code_snippet