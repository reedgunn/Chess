import os
import json
from pathlib import Path
import pathspec

def load_gitignore(gitignore_path):
    """
    Load and compile the .gitignore file patterns.
    """
    if gitignore_path.exists():
        with gitignore_path.open('r') as f:
            patterns = f.read().splitlines()
        return pathspec.PathSpec.from_lines('gitignore', patterns)
    return pathspec.PathSpec.from_lines('gitignore', [])

def should_ignore(path, spec, base_path):
    """
    Determine if a path should be ignored based on the spec.
    """
    try:
        relative_path = path.relative_to(base_path)
    except ValueError:
        # Path is not relative to base_path
        return False
    return spec.match_file(str(relative_path))

def scrape_directory(base_dir, output_file='scraped_data.json'):
    """
    Traverse the directory, scrape file structure and contents,
    and save to a JSON file.
    """
    base_path = Path(base_dir).resolve()
    gitignore_path = base_path / '.gitignore'
    spec = load_gitignore(gitignore_path)

    scraped_data = {
        'base_directory': str(base_path),
        'files': []
    }

    for root, dirs, files in os.walk(base_path):
        current_dir = Path(root)
        
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(current_dir / d, spec, base_path)]
        
        for file in files:
            file_path = current_dir / file
            if should_ignore(file_path, spec, base_path):
                continue
            try:
                with file_path.open('r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception as e:
                content = f'Error reading file: {e}'
            
            relative_path = file_path.relative_to(base_path)
            scraped_data['files'].append({
                'path': str(relative_path),
                'content': content
            })

    # Save the scraped data to a JSON file
    with open(output_file, 'w', encoding='utf-8') as out_f:
        json.dump(scraped_data, out_f, indent=4, ensure_ascii=False)
    
    print(f"Scraped data saved to {output_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scrape directory structure and file contents.")
    parser.add_argument('directory', help='Path to the target directory')
    parser.add_argument('--output', default='scraped_data.json', help='Output JSON file')
    args = parser.parse_args()

    scrape_directory(args.directory, args.output)

# python3 scrape_directory.py /path/to/target/directory --output output.json
# python3 scrape_directory.py /Users/reedgunn/Chess --output output.json