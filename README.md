# Web Interface to Generate Code

## Run the Code Locally

### Run the program - With poetry
1. Install [pyenv](https://realpython.com/intro-to-pyenv/#installing-pyenv)
2. Install poetry 
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
3. Download python 3.10.0 using pyenv
```bash
pyenv install 3.10.0
```
4. Create the poetry environment
```bash
pyenv global 3.10.0
poetry env use 3.10.0
```
5. Install the dependencies
```bash
poetry install
```
6. Run the application
```bash
cd src
poetry run uvicorn server:app --reload
```

### Prerequisites - Without poetry
1. Install [Anaconda](https://docs.anaconda.com/free/anaconda/install/index.html) or [Miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/)
2. Create a new environment
```bash
conda create -n code-generation-app python=3.10
conda activate code-generation-app
```
3. Install the dependencies
```bash
pip install -r requirements.txt
```
4. Run the application
```bash
cd src
uvicorn server:app --reload
```

### Contributing to this project
1. Clone the repository
```bash
git clone
```

2. Install the dependencies using one of the methods above, if not using poetry install the requirements-dev.txt
```bash
pip install -r requirements-dev.txt
```

3. Install the pre-commit hooks
```bash
poetry run pre-commit install --hook-type pre-commit --hook-type pre-push
# or
pre-commit install --hook-type pre-commit --hook-type pre-push
```

## Build and Run the Application

To build the application, we can use the following command:
```bash
docker build -t code-generation-app --build-arg OPENAI_API_KEY=$OPENAI_API_KEY -f build/Dockerfile .
```
Make sure that you have the `OPENAI_API_KEY` environment variable set with your OpenAI API key.

Then to run it, we can use the following command:
```bash
docker run -p 8000:8000 code-generation-app
```
## Using Custom LLM

### Choosing a Model

For the open source model, there are few options such as StarCoder and Llamacode. The current state-of-the-art model [is Llamacode-70B-instruct](https://ai.meta.com/blog/code-llama-large-language-model-coding/), which is a large language model trained specifically for code generation tasks. It is available on Hugging Face model hub and can be used for code generation tasks.

### Setting Up the Model
When considering using Llamacode-70B-instruct, to be aware of the cost and GPU requirements, it is important to consider the following:
- The model size and computational requirements for inference.
- The quantization and optimization techniques to reduce the computational cost.

For local deployment, we can try to use the model with quantization and optimization techniques to reduce the computational cost. For Llama specifically, we can use Llama-cpp, which is a C++ library for running Llama models, and it's python binding: [llama-cpp-python](https://github.com/abetlen/llama-cpp-python).

To start using the model, we can install the required dependencies for the model.
```
# for CPU
pip install llama-cpp-python # for CPU only

# for CUDA GPU on linux
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
```

After that, for high level usage, we can use LangChain wrapper to interact with the model.
```python
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp


def generate_code_llama(query: str, model_name: str = "codellama-7b-instruct.Q5_K_M.gguf") -> str:
    # Callbacks support token-wise streaming
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    prompt = PromptTemplate(query)
    llm = LlamaCpp(
        model_path=f"path/to/llama-model/{model_name}",
        n_gpu_layers=-1,  # The number of layers to put on the GPU. The rest will be on the CPU. If you don't know how many layers there are, you can use -1 to move all to GPU.
        n_batch=512, # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
    )
    callback_manager = CallbackManager()
    callback_manager.add_callback_handler(StreamingStdOutCallbackHandler())
    chain = LLMChain(llama_cpp, prompt, callback_manager)
    return chain.run()
```

When running the model locally, consider the computational resources required to run the model. Consider using smaller model with quantization for local GPU (e.g. [llama-7b-instruct-gguf](https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF)). The medium balanced quality model is a good starting point for local development and testing, which only requires 4.08GB of VRAM and 6.58GB of RAM
For production, we can use the larger model with higher quality (e.g. [llama-70b-instruct-gguf](https://huggingface.co/TheBloke/CodeLlama-70B-Instruct-GGUF)), which requires at most 73.29GB of VRAM and 75.79GB of RAM.
## Comparison Between LLM API and Custom LLM

### Cost Performance Analysis

The pros and cons of using LLM API (e.g., GPT-4):
- Pros:
    - No upfront costs for model development and training.
    - Access to state-of-the-art language models with proven performance.
    - Scalability and reliability handled by the API provider.
- Cons:
    - Recurring costs based on API usage, which can be significant for high-traffic applications.
    - Limited control over the model's behavior and performance.
    - Dependency on the API provider's availability and pricing structure.

The pros and cons of using Custom LLM are:
- Pros:
    - No recurring costs for API usage once the model is trained and deployed.
    - Full control over the model architecture, training process, and performance optimization.
    - Ability to fine-tune the model for specific domain or use case.
- Cons:
    - High upfront costs for training if we considering fine-tuning the model and infrastructure setup.
    - Requires specialized expertise in machine learning and model development.
    - Ongoing maintenance and updates are the responsibility of the development team.

#### Cost Calculation
Assuming that:
- For LLM API, we want to use GPT-4.
- For custom LLM, we want to use available state-of-the-art open-source models as it is without fine-tuning, e.g. `Llamacode-70B-instruct`.

For GPT-4 we can use this function to calculate the cost of generating code based on the number of tokens used:
```python
def calculate_token_cost(query: str, model_name: str = "gpt-3.5-turbo") -> str:
    with get_openai_callback() as cb:
        _ = generate_code(query, model_name)
        return str(cb)
```
Example of the cost calculation for GPT-4:
```python
>>> query = "Develop a user-friendly web interface using FastAPI that prompts users to input a description of their coding problem. The interface should interact with an LLM to generate a corresponding code snippet based on the user's input. Create the HTML template to support the python code as well."
>>> print(calculate_token_cost(query, "gpt-4"))
Tokens Used: 579
        Prompt Tokens: 174
        Completion Tokens: 405
Successful Requests: 1
Total Cost (USD): $0.02952
>>> query = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.You may assume that each input would have exactly one solution, and you may not use the same element twice.You can return the answer in any order."
>>> print(calculate_token_cost(query, "gpt-4"))
Tokens Used: 416
        Prompt Tokens: 174
        Completion Tokens: 242
Successful Requests: 1
Total Cost (USD): $0.019739999999999997
```

Assuming that the average cost for every user request is 0.025 USD, and the average number of user requests per hour is 100, the hourly cost for using GPT-4 would be 2.5 USD.

For custom LLM (Llamacode-70B-instruct), with quantization, [it needs at most 75.79GB of VRAM for the inference](https://huggingface.co/TheBloke/CodeLlama-70B-Instruct-GGUF#provided-files). Assuming that we're using the quantization with extremely low quality loss, we will need at least 1 A100 80GB GPU to run the model. [The cost of running 1 A100 80GB GPU on Google Cloud Platform is around 4.05 USD per hour for on-demand price](https://cloud.google.com/compute/vm-instance-pricing#accelerator-optimized). Let's assume we want to prepare for the peak traffic, if we're using 2 A100 80GB GPUs, the hourly cost for using custom LLM would be around 8.1 USD.

With such a small request per hour, using GPT-4 would be more cost-effective than using custom LLM. However, if the number of requests increases, the cost of using GPT-4 would increase linearly, while the cost of using custom LLM would remain constant. Therefore, if the number of requests per hour exceeds a certain number, using custom LLM would be more cost-effective than using GPT-4.

### Potential Scaling Challenges
Scaling challenges of using LLM API:
- Dealing with API rate limits and throttling during high-traffic periods.
- Managing the costs associated with increased API usage as the application scales.
- Ensuring the application can handle potential API downtime or performance issues gracefully.

Scalling challenges of using custom LLM:
- Handling increased traffic and concurrent requests may require scaling the infrastructure horizontally or vertically.
- Ensuring consistent performance and response times as the model serves more users simultaneously.
- Managing the computational resources and costs associated with scaling the custom LLM.

Scaling challenges, such as handling increased traffic and managing costs, need to be addressed for both options to ensure a robust and efficient code generation system.