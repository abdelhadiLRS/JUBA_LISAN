import re

with open('src/app/juba-modern.css', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Replace the problematic calc selector with a simple class
    if 'main .flex.h-' in line and 'calc' in line:
        line = line.replace('main .flex.h-\\\\[calc\\\\(100dvh-56px\\\\)\\\\]', 'main .juba-layout-container')
        line = line.replace('main .flex.h-\\[calc\\(100dvh-56px\\)\\]', 'main .juba-layout-container')
    new_lines.append(line)

with open('src/app/juba-modern.css', 'w') as f:
    f.writelines(new_lines)

print("CSS fixed!")
