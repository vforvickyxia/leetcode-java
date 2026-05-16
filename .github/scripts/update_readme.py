import os
import re

# Get all problem files (exclude README.md and hidden files/dirs)
files = sorted([
    f for f in os.listdir('.')
    if os.path.isfile(f) and f != 'README.md' and not f.startswith('.')
])

# Read current README
with open('README.md', 'r') as f:
    content = f.read()

# Parse existing table to preserve topics
existing_topics = {}
for match in re.finditer(r'\| \d+ \| (.+?) \| (.+?) \|', content):
    problem, topic = match.group(1).strip(), match.group(2).strip()
    existing_topics[problem] = topic

# Build new table
rows = ['| # | Problem | Topic |', '|---|---------|-------|']
for i, filename in enumerate(files, 1):
    topic = existing_topics.get(filename, '—')
    rows.append(f'| {i} | {filename} | {topic} |')
table = '\n'.join(rows)

# Update badge count
count = len(files)
content = re.sub(
    r'!\[solved\]\(https://img\.shields\.io/badge/solved-\d+-brightgreen\)',
    f'![solved](https://img.shields.io/badge/solved-{count}-brightgreen)',
    content
)

# Replace table block
content = re.sub(
    r'\| # \| Problem \| Topic \|.*?(?=\n\n---|\n\n##|\Z)',
    table,
    content,
    flags=re.DOTALL
)

with open('README.md', 'w') as f:
    f.write(content)

print(f"Updated README: {count} problems")
