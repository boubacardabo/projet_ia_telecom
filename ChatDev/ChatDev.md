## CHATDEV Organizational Structure

ChatDev functions as a virtual software company with various intelligent agents holding different roles, including:
- Chief Executive Officer
- Chief Product Officer
- Chief Technology Officer
- Programmer
- Reviewer
- Tester
- Art Designer

These agents collaborate by participating in specialized functional seminars, which involve phases like designing, coding, testing, and documenting.

## CHATDEV Approach to Collaborative Software Development

CHATDEV acknowledges that utilizing AI for software development can lead to errors and incomplete code due to the lack of task specificity. To address this, CHATDEV creates a collaborative environment where diverse human agents work in conjunction with AI agents, such as large language models, to simulate the entire software development process. This approach divides the development process into phases, including designing, coding, testing, and documenting, and further breaks down each phase into smaller tasks referred to as "chat chains." These chat chains involve role-playing between different agents to achieve specific subtasks within the software development process.

### Key Mechanisms

Within CHATDEV, each chat involves three key mechanisms:

1. **Role Specialization**: Assigns specific roles to agents and provides task-specific instructions.
2. **Memory Stream**: Maintains a record of previous dialogues to aid in decision-making.
3. **Self-Reflection**: Allows agents to reflect on their decisions and make improvements as needed.

Overall, CHATDEV aims to enhance the software development process by facilitating effective communication and collaboration between human and AI agents.

## Coding Phase

In the coding phase of CHATDEV, three predefined roles are involved:

- Chief Technology Officer (CTO)
- Programmer
- Art Designer

This phase consists of sequential atomic chatting tasks, including generating code (CTO and programmer), and creating a graphical user interface (designer and programmer). The CTO instructs the programmer to implement a software system in markdown format, and the programmer generates code accordingly. The art designer focuses on creating a user-friendly graphical user interface using graphical icons and external text-to-image tools, which the programmer incorporates into the GUI design.

To improve code generation accuracy, CHATDEV introduces the "thought instruction" mechanism, which focuses on addressing specific problem-solving thoughts in instructions.

### Testing Phase

The testing phase in CHATDEV involves three roles:

- Programmer
- Reviewer
- Tester

This phase includes sequential tasks like peer review (programmer and reviewer) and system testing (programmer and tester). Peer review examines source code for potential issues, while system testing verifies software execution through tests conducted by the programmer using an interpreter, with a focus on application performance through black-box testing.

To address potential issues stemming from interpreter feedback, the "thought instruction" mechanism is employed to express debugging thoughts explicitly. The tester analyzes bugs, proposes modifications, and guides the programmer to eliminate potential bugs iteratively until the system functions correctly.

In situations where the interpreter struggles to identify fine-grained logical issues, CHATDEV allows a human client to provide feedback and suggestions in natural language, similar to a reviewer or tester. CHATDEV can understand and utilize this feedback to refine the software system.

## Documenting Phase

In the documenting phase of CHATDEV, following the designing, coding, and testing phases, four agents (CEO, CPO, CTO, and programmer) collaborate to create software project documentation. They use large language models and employ few-shot prompting with in-context examples for document generation. The CTO instructs the programmer to provide configuration instructions for environmental dependencies, resulting in a document like requirements.txt. This document enables users to configure the environment independently. Simultaneously, the CEO communicates requirements and system design to the CPO, who generates a user manual for the software.


## How to Set Up ChatDev to Run a Task on a Locally Installed Model using LM Studio (as a replacement for OpenAI)

1. **Clone the GitHub Repository**: Begin by cloning the repository using the command:
   ```bash
   git clone https://github.com/OpenBMB/ChatDev.git
   ```

2. **Set Up Python Environment**: Ensure you have a version 3.9 or higher Python environment. You can create and activate this environment using the following commands, replacing `ChatDev_conda_env` with your preferred environment name:
   ```bash
   conda create -n ChatDev_conda_env
   conda activate ChatDev_conda_env
   ```

3. **Install Dependencies**: Move into the ChatDev directory and install the necessary dependencies by running:
   ```bash
   cd ChatDev
   pip3 install -r requirements.txt
   ```

4. **Download and Install LM Studio**: Download and install LM Studio from this site: [https://lmstudio.ai/](https://lmstudio.ai/). On LM Studio, download an LLM model of your choice and launch a local server.

5. **Update the Configuration in ChatDev**: In your ChatDev Repository (the one you cloned from GitHub), open the "configs.py" file ("ChatDev\camel\configs.py") and add the following three lines of code to the end of the file:
   ```python
   import os
   os.environ["OPENAI_API_KEY"] = "sk-dummy1234"
   os.environ["OPENAI_API_BASE"] = "http://localhost:1234/v1"
   ```

6. **Build Your Software**: Use the following command to initiate the building of your software, replacing `[description_of_your_idea]` with your idea's description and `[project_name]` with your desired project name:
   ```bash
   python run.py --task "[description_of_your_idea]" --name "[project_name]"
   ```

7. **Run Your Software**: Once generated, you can find your software in the WareHouse directory under a specific project folder, such as `project_name_DefaultOrganization_timestamp`. Run your software using the following command within that directory:
   ```bash
   cd WareHouse/project_name_DefaultOrganization_timestamp
   python main.py
   ```

