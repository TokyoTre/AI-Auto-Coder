from auto_coder import run_tests
import generated_code

test_cases = [
    ("reverse_string", ("hello",), "olleh"),
    ("reverse_string", ("AI Auto-Coder",), "redoC-otuA IA"),
    ("reverse_string", ("",), ""),
    ("reverse_string", ("12345",), "54321")
]

success, message, failed, score = run_tests(generated_code, test_cases)
print(message)
