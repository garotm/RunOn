#!/bin/bash

# Exit on error
set -e

echo "🔧 Fixing file formatting..."

# Find all Kotlin files
find . -name "*.kt" -type f | while read -r file; do
    # Ensure file ends with newline
    if [ "$(tail -c1 "$file" | xxd -p)" != "0a" ]; then
        echo "" >> "$file"
        echo "✓ Added newline to $file"
    fi
    
    # Remove trailing whitespace
    sed -i '' 's/[[:space:]]*$//' "$file"
    echo "✓ Removed trailing spaces from $file"
done

echo "✅ Formatting fixes complete!" 