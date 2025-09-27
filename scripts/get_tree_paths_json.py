import json
import argparse
import os

def find_all_paths(data, target_key, target_value=None, path=None, results=None):
    if path is None:
        path = []
    if results is None:
        results = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_path = path + [key]
            if key == target_key:
                if target_value is None:
                    results.append((new_path, value))
                elif isinstance(value, (str, int, float)):
                    if target_value.lower() in str(value).lower():
                        results.append((new_path, value))
            find_all_paths(value, target_key, target_value, new_path, results)

    elif isinstance(data, list):
        for index, item in enumerate(data):
            find_all_paths(item, target_key, target_value, path + [f"[{index}]"], results)

    return results

def main():
    parser = argparse.ArgumentParser(
        description="Find all tree paths from the top level to a specified child key in a JSON file. Optionally match partial values."
    )
    parser.add_argument("-f", "--file", type=str, help="Path to the JSON file")
    parser.add_argument("-k", "--key", type=str, help="Target child key to search for")
    parser.add_argument("-v", "--value", type=str, help="Optional partial value to match (case-insensitive)")

    args = parser.parse_args()

    json_file = args.file or input("Enter the path to your JSON file: ")
    target_key = args.key or input("Enter the child key to find: ")
    target_value = args.value

    if not os.path.exists(json_file):
        print(f"Error: File '{json_file}' does not exist.")
        return

    try:
        with open(json_file, 'r') as f:
            data = json.load(f)

        paths = find_all_paths(data, target_key, target_value)
        if paths:
            print(f"Found {len(paths)} path(s) to key '{target_key}'" +
                  (f" with value containing '{target_value}':" if target_value else ":"))
            for p, val in paths:
                print(f"{' -> '.join(p)} : {repr(val)}")
        else:
            print(f"No matches found for key '{target_key}'" +
                  (f" with value containing '{target_value}'." if target_value else "."))

    except Exception as e:
        print("Error reading JSON file:", e)

if __name__ == "__main__":
    main()
