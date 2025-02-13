import re
import os
import datetime

# Refined regex patterns
patterns = {
    'Visa': r'\b4[0-9]{12}(?:[0-9]{3})?\b',
    'MasterCard': r'\b(?:5[1-5][0-9]{14}|2(?:2[2-9][0-9]{2}|[3-6][0-9]{3}|7[0-1][0-9]{2}|720)[0-9]{12})\b',
    'AMEX': r'\b3[47][0-9]{13}\b',
    'DinersClub': r'\b3(?:0[0-5][0-9]{11}|[68][0-9]{12})\b',
    'CVV': r'\b[0-9]{3,4}\b'
}


# Valid extensions for text-based files
valid_extensions = {'.txt', '.log', '.csv'}

def search_patterns_in_file(file_path):
    """Search for credit card patterns in a given file and return matched lines and line numbers."""
    matches = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                for name, pattern in patterns.items():
                    if re.search(pattern, line):
                        matches.append((line_num, name, line.strip()))
    except (UnicodeDecodeError, IOError):
        print(f"Skipping file due to read error or encoding issue: {file_path}")
    return matches

def main():
    # Ask user for the directory to scan
    path = input("Enter the directory path (e.g., C:\\path\\to\\directory on Windows or /path/to/directory on Linux): ")
    
    if not os.path.isdir(path):
        print("Invalid directory path. Please enter a valid directory.")
        return
    
    # Prepare a report file with a timestamp
    report_filename = f"PANSearches-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    with open(report_filename, 'w', encoding='utf-8', errors='ignore') as report_file:
        report_file.write(f"PAN Search Report - {datetime.datetime.now().isoformat()}\n")
        report_file.write(f"Directory Scanned: {path}\n\n")
        
        # Flag to check if any matches were found
        any_matches = False

        # Walk through files in the specified directory
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip files that do not have valid extensions
                if not any(file.lower().endswith(ext) for ext in valid_extensions):
                    continue
                
                matches = search_patterns_in_file(file_path)
                
                # If matches are found, log them in the report file
                if matches:
                    any_matches = True
                    report_file.write(f"File: {file_path}\n")
                    for line_num, name, line in matches:
                        report_file.write(f"  Line {line_num}: [{name}] {line}\n")
                    report_file.write("\n")

        if not any_matches:
            report_file.write("No matches found.\n")

    print(f"Search complete. Report saved to {report_filename}")

if __name__ == "__main__":
    main()
