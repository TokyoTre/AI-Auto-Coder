from openai import OpenAI
import os
import importlib.util
import sys
from datetime import datetime
import ast
import re

# -------------------------------
# 1️⃣ Configure OpenAI client
# -------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------
# 2️⃣ Test runner with scoring
# -------------------------------
def run_tests(module, tests):
    failed = []
    score = 0
    for func_name, args, expected in tests:
        func = getattr(module, func_name)
        try:
            result = func(*args)
            if result != expected:
                failed.append(f"{func_name}{args} → {result}, expected {expected}")
            else:
                score += 1
        except Exception as e:
            if isinstance(expected, type) and issubclass(expected, Exception):
                if isinstance(e, expected):
                    score += 1
                else:
                    failed.append(f"{func_name}{args} → Raised {type(e)}, expected {expected}")
            else:
                failed.append(f"{func_name}{args} → Raised {type(e)}, expected {expected}")
    total = len(tests)
    success = len(failed) == 0
    message = f"{score}/{total} tests passed" if success else "\n".join(failed)
    return success, message, failed, score

# -------------------------------
# 3️⃣ Logging utility
# -------------------------------
def log_attempt(code, test_result, attempt_num, log_folder="logs"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    filename = f"{log_folder}/attempt_{attempt_num}_{timestamp}.py"
    with open(filename, "w") as f:
        f.write("# GPT attempt\n")
        f.write(code + "\n\n")
        f.write("# Test result / Score:\n")
        f.write(test_result + "\n")
    print(f"Saved attempt {attempt_num} to {filename}")

# -------------------------------
# 4️⃣ Generate additional edge-case tests
# -------------------------------
def generate_additional_tests(problem_prompt, current_tests):
    test_prompt = (
        f"Problem: {problem_prompt}\n"
        f"Existing tests: {current_tests}\n"
        "Generate 3-7 additional edge-case test cases "
        "in the format: (function_name, input_args tuple, expected_output). "
        "Return ONLY a valid Python list."
    )
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an expert Python programmer."},
            {"role": "user", "content": test_prompt}
        ],
        max_tokens=350
    )
    code = response.choices[0].message.content
    try:
        code_list = ast.literal_eval(code)
        return code_list if isinstance(code_list, list) else []
    except:
        return []

# -------------------------------
# 4.5️⃣ Hallucination detection
# -------------------------------
FORBIDDEN_CONSTRUCTS = ["xyz(", "nonexistent_", "fake_function", "magic_method", "foobar"]

def detect_hallucinations(code, forbidden_list=FORBIDDEN_CONSTRUCTS):
    return [item for item in forbidden_list if item in code]

# -------------------------------
# 5️⃣ Resume helper
# -------------------------------
def get_last_attempt(log_folder="logs"):
    if not os.path.exists(log_folder):
        return 0, None
    files = [f for f in os.listdir(log_folder) if f.startswith("attempt_")]
    if not files:
        return 0, None
    files.sort()
    last_file = files[-1]
    match = re.match(r"attempt_(\d+)_\d+\.py", last_file)
    if match:
        attempt_num = int(match.group(1))
        with open(os.path.join(log_folder, last_file), "r") as f:
            last_code = f.read()
        return attempt_num, last_code
    return 0, None

# -------------------------------
# 6️⃣ Auto-coder loop
# -------------------------------
def auto_code(problem_prompt, initial_tests, model="gpt-4-turbo", max_attempts=50, log_folder="logs"):
    last_attempt, previous_code = get_last_attempt(log_folder)
    attempt = last_attempt + 1
    success = False
    all_tests = initial_tests.copy()

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    while attempt <= max_attempts and not success:
        print(f"\n=== Attempt {attempt} ===")

        # Generate additional tests
        if previous_code:
            additional_tests = generate_additional_tests(problem_prompt, all_tests)
            all_tests.extend(additional_tests)
            print(f"Added {len(additional_tests)} additional edge-case tests.")

        full_test_results = "\n".join([f"{t[0]}{t[1]} → {t[2]}" for t in all_tests])

        # Detect hallucinations
        hallucinations = detect_hallucinations(previous_code) if previous_code else []
        hallucination_feedback = ""
        if hallucinations:
            print(f"⚠️ Hallucinations detected: {hallucinations}")
            hallucination_feedback = (
                f"The previous code contains invalid references: {hallucinations}. Remove them."
            )

        # Build GPT prompt
        if previous_code:
            user_prompt = (
                f"The previous code did not pass all tests.\n"
                f"Previous code:\n{previous_code}\n"
                f"Full test context:\n{full_test_results}\n"
                f"{hallucination_feedback}\n"
                "Rewrite the module to pass all tests. Return only valid Python code."
            )
        else:
            user_prompt = problem_prompt + "\n" + hallucination_feedback + "\nReturn only valid Python code."

        # Generate GPT code
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert Python programmer."},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1000
        )
        gpt_code = response.choices[0].message.content
        previous_code = gpt_code

        # Clean GPT code
        if "```" in gpt_code:
            parts = gpt_code.split("```")
            gpt_code = parts[1] if len(parts) >= 3 else parts[-1]
        lines = gpt_code.split("\n")
        if lines[0].strip().lower() == "python":
            lines = lines[1:]
        gpt_code = "\n".join(lines).strip()

        # Save and import code
        with open("generated_code.py", "w") as f:
            f.write(gpt_code)
        try:
            spec = importlib.util.spec_from_file_location("generated_code", "generated_code.py")
            module = importlib.util.module_from_spec(spec)
            sys.modules["generated_code"] = module
            spec.loader.exec_module(module)
        except Exception as e:
            message = f"Import error: {e}"
            print(message)
            log_attempt(gpt_code, message, attempt, log_folder)
            attempt += 1
            continue

        # Run tests
        success, message, failed_tests, score = run_tests(module, all_tests)
        print(f"Test result:\n{message}")
        if hallucinations:
            print(f"⚠️ Hallucinations detected: {hallucinations}")
        log_attempt(gpt_code, message, attempt, log_folder)

        if success and not hallucinations:
            print("\n✅ Function works and no hallucinations! Auto-coder finished successfully.")
            break
        elif not success:
            print("Code failed. GPT will try again with improved solution...")

        attempt += 1

    if not success:
        print("\n⚠️ Max attempts reached. Function may still fail some tests.")

# -------------------------------
# 7️⃣ Example usage
# -------------------------------
if __name__ == "__main__":
    problem_prompt = """

"""

test_cases = [

]


auto_code(problem_prompt, test_cases, model="gpt-4-turbo", max_attempts=50)

