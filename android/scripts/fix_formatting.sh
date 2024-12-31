#!/bin/bash

# Exit on error
set -e

# Set Java version for the session
export JAVA_HOME=$(/Users/garotconklin/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home)
export PATH="$JAVA_HOME/bin:$PATH"

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