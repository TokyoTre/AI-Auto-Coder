# AI Auto-Coder 🚀  

An experimental AI-powered coding assistant that **writes, tests, and improves its own code**.  
The Auto-Coder generates Python solutions for given prompts, runs built-in test cases, detects failures or hallucinations, and iteratively refines outputs until the solution passes.  

This project demonstrates how **AI + self-testing + hallucination detection** can be combined into a semi-autonomous coding framework.  

---

## ✨ Features  
- **Prompt-to-Code Generation** – Convert natural language problem prompts into runnable Python code.  
- **Self-Testing** – Automatically executes generated code against test cases to verify correctness.  
- **Hallucination Detection** – Flags unexpected or irrelevant outputs.  
- **Iterative Refinement** – Re-prompts AI to fix errors until all tests pass.  
- **Extensible Framework** – Can be adapted for custom domains, optimizations, or integration with larger agentic AI pipelines.  

---

## 📂 Folder Structure  
AI_AutoCoder/
│── README.md # Project documentation
│── auto_coder.py # Core implementation
│── test/ # Unit tests & evaluation scripts
│── example/ # Example problem prompts & outputs
│── docs/ # Additional design notes and explanations

---

## ⚙️ How It Works  
1. **Input a Prompt**: Provide a natural language description of the coding problem.  
2. **Code Generation**: AI generates an initial Python solution.  
3. **Testing**: The solution is validated against pre-defined test cases (stored as tuples: `(function_name, args, expected_output)`).  
4. **Refinement**: If tests fail or hallucinations are detected, the system re-prompts and iterates.  
5. **Result**: A correct and optimized implementation is produced.  

---

## 🖥️ Example  

**Prompt:**  
Write a Python function called reverse_string that takes a single string s and returns the string in reverse order.

**Test Cases:** 
("reverse_string", ("hello",), "olleh"),
("reverse_string", ("AI Auto-Coder",), "redoC-otuA IA"),
("reverse_string", ("",), ""),
("reverse_string", ("12345",), "54321")

**Generated Solution:**  
def reverse_string(s: str) -> str:
    return s[::-1]

✅ Output passes all tests.

🔬 Use Cases:
- Rapid prototyping of coding solutions
- Automated test-driven development
- Exploring AI hallucination detection in code
- Building blocks for agentic AI systems

🚧 Next Steps:
- Add advanced hallucination classifiers.
- Expand test coverage and edge-case handling.
- Support multiple programming languages.
- Deploy as a web-based or CLI tool.

📜 License:
© 2025 Samuel Montgomery III. All rights reserved.

The AI Auto Coder and all associated code, modules, documentation, and assets
are proprietary software owned exclusively by Samuel Montgomery III.

Permission is NOT granted to copy, modify, distribute, sell, sublicense,
or otherwise use this software, in whole or in part, without express written
consent from the copyright holder.

This software is provided "as-is" without any warranties, express or implied,
including but not limited to fitness for a particular purpose or non-infringement.

For inquiries regarding licensing or authorized use, contact:
sam.mont006@gmail.com
(252) 350-1541

👤 Author
- Developed by Samuel A. Montgomery, III
- AI Developer & Prompt Engineer (Freelance-ready)
- Certifications: Generative AI Leader Professional Certificate (Google Cloud), IBM AI Developer Professional Certificate, Python for Data Science, AI & Development Certificate (IBM), Google AI Essentials Specialization, Google Prompting Essentials Specialization, Generative AI for Customer Support Specialization (IBM).