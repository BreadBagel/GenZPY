import sys
import re

def yeet(*args):
    print(*args)

def nopeOut():
    exit()

def sufferWithIndex(iterable):
    return enumerate(iterable)

def clean_code(code):
    """ Remove all non-printable characters, including U+0008. """
    return ''.join(c for c in code if c.isprintable() or c in '\n\t')

def preprocess_code(code):
    """ Apply meme transformations (Python → Memes). """
    transformations = {
        r'\bprint\b': 'yeet',
        r'\bTrue\b': 'fact',
        r'\bFalse\b': 'cap',
        r'\bexit\(\)': 'nopeOut()',
        r'\breturn\b': 'gtfo',
        r'\bwhile\b': 'suffer',
        r'\btry\b': 'yolo',
        r'\bexcept\b': 'holdmybeer',
        r'\bfor\b': 'sufferWithIndex'
    }

    for pattern, replacement in transformations.items():
        code = re.sub(pattern, replacement, code)

    # Fix sufferWithIndex loops
    code = re.sub(r'\bsufferWithIndex (\w+) in (.+):', r'for \1, value in enumerate(\2):', code)

    return code

def reverse_transform(code):
    """ Reverse the meme transformations back to Python syntax. """
    reverse_transformations = {
        'yeet': 'print',
        'fact': 'True',
        'cap': 'False',
        'nopeOut()': 'exit()',
        'gtfo': 'return',
        'suffer': 'while',
        'yolo': 'try',
        'holdmybeer': 'except',
        'sufferWithIndex': 'for'
    }

    for meme, python_keyword in sorted(reverse_transformations.items(), key=len, reverse=True):
        code = re.sub(r'\b' + re.escape(meme) + r'\b', python_keyword, code)

    return code

def main():
    if len(sys.argv) < 2:
        print("Usage: python preprocess.py <filename>")
        return

    filename = sys.argv[1]

    try:
        with open(filename, 'r', encoding="utf-8") as file:
            code = file.read()
    except UnicodeDecodeError:
        print("Error: Unable to read file. Ensure it's UTF-8 encoded.")
        return

    if not code.strip():
        print("Error: The input file is empty.")
        return

    # Step 1: Apply meme transformations
    transformed_code = preprocess_code(code)

    if not transformed_code.strip():
        print("Error: No transformed code to execute.")
        return

    # Step 2: Reverse transformations back to Python
    final_code = reverse_transform(transformed_code)

    # Step 3: Save the final **Python code** to processed.py
    try:
        with open("processed.py", "w", encoding="utf-8") as f:
            f.write(final_code)
        print("✅ Final reversed Python code saved to processed.py")
    except Exception as e:
        print(f"❌ Error writing to processed.py: {e}")
        return

    # Step 4: Read back and clean processed.py before execution
    try:
        with open("processed.py", "r", encoding="utf-8") as f:
            sanitized_code = clean_code(f.read())  # Remove unwanted characters
    except Exception as e:
        print(f"❌ Error reading processed.py: {e}")
        return

    if not sanitized_code.strip():
        print("❌ Error: processed.py is empty after saving.")
        return

    print("🔄 Final Code (Before Execution):\n", sanitized_code)

    # Step 5: Execute final reversed Python code
    exec_globals = {
        "yeet": yeet,
        "nopeOut": nopeOut,
        "fact": True,
        "cap": False,
        "sufferWithIndex": sufferWithIndex
    }

    try:
        exec(sanitized_code, exec_globals)
    except Exception as e:
        print(f"Execution Error: {e}")

if __name__ == "__main__":
    main()
