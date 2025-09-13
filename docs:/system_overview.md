# AI Auto-Coder System Overview

AI Auto-Coder is a Python framework that automatically generates, tests, and refines Python code from natural language prompts. 

Core Components:
1. auto_coder.py – Main engine
2. test/ – Unit tests and edge-case verification
3. example/ – Sample problem prompts and outputs
4. docs/ – Detailed documentation

Workflow:
- Receive problem prompt
- Generate Python solution using OpenAI API
- Run tests with run_tests()
- Detect hallucinations (invalid references)
- Iterate until solution passes all tests
