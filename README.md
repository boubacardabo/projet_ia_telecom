# Generative AI trained for software debugging and validation

## Project Overview

Create a generative AI able to support NXP developers during debugging phases and able to predict new bugs based on code/test updates. The model sohuld also be able to generate tests (unit, system) in Python for  NFC/UWB products. The AI must be able to understand the domain, the specification and the existing tests. RAG methods (Langchain,...) with open source models (Code Llama, Llama 2...) will be used.

## Architecture
See [architecture](architecture/README.md) for more information 

## End goals
Generative AI trained for software validation :

    - Code Writer:
        Use case: On demand generate of test from specification (unit, system)

    - Code Coverage:
        Use case: Generate missing tests improving the code coverage (positive and negative tests) 
        Use case: Injects invalid, malformed, or unexpected inputs into a system to reveal software defects and vulnerabilities.

    - Code Tester:
        Use case: Dynamic selection of test cases to run for the verification of code updates.

    - Log Reader:
        Use case: Chat with an AI on a large source of logs.

    - Advanced query with natural language
        Use case: Detect code error based on the log tracking - data lake.




Generative AI trained for software debugging:

    - Code Debugger:
        Use case: Detect new bugs by tracking the source evolution (testbench, tests, code, specs).
        Use case: Assist developers during the debugging phase.

    - Code Reader:
        Use case: Check if the source code is aligned to specification (UML,…).

    - Code Assistant:
        Use case: Understand existing source code, translate to human readable form.




