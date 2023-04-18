import re

def validate_input(input_str):
    # Define the allowed pattern using a regular expression
    allowed_pattern = r"^[+-]?\d+(\.\d+)?$|^[\w\s]+$"

    # Check if the input matches the allowed pattern
    if not re.match(allowed_pattern, input_str):
        raise ValueError("Invalid input. Only integers, floats or strings are allowed.")

    # If the input is valid, return it
    return input_str

if __name__ == "__main__":
    # Test the function
    print(validate_input(77))
    print(validate_input(123))
    print(validate_input("abc"))
    x = validate_input('+234')
