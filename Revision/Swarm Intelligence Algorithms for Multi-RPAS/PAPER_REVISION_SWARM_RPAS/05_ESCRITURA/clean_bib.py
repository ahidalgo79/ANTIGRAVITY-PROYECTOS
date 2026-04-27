import re

def clean_bib(bib_path, cited_keys_path, output_path):
    with open(cited_keys_path, 'r') as f:
        cited_keys = set(line.strip() for line in f if line.strip())
    
    with open(bib_path, 'r') as f:
        content = f.read()
    
    # Split by entries
    entries = re.split(r'\n@', content)
    cleaned_entries = [entries[0]] # Keep the header
    
    for entry in entries[1:]:
        # Find the key
        match = re.search(r'^(\w+)\{([^,]+),', entry)
        if match:
            key = match.group(2)
            if key in cited_keys:
                cleaned_entries.append('@' + entry)
        else:
            # If no match, it might be a comment or something else, but let's be safe
            cleaned_entries.append('@' + entry)
            
    with open(output_path, 'w') as f:
        f.write(''.join(cleaned_entries))

if __name__ == "__main__":
    clean_bib('references_clean.bib', 'cited_keys.txt', 'references_clean.bib')
