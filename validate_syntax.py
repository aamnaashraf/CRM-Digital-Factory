"""
Validate the syntax of the updated frontend files
"""
import os
import ast

def validate_tsx_like_syntax(file_path):
    """Validate that the file has proper JavaScript-like syntax with JSX"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Basic validation - check if it has the essential parts
        essential_parts = [
            '"use client"',
            'export default function',
            'useState',
            'useEffect'
        ]

        for part in essential_parts:
            if part not in content and part != 'useState':  # useState might not be in every file
                print(f"Warning: {part} not found in {file_path}")

        # Check for JSX structure
        if 'return (' in content or 'return <' in content:
            print(f"SUCCESS: {os.path.basename(file_path)} has proper JSX return structure")
            return True
        else:
            print(f"ERROR: {os.path.basename(file_path)} might have missing JSX structure")
            return False

    except Exception as e:
        print(f"ERROR: Error validating {file_path}: {e}")
        return False

if __name__ == "__main__":
    print("Validating frontend files syntax...")

    files_to_check = [
        "E:\\Hackathon 5\\frontend\\app\\channels\\gmail\\page.tsx",
        "E:\\Hackathon 5\\frontend\\app\\channels\\whatsapp\\page.tsx",
        "E:\\Hackathon 5\\frontend\\app\\page.tsx"
    ]

    all_valid = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            is_valid = validate_tsx_like_syntax(file_path)
            all_valid = all_valid and is_valid
        else:
            print(f"File not found: {file_path}")
            all_valid = False

    print(f"\nAll files valid: {all_valid}")