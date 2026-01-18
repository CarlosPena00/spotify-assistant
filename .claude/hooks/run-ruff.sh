#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path' 2>/dev/null)

# Check if file exists and is a Python file
if [[ -z "$file_path" || ! -f "$file_path" || "$file_path" != *.py ]]; then
  exit 0
fi

uv run ruff check --fix --unsafe-fixes "$file_path"
uv run ruff format "$file_path"
exit 0
