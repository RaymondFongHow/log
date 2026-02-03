import json
import sys
from datetime import datetime

def add_entry(date, category, title, description):
    """
    Add a new entry to updates.json
    
    Args:
        date: Date in YYYY-MM-DD format
        category: Category (e.g., "Mathematics", "Physics")
        title: Title of the entry
        description: Description text (can include HTML tags)
    """
    # Read existing data
    try:
        with open('updates.json', 'r') as f:
            entries = json.load(f)
    except FileNotFoundError:
        entries = []
    
    # Create new entry
    new_entry = {
        "date": date,
        "cat": category,
        "title": title,
        "desc": description
    }
    
    # Add to beginning of list (newest first)
    entries.insert(0, new_entry)
    
    # Write back to file
    with open('updates.json', 'w') as f:
        json.dump(entries, f, indent=2)
    
    print(f"✅ Added entry for {date}")
    print(f"   Category: {category}")
    print(f"   Title: {title}")
    print(f"\nTotal entries: {len(entries)}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python add_entry.py <date> <category> <title> <description>")
        print("Example: python add_entry.py 2025-02-05 Mathematics 'MATH 2551' 'Finished problem set 6 #math'")
    else:
        add_entry(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
