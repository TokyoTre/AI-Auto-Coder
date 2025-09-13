from auto_coder import run_tests

# Define test cases for add_numbers function
test_cases = [
    ("add_numbers", (2, 3), 5),
    ("add_numbers", (-1, 1), 0),
    ("add_numbers", (0, 0), 0),
    ("add_numbers", (100, 250), 350),
    ("add_numbers", (-50, -25), -75)
]

# Import a module to test
import generated_code  # Auto-coder output

success, message, failed, score = run_tests(generated_code, test_cases)
print(message)
