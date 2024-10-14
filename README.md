# OLLAMA to query local documents 

Enterprises manage a vast amount of documentation, both for internal use and for customers. Traditionally, organizations have relied on search functionalities to navigate these documents, allowing teams to operate and perform text processing on them. However, providing tailored summaries for various user profiles has been challenging. For instance, a summary of banking documentation should differ for someone familiar with financial terminology compared to a first-time user. The same holds true for technical documents, where different audiences require varying levels of detail and clarity.

Large Language Models (LLMs) have transformed this landscape by enabling seamless document summarization, advanced querying (beyond simple search), and context-based follow-up actions. Extending these capabilities to other areas—such as employee inquiries, error reporting, and knowledge management—allows LLMs to support a unified, comprehensive solution. With this approach, LLMs play a pivotal role in creating a “single pane of glass,” offering enhanced accessibility and insights across multiple channels.

Here are some reasons why LLAMA is useful for document scanning:
- Efficient Text Analysis and Summarization
  * LLAMA can quickly process lengthy documents and provide summaries, allowing users to grasp the essential points without reading the entire document.
  * This is particularly useful for business reports, legal documents, or academic papers, where summarizing saves time and aids decision-making.
- Extracting Key Information
  * LLAMA can be fine-tuned or prompted to extract specific types of information, such as names, dates, financial figures, or other critical data points.
  * It can also identify and classify entities (like people, organizations, and locations) and perform tasks like fact extraction, which is valuable in fields such as compliance, legal, or healthcare.
- Natural Language Interaction
  * LLAMA enables users to query documents conversationally. You can ask it questions about the document’s content and get relevant responses, which can be much more intuitive than using traditional search or data extraction tools.
- Handling Multilingual and Unstructured Data
  * LLAMA can process documents in multiple languages and adapt to various formats, including unstructured data. This makes it ideal for organizations that handle diverse document types and languages.
- Automation and Scalability
  * LLAMA can process a vast number of documents efficiently, making it suitable for automated workflows that involve document review or compliance checks, significantly reducing manual workload and human error.
- Improving Accessibility
  * By generating plain language summaries or converting technical jargon into more accessible language, LLAMA can help make documents understandable to a broader audience.

### Objective
Our objective in this article is to use OLLAMA to run locally and process simple document with a LLAMA 3.1. We'll use Chroma DB for embeddings. 

### Architecture
[High level architecture] (https://github.com/KrishnanSriram/pyollamarestapi/blob/main/ollama_py_chroma.jpg)

### Cloud alternatives
If you want to not have anything build from scratch and want to run it from cloud, you do have some great choices in the form of Azure Open AI, Amazon Bedrock etc..

### Why OLLAMA?
Our approach is to see how we to build a small scale RAG LLM solution on my local machine or in local network

### What is OLLAMA?
OLLAMA is a command-line tool designed to make working with large language models (LLMs) more accessible and efficient for developers. It provides a unified interface for managing, deploying, and interacting with LLMs, allowing users to run and deploy models locally or on remote servers. OLLAMA supports a variety of tasks, such as generating text, summarizing content, and even performing question-answering or natural language processing tasks.

#### Download ollama and install it from ollama.com
If you use linux, here's the command
```
curl -fsSL https://ollama.com/install.sh | sh
```

Once you install, you can pull latest llama model. You can check all available models in olla.com/models

At the time of this article llama3.1 is the latest
```
ollama pull llama3.1

pulling manifest 
pulling 8eeb52dfb3bb... 100% ▕████████████████▏ 4.7 GB                         
pulling 948af2743fc7... 100% ▕████████████████▏ 1.5 KB                         
pulling 0ba8f0e314b4... 100% ▕████████████████▏  12 KB                         
pulling 56bb8bd477a5... 100% ▕████████████████▏   96 B                         
pulling 1a4c3c319823... 100% ▕████████████████▏  485 B                         
verifying sha256 digest 
writing manifest 
success 
```

You can check the installation with the following command

```
ollama list
```
You should see something like this

```
NAME               ID              SIZE      MODIFIED           
llama3.1:latest    42182419e950    4.7 GB    About a minute ago 
```

Yes, its a sizable installation. But you'll shortly understand why and the power this model brings to the table. Stay put

Before you ask your queries, you may want to observe the service. You can do that with the following command

```
ollama serve
```

If you receive port already used error. You stop the existing service and execute the above command. In Ubuntu to stop the service you can do

```
systemctl stop ollama
```

Now the service is running, Open another terminal and execute this command

```
ollama run llama3.1
```

You'll see something like this

```
~$ ollama run llama3.1
pulling manifest 
pulling 8eeb52dfb3bb... 100% ▕███████████████████████████████████████████████████████████████████████████████████▏ 4.7 GB                         
pulling 948af2743fc7... 100% ▕███████████████████████████████████████████████████████████████████████████████████▏ 1.5 KB                         
pulling 0ba8f0e314b4... 100% ▕███████████████████████████████████████████████████████████████████████████████████▏  12 KB                         
pulling 56bb8bd477a5... 100% ▕███████████████████████████████████████████████████████████████████████████████████▏   96 B                         
pulling 1a4c3c319823... 100% ▕███████████████████████████████████████████████████████████████████████████████████▏  485 B                         
verifying sha256 digest 
writing manifest 
success 
```

Now you are all set on the prompts, feel free to ask any general question....Why is the ocean blue or what's the pressure feel like under the ocean.....

Play around with it.

Our objective is to see how we can enable it as service and serve our own documents. We are still a long way from there, however we are heading in the right direction. Before we wrap up the initial setup process, you can check ollama's availability over http request too. Back to the terminal and execute this command

```
curl http://localhost:11434/api/generate -d '{
	"model": "llama3.1",
	"prompt": "In 5 lines tell me why ocean is blue?",
	"stream": false
}'
```

You should see response along with vector embeddings and probability. There you go. You are now all set. If you are happy just with this, you can build a simple front end API and call it a day. You can snap off wifi to see, if the model is really local or does it need any internet. However, if you want to have a RAG setup to query your documents, stick around.

Build a simple python API to upload files and query OLLAMA
A simple REST API based operation on local LLM You check out the code here https://github.com/KrishnanSriram/pyollamarestapi

We'll expand on this for processing documents in the following section

