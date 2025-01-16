# Casevo: Cognitive agents and social evolution simulator
![Casevo Logo](logo_casevo.svg)

## 1. Introduction

**Casevo (Cognitive agents and social evolution simulator)** is a Python framework specifically designed for building social simulation multi-agent experiments or applications based on complex networks. This tutorial aims to help you get started. By completing this tutorial, you will discover the core functionalities of Casevo. Throughout the tutorial, you will gradually create a basic level model, with features increasing as you progress.

The goal of this tutorial is to help you construct a simple basic level model and be able to perform simple analyses on the results.

Our paper is available at [this link](https://arxiv.org/abs/2412.19498). Citations are welcome.

```bibtex
@misc{jiang2024casevocognitiveagentssocial,
      title={Casevo: A Cognitive Agents and Social Evolution Simulator}, 
      author={Zexun Jiang and Yafang Shi and Maoxu Li and Hongjiang Xiao and Yunxiao Qin and Qinglan Wei and Ye Wang and Yuan Zhang},
      year={2024},
      eprint={2412.19498},
      archivePrefix={arXiv},
      primaryClass={cs.SI},
      url={https://arxiv.org/abs/2412.19498}, 
}
```

## 2. Background Information

Casevo is built on [Mesa](https://github.com/projectmesa/mesa), so it is similar in fundamental elements and operational logic. Key related information:

- **Mesa**: A Python-based Agent-based Modeling （[**agent-based model，ABM**](https://zh.wikipedia.org/wiki/%E4%B8%AA%E4%BD%93%E4%B8%BA%E6%9C%AC%E6%A8%A1%E5%9E%8B)） tool with straightforward logic and ease of secondary development.
  - [GitHub link](https://github.com/projectmesa/mesa)
- Components of simulation experiments in Mesa:
  - Model: Similar to the concept of a scene, it defines global scene information in the experiment, including scheduling methods and modeling approaches.
  - Agent: The agents within the scene.
  - Entry File: The entry file for the simulation experiment, typically named `run.py`.

Basic operational logic of the simulation experiment:

- The entry file repeatedly calls the `step` function defined in the model, representing each round of the simulation.
- The `step` function in the model calls the scheduler, which arranges the corresponding agent’s `step` function according to the schedule.

In summary, **the Model defines global information and events, while Agents define their own local information and events**.

If you want to further understand Mesa's operational logic, please read the [documentation](https://mesa.readthedocs.io/stable/tutorials/intro_tutorial.html) carefully.

## 3. Tool Installation

Create and activate a Python [virtual environment](https://docs.python-guide.org/dev/virtualenvs/) or a [conda environment](https://docs.conda.org.cn/projects/conda/en/stable/user-guide/index.html). Python version above 3.11 is required.

- Download the tool's whl file `casevo-0.3.18-py3-none-any.whl`.
- Install the tool using `pip install casevo-0.3.18-py3-none-any.whl`.

## 4. Building a Sample Simulation Experiment

### 4.1 Description of the Simulation Scenario and Configuration File Construction

The goal is to construct a beginner-level social simulation experiment. In the U.S. presidential elections, candidates organize debates, which are broadcast on television, allowing candidates to express their views and attract votes. However, the effects of debates are not easy to quantify or measure. To address this issue, we can create a virtual pool of voters to simulate the process of voters watching debate content, discussing with each other, and ultimately voting, thereby evaluating the effectiveness of the candidates' debates. This design not only ensures that agents make organized decisions but also reflects the influence of information exchange and individual experiences on final decisions through memory mechanisms and reflection processes.

Key information in the simulation experiment includes:

- Debate Content: Uses transcripts of the 2020 U.S. presidential television debates [Link1](https://www.debates.org/voter-education/debate-transcripts/october-22-2020-debate-transcript/) [Link2](https://www.presidency.ucsb.edu/documents/presidential-debate-belmont-university-nashville-tennessee-0)
  - Divided into 6 parts placed in the `content` folder.
- Voter Profiles: Derived from [political voter research article](https://www.pewresearch.org/politics/2021/11/09/beyond-red-vs-blue-the-political-typology-2/)
  - A total of 9 voter profiles, with 3 selected and configured in JSON format in the `person.json` file.
- Network Structure:
  - A random network with 9 nodes, using a complete network.

The following code in `build_case.py` can be used to build the simulation scenario configuration:

```python
import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import json
# Generate graph
# Number of nodes
node_num = 3
graph = nx.complete_graph(node_num)
graph_data = json_graph.node_link_data(graph)

# Configure profiles
with open('person.json') as f:
    person_data = json.load(f)

output_item = {
    "graph": graph_data,
    "person": person_data[:node_num]
}

# Output experiment configuration file
with open('case_lite.json', 'w') as f:
    json.dump(output_item, f, ensure_ascii=False)
```

The output result is `case_lite.json`:

```json
{
    "graph": {
        "directed": false,
        "multigraph": false,
        "graph": {},
        "nodes": [
            {
                "id": 0
            },
            {
                "id": 1
            },
            {
                "id": 2
            }
        ],
        "links": [
            {
                "source": 0,
                "target": 1
            },
            {
                "source": 0,
                "target": 2
            },
            {
                "source": 1,
                "target": 2
            }
        ]
    },
    "person": [
        {
            "general": "A 55-year-old conservative white male living in a rural community.",
            "character": "1) A devout Christian who believes religious faith is very important. Supports a greater role for religion in public life and believes government policies should support religious values.\n 2) Concerned about government and public affairs, wants a reduced role of government in society, holds restrictive views on abortion and same-sex marriage, believes legalizing same-sex marriage is harmful to the nation, thinks white people do not have advantages in society due to race, and are more likely to perceive that white people face significant discrimination today.\n 3) Believes a strong national military presence is essential in international affairs, and that the best way to ensure peace is through military strength rather than diplomacy. Supports military expansion.",
            "issue": "a) Believes the country is the strongest in the world.\n b) Sees illegal immigration as a very serious national issue.\n c) Believes the government should reduce public assistance to vulnerable groups.\n d) Thinks the decline in the proportion of people participating in religion is detrimental to society.\n e) Supports allowing towns to place religious symbols on public property.\n f) Feels conservatives cannot freely express their views."
        },
        {
            "general": "A white male over 50, financially stable, and well-educated.",
            "character": "1) Holds pro-business views, is positive about international trade, and advocates for a limited government role. Their approach to international relations centers on cooperating with U.S. allies and maintaining American military strength, with ally interests taken into account in foreign policy.\n 2) Holds a more moderate stance on immigration and racial issues but generally maintains a conservative attitude. 3) Actively participates in political activities.",
            "issue": "a) Identifies with the actions of Republican members in Congress.\n b) Believes government assistance to poor populations leads to excessive reliance on government aid and is more harmful than beneficial.\n c) Thinks everyone has the ability to succeed on their own.\n d) Partially agrees that vaccines are the best way to protect people from COVID-19."
        },
        {
            "general": "A white female living in a rural area with lower income and education levels.",
            "character": "1) An immigration hardliner who is critical of the economic system, views illegal immigration as a very serious national problem, believes legal immigration to the U.S. should be reduced, and thinks the decline in the proportion of white people in the U.S. population is harmful to society.\n 2) Holds a critical and skeptical attitude toward government and economic systems, advocating for increased taxation on large corporations, believing the entertainment industry, tech companies, and labor unions have negatively impacted the country's development.",
            "issue": "a) Believes the government is almost always inefficient and wasteful.\n b) Thinks the government interferes too much in personal and business matters.\n c) Feels illegal immigrants often make their communities worse.\n d) Believes the country's economic system unfairly favors powerful interest groups.\n e) Advocates for increasing taxes on households earning over $400,000."
        }
    ]
}
```

The overall simulation process can be described as follows:

- The simulation is divided into 6 rounds, with each round corresponding to a portion of the debate content, including events such as:
  - Public Debate: Agents receive information about presidential candidates' debates during this phase, mainly understanding and recording candidates' statements and policy positions. Each agent makes initial judgments based on their views and preferences.
  - Talk: After the debate, agents discuss with other voters. This is a critical stage for information exchange and conflict of views among agents. Discussion topics can include opinions on the debate, discussions on candidates' policies, or sharing of individual experiences.
  - Reflect: After the discussions, each agent engages in self-reflection. During this phase, agents conduct comprehensive thinking based on the content of the discussions, their understanding of the debate, and information in their memory. The reflection process introduces a memory mechanism, allowing agents to adjust their views on candidates based on past experiences and memories.
  - Vote: Each agent makes a voting decision based on the outcomes of the debate, discussion, and reflection. This step is the final output of the entire process, where all agents' decisions are reflected in the voting results.

### 4.2 Initialize Directories and Files

- Create the `election_example` project folder.
- Inside the project folder, create the main directories:
  - `content`: Texts of the debate content, named by rounds as `1.txt, 2.txt, ...`
  - `prompt`: Templates for all prompts
  - `log`: Directory for log output
  - `memory`: Directory for memory vector database
- Create the main project files:
  - `election_model.py`: Simulation scenario file
  - `election_agent.py`: Agent file
  - `baichuan.py`: Large model interface file, implementing the Baichuan Intelligence API in this example
  - `run.py`: Simulation entry point

*The code will be supplemented in the later sections of the tutorial.*

### 4.3 Implement the Large Model Interface File

This example integrates the [Baichuan Intelligence API](https://platform.baichuan-ai.com/docs/api), with the specific implementation referring to the [LLM_INTERFACE](#user-content-51-large-model-interface-llm_interfacepy-module).

### 4.4 Create the Agent (`election_agent.py`)

#### 4.4.1 Agent Initialization

Initialize the agent using [casevo.AgentBase](#user-content-56-agent-base-class-agentbase-agent_basepy), with the main steps including:

- Initializing the parent class
- Loading prompts
- Setting up the chain of thought (CoT)

```python
from casevo import AgentBase
from casevo import BaseStep, JsonStep
from casevo import TotLog
# Define steps in the CoT
class OpinionStep(BaseStep):
    def pre_process(self, input, agent=None, model=None):
        cur_input = input['input']
        cur_input['issue'] = input['last_response']
        return cur_input

class AgreeStep(JsonStep):
    def pre_process(self, input, agent=None, model=None):
        cur_input = input['input']
        cur_input['opinion'] = input['last_response']
        return cur_input
        
class ElectionAgent(AgentBase):
    def __init__(self, unique_id, model, description, context):
        # Initialize the parent class
        super().__init__(unique_id, model, description, context)
        # Load Prompts
        issue_prompt = self.model.prompt_factory.get_template("issue.txt")
        opinion_prompt = self.model.prompt_factory.get_template("opinion.txt")
        agree_prompt = self.model.prompt_factory.get_template("agree.txt")
        talk_prompt = self.model.prompt_factory.get_template("talk.txt")
        # Set up CoT
        issue_step = BaseStep(0, issue_prompt)
        opinion_step = OpinionStep(1, opinion_prompt)
        agree_step = AgreeStep(2, agree_prompt)
        talk_step = BaseStep(3, talk_prompt)
        chain_dict = {
            'listen': [issue_step, opinion_step, agree_step],
            'talk': [talk_step]
        }
        self.setup_chain(chain_dict)
```

#### 4.4.2 Define Agent Behavior Functions

Define the agent's behavior functions through member functions of the `ElectionAgent` class. The agent's behavior logic is managed using the chain of thought and multiple rounds of input-processing-output, determining how the agent receives information, processes it, reflects, and interacts with other agents.

###### (1) **`listen`** Function

- **Functionality:** Simulates the agent's behavior of listening to content. This function receives content from candidates' debates or discussions with other agents, processes it through the chain of thought, and records the agent's understanding and reaction.
  - The agent stores processed opinions, agreement levels, and other content in the memory module, and logs related information.

###### (2) **`talk`** Function

- **Functionality**: Implements the conversation behavior between agents. The agent interacts with a target agent based on the debate information it has heard, the results of its reflection, and long-term memory, exchanging opinions.
  - The function first processes the information through the chain of thought, then generates dialogue content and logs it. After the conversation, the target agent passes the dialogue content to its own `listen` function for further processing.

###### (3) **`reflect`** Function

- **Functionality**: The agent reflects on its long-term opinions and updates its long-term memory. By comparing the changes in opinions before and after reflection, the agent can learn and adapt to new information, while logging the reflection process.

#### 4.4.3 Define Agent Scheduling Function

By overriding the `casevo.AgentBase.step` function, implement the model's scheduling of agents. In this example, the agent interacts with another agent in its neighborhood with a certain probability, performing dialogue and information exchange through the `talk` function.

### 4.5 Create the Model (`election_model.py`)

#### 4.5.1 Model Initialization

Initialize the model using [casevo.ModelBase](#user-content-57-model-base-class-modelbase-model_basepy), with the main steps including:

- Initializing the parent class
- Generating agents and adding them to the scheduling sequence

```python
from election_agent import ElectionAgent
from casevo import ModelBase
from casevo import TotLog

# Test example model
class ElectionModel(ModelBase):

    # Generate model based on config
    def __init__(self, tar_graph, person_list, llm):
        """
        Initialize each person in the dialogue system and their dialogue process.
        :param tar_graph: Target graph representing the structure of the dialogue system.
        :param person_list: List of persons containing information about all participants in the dialogue.
        :param llm: Language model used to generate dialogue content.
        """
        super().__init__(tar_graph, llm)
        # Set up agents
        for cur_id in range(len(person_list)):
            cur_person = person_list[cur_id]
            cur_agent = ElectionAgent(cur_id, self, cur_person, None)
            self.add_agent(cur_agent, cur_id)
```

#### 4.5.2 Define Global Event Functions

Define global event functions through member functions of the `ElectionModel` class. In this example, the following two global functions are included:

###### (1) **`public_debate`** Function

- **Functionality**: This function simulates the process of a public debate, allowing each agent to listen to the debate content and adding the event to the log.

###### (2) **`reflect`** Function

- **Functionality**: Allows all agents to reflect, executing their respective `reflect` member functions.

#### 4.5.3 Define the Simulation Entry Function

By overriding the `casevo.ModelBase.step` function, implement a round of simulation experiments. In this example, it includes listening to the debate, agents engaging in free discussion, and forming opinions.

```python
# Step function of the overall model
    def step(self):
        # Listen to the debate content
        self.public_debate()
        # Agents engage in free discussion
        self.schedule.step()
        # Agents reflect
        self.reflect()
        return 0
```

### 4.6 Write the Simulation Entry File and Run (`run.py`)

Write the simulation entry file with the main functions including:

- Initializing the large model interface
- Reading the simulation configuration
- Initializing the model
- Calling the `ElectionModel.step` function for each round

Run the experiment by executing the following command in the command line:

```cmd
python run.py case_lite.json 6
```

Where `case_lite.json` is the configuration file, and `6` is the number of simulation rounds.

PS: In the example, you need to replace `API_KEY` in `run.py` with a valid Baichuan large model API_KEY.

### 4.7 Analyze the Results

The results will be output in the `log` folder, including the following files:

- `agent_id.json`: The event log for the agent with the corresponding ID, containing the opinion changes at each stage of the agent.
- `event.json`: The log of all events.
- `model.json`: The global event log for the model.

## 5. Module and API Overview

### 5.1 Large Model Interface: `llm_interface.py` Module

This module defines an interface base class for interacting with large language model (LLM).
The interface provides a standardized method for integrating different LLM implementations, making it easy to extend and integrate.

#### 5.1.1 Class: `LLM_INTERFACE`

This is an **abstract base class** that defines the essential methods required for interacting with LLMs, which must be **overridden** in subclasses.

- `send_message(prompt, json_flag=False)`:
  - **Parameters:**
    - `prompt`: The prompt text to send to the LLM.
    - `json_flag`: A boolean indicating whether the returned data should be in JSON format. The default is `False`.
  - **Returns**: This method should return the LLM's response to the prompt.
- `send_embedding(text_list)`:
  - **Parameters:**
    - `text_list`: A list of strings representing the texts to generate embeddings for.
  - **Returns**: This method should return the embeddings corresponding to the input texts.
- `get_lang_embedding()`:
  - **Returns**: This method should return an instance of the tool class used to generate LangChain embeddings.

### 5.2 Prompt Template: Prompt + PromptFactory (`prompt.py`)

This module defines classes for generating and sending prompt information, integrating template rendering functionality.

- Purpose:
  - Define prompts using templates
  - Use Jinja2 for templating
- The model shares a factory class PromptFactory,
  - Standardize the LLM call interface
- Each agent uses its own `Prompt` class

#### 5.2.1 Class: `Prompt`

Handles the generation and sending of prompt information. 

**Attributes**:

- `template`: The prompt template object.
- `factory`: The factory object used to send the generated prompt information.

**Methods**:

- `init(tar_template, tar_factory)`:Initializes a `Prompt`instance. This constructor prepares the necessary attributes for subsequent operations by providing the template and factory parameters.  
  - **Parameters**
    - `tar_template`: The template object used to generate the target file. The template object should have a specific structure and rules to guide the creation of the target file.
    - `tar_factory`: The factory object used to generate the target file based on the template. The factory object should have methods and logic for generating the actual target file based on the template. 
  - **Returns**: No return value. This method primarily initializes the instance attributes of the class.

- `get_prompt(tar_dict)`: Generates a prompt text by rendering the template with the provided dictionary.

- `send_prompt(ertra=None, agent=None, model=None)`: Generates and sends a prompt message. This method generates and sends a prompt message based on the provided parameters. It supports customization of the prompt content using an agent and model. Additional parameters (ertra) can provide further customization.  
  - **Parameters**
    - `ertra`: Additional parameters used to provide extra customization information, defaults to None.
    - `agent`: The agent object, if provided, will use the agent's description and context to customize the prompt message.
    - `model`: The model object, if provided, will use the model's context to customize the prompt message. 
  - **Returns**: The response result of the sent prompt message.

#### 5.2.2 Class: `PromptFactory`

Manages prompt templates and generates `Prompt` objects. 

**Attributes**:

- `prompt_folder`: Path to the template folder.
- `env`: Jinja2 environment object for loading templates.
- `llm`: Language model instance. 

**Methods**:

- `init(tar_folder, llm)`: Initializes a `PromptFactory` instance, responsible for setting the template folder path and the language model, as well as verifying the existence of the template folder. 
  - **Parameters**:
    - `param tar_folder`: The path to the template folder. It must be an existing directory.
    - `param llm`: An instance of the language model used for natural language processing.

- `get_template(tar_temp)`: Retrieves a template file from a specific folder based on the given template name. This method first constructs the full path to the template file and then checks if the file exists.
   - If the file does not exist, an exception is thrown.
   - If the file exists, the environment variable is used to load the template, and a `Prompt` object is returned, which is initialized using the loaded template and the current object. 
   - **Parameters**:
     - `tar_temp (str)`: The name of the template file. 
   - **Returns**:
     - `Prompt`: A `Prompt` object initialized using the loaded template and the current object. 
   - **Throws**:
     - `Exception`: An exception is thrown if the specified template file does not exist.

- `send_message(prompt_text)`: Sends the prompt text to the language model and returns the response result.

### 5.3 Thought Chain: Step + ThoughtChain (`chain.py`)

This module defines a chained structure for processing steps, including basic steps, choice steps, and rating steps, along with a ThoughtChain class for executing these steps. These classes allow users to create and manage complex interactive processes. 

Purpose: To quickly define and invoke a chain of thought processes.

#### 5.3.1 Step Class: `BaseStep`

`BaseStep` is the **base class** for all steps, providing fundamental methods for preprocessing input, executing actions, and handling post-processing tasks.

- Constructor `def __init__(self, step_id, tar_prompt)`
  - **Parameters**
    - `step_id`: A unique identifier for the step.
    - `tar_prompt`: The question or prompt that needs to be answered by the user.
- **Methods**
  - `pre_process(input, agent=None, model=None)`: Performs **preprocessing** on the input data and returns the processed data. *(Currently, the function returns the input directly, but additional preprocessing steps may be added as the functionality expands.)*
    - **Parameters**
      - `input`: The input data that needs preprocessing.
      - `agent`: (Optional) An agent object used for specific preprocessing tasks.
      - `model`: (Optional) A model object used for specific preprocessing tasks.
    - **Returns**: The processed input data.
  - `action(input, agent=None, model=None)`: Executes a specific action based on the input and context. The main responsibility of this function is to send a prompt and get a response by invoking the `send_prompt` method from the prompt module, considering the input, agent, and model information. This method is commonly used to generate replies in a dialogue system.
    - **Parameters**
      - `input (str)`: The user’s input, serving as the basis for generating a response.
      - `agent (Agent, optional)`: The agent object for passing contextual information. Defaults to None.
      - `model (Model, optional)`: The model object used for processing the input and generating a response. Defaults to None. 
    - **Returns**: The generated response text.
  - `after_process(input, response, agent=None, model=None)`:   This is a callback function that processes after the conversation. It collects and returns key information, such as the input and the final response, in a dictionary.
    - **Parameters**
      - `input`: The user's original input, used for logging or further processing.
      - `response`: The robot's response to the user's input, used for analysis or logging.
      - `agent`: The agent object, typically used to access dialogue management-related functions. Defaults to None, indicating it is not used.
      - `model`: The model object, typically used to access natural language processing-related functions. Defaults to None, indicating it is not used.
    - **Returns**: A dictionary containing the original user input and the last response generated by the system.

#### 5.3.2 Three Common Step Types for Thought Chains: Choice, Score, JSON

1. **Choice Step Class**: `ChoiceStep` is used for interaction steps that require the model to make a selection, with added logic for handling the model's choice responses.
2. **Score Step Class**: `ScoreStep` is used to evaluate and generate scoring responses based on a given step ID, target prompt, and scoring template.
3. **JSON Step Class**: `JsonStep` is used for handling data in JSON format.

#### 5.3.3 Thought Chain: `ThoughtChain`

This class extends `BaseAgentComponent`, representing a chain of operations consisting of a series of steps.

- **Constructor: `def __init__(self, agent, step_list)`**:This constructor is used to create an instance that represents a chain of operations composed of multiple steps. It inherits from a base class and customizes the instance with specific parameters.
  - **Parameters**:
    - `agent`: Agent responsible for executing the steps in the chain.
    - `step_list`: A list of steps that define the sequence and content of the chain.
- **Methods**:
  - `set_input(input)`: Sets the input content and updates the state.
  - `run_step()`: Executes the steps in the thought chain, sequentially calling the three functions in the step class and updating the step history and output.
  - `get_output()`: Retrieves the output content. The state must be `finish`.
  - `get_history()`: Retrieves the step history. The state must be `finish`.

### 5.4 Module Execution Logic

1. **Define the Large Model Interface**: Users customize the large model interface based on their requirements to ensure that messages can be sent and received.
2. **Define Prompt Templates**: Create Prompt templates that contain the information structure and format to be sent to the large model.
3. **Automatically Invoke the Large Model Interface**: Once the Prompt template is set, the system can automatically call the large model interface to generate an appropriate response.
4. **Combine with Thought Chain Steps**: Integrate the generated Prompt with specific steps in the thought chain to form a complete thought process.
5. **Invoke the Large Model via the Thought Chain**: Finally, use the thought chain's logic to call the large model, completing the information processing and response generation.

### 5.5 Memory Mechanism Memory + MemoryFactory (`memory.py`)

This module implements the agent's memory system, managing short-term and long-term memory, with persistence through integration with ChromaDB.

- Purpose
  - Implement memory mechanisms
  - Retrieval
  - Reflection
- Shared Factory Class MemoryFactory
  - Provides a unified LLM interface.
- Individual Memory Class for Each Agent
- All Memory Items Stored in a Vector Database Table
- RAG 
  - Background

#### 5.5.1 Memory Element: `MemoryItem` Class

Represents a single memory item.

- **Attributes**:
  - `id`: Unique identifier for the memory item, default is -1.
  - `ts`: Timestamp.
  - `source`: Source agent.
  - `target`: Target agent.
  - `action`: Event type.
  - `content`: Memory content.

- **Methods**:
    - `init(ts, source, target, action, content)`: Initializes a memory item.
    - `toDict()`: Converts the memory item to a dictionary.
    - `toList(memory_list, start_id)`: Converts a list of memory items to a list of content, metadata, and IDs.

#### 5.5.2 Memory Module: `Memory` Class

The memory module for the agent, responsible for managing short-term and long-term memory.

- **Methods**:
  - `__init__(component_id, agent, tar_factory)`: Initializes a Memory instance.
  - `add_short_memory(source, target, action, content, ts=None)`: Adds a memory item to short-term memory.
  - `search_short_memory_by_doc(content_list: List[str])`: Searches short-term memory based on a list of document content.
  - `reflect_memory()`: Updates long-term memory and retrieves the latest memory ID.
  - `get_long_memory()`: Retrieves long-term memory.

#### 5.5.3 Global Memory Factory: `MemoryFactory` Class

The global memory factory module, responsible for creating memory entities for agents and managing memory storage.

- **Methods**:
  - `__init__(tar_llm: LLM_INTERFACE, memory_num, prompt, model, tar_path=None)`: Initializes the memory module.
  - `create_memory(agent)`: Creates a Memory instance for the specified agent.
  - `add_short_memory(tar_memory: List[MemoryItem])`: Adds target memory items to short-term memory.
  - `search_short_memory_by_doc(content_list: List[str], tar_agent)`: Searches short-term memory based on content.
  - `reflect_memory(tar_agent, tar_pos, tar_long_opinion)`: Reflects on short-term memory to update long-term memory.

#### 5.5.4 External Memory: `BackgroundItem/Background/BackgroundFactory` Class

Handles the RAG functionality for external memory, designed with reference to the `MemoryItem/Memory/MemoryFactory` classes.

### 5.6 Agent Base Class AgentBase (`agent_base.py`)

This module defines the base class `AgentBase` for agents, providing fundamental functionality and structure for other agent classes. The `AgentBase` class extends `mesa.Agent`, responsible for initializing and managing the basic properties and behaviors of the agent.

- **Constructor**: `def __init__(self, unique_id, model, description, context)：`
  - **Parameters**:
    - `unique_id`: Unique identifier for the agent.
    - `model`: The model environment in which the agent is situated.
    - `description`: Description of the agent's persona.
    - `context`: Contextual information for the agent (used for prompt generation).
  - **Functionality**:
    - Calls the parent class's initialization method, setting the agent's unique ID and model.
    - Generates a component ID specific to the agent.
    - Initializes a logging object (optional, used for recording the agent's operations).
    - Sets the agent's description and context.
    - Creates a memory object using the model's memory factory to store the agent's state information.

- **Methods**:
  - `setup_chain`:**Initializes the agent's set of thought chains.** It creates a `ThoughtChain` instance for each thought chain in the given dictionary and stores them in `self.chains` for later operations.
    - **Parameters**
      - `chain_dict` (dict): Dictionary containing identifiers and data for the thought chains.
    - **Returns**: None
  - **Abstract Method**: `step`
    - Defines an abstract method that requires all subclasses to implement specific agent behaviors.
    - Allows for the direct setting of corresponding thought chains and scheduling functions and must be implemented.

### 5.7 Model Base Class ModelBase (`model_base.py`)

The `model_base.py` module defines a model class `ModelBase` based on the Mesa framework, which extends `mesa.Model` for creating and managing agent models. This model supports network structures, scheduling mechanisms, memory management, and prompt generation. Main functionalities include:

- **Network Setup**: Creates a network structure using `NetworkGrid`.
- **Agent Scheduling**: Manages agent activities via the `RandomActivation` scheduler.
- **Context Management**: Supports the transfer of contextual information.
- **Prompt Factory**: Integrates prompt templates for easy interaction with the large model interface.
- **Memory Factory**: Manages short-term and long-term memory.

- **Attributes**:
  - `grid`: The network space for agents.
  - `schedule`: The agent scheduler.
  - `context`: Contextual information.
  - `llm`: The language model.
  - `prompt_factory`: The prompt factory for generating prompts.
  - `memory_factory`: The memory factory for managing memory items.
  - `agent_list`: A list to store agent objects.

- **Methods**:
    - `init(tar_graph, llm, context=None, prompt_path='./prompt/', memory_path=None, memory_num=10, reflect_file='reflect.txt')`: Initializes the model and its related components.
    - `add_agent(tar_agent, node_id)`:Adds a new agent to the model and places it on the specified node.
      - **Parameters**：
        - `tar_agent`: The agent object to add.
        - `node_id`: The ID of the node where the agent will be placed.
    - `step()`: Executes a simulation step, advancing the simulation time and managing all agent activities. This method advances the simulation by one step and updates all scheduled objects. It does not take any parameters or return any meaningful value, mainly serving to trigger the progress of the simulation.
      - **Returns**: Always returns 0 as an indication of the step execution result.

### 5.8 Logging Class TotLog (`util/tot_log.py`)

The `TotLog` class is used for **recording and managing log data**, supporting the saving of log information to a file and managing time offsets. This class provides functionality for adding logs, setting logs, and writing logs to a file.

## 6 Acknowledgement
During the development of the Casevo, we are fortunate to have the support of a group of brilliant code contributors. 
- [Yafang Shi](https://github.com/Freya236)
- [Maoxu Li](https://github.com/limaoSure)
- [Hang Su](https://github.com/suhangha)