import json
import re
import sys

# Define the file extensions to look for
FILE_EXTENSIONS = ['pdf', 'docx', 'xlsx', 'jpg', 'png', 'txt', 'csv', 'json', 'xml']

# Regex pattern to match file paths, including variable syntax like {{filePath}}
FILE_PATTERN = re.compile(
    r'{{[^{}]*\.(?:' + '|'.join(FILE_EXTENSIONS) + r')}}|[\w./\\-]+\.(?:' + '|'.join(FILE_EXTENSIONS) + r')',
    re.IGNORECASE
)

def extract_file_paths(data, path="root"):
    results = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path} → \"{key}\""
            results.extend(extract_file_paths(value, new_path))
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            new_path = f"{path} → [{idx}]"
            results.extend(extract_file_paths(item, new_path))
    elif isinstance(data, str):
        if FILE_PATTERN.search(data):
            results.append((path, data))

    return results

def print_help():
    help_text = """
Usage: python script.py <json_file>

This script scans a JSON file for file references based on common extensions
(e.g., .pdf, .docx, .jpg) and outputs the paths found, including those using
Handlebars-style syntax like {{filePath.pdf}}.

Output format:
  root → flows → [0] → "key"
  "key" : "value"

Options:
  -h, --help      Show this help message and exit

Example:
  python script.py data.json
"""
    print(help_text)

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print_help()
        sys.exit(0)

    json_file = sys.argv[1]

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        matches = extract_file_paths(data)
        for path, value in matches:
            key_match = re.search(r'→ "([^"]+)"$', path)
            key = key_match.group(1) if key_match else "<unknown>"
            print(f"{path}\n\"{key}\" : \"{value}\"\n")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)