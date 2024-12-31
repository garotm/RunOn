#!/bin/bash

# Set Java version for the session
export JAVA_HOME=$(/Users/garotconklin/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home)
export PATH="$JAVA_HOME/bin:$PATH"

# Exit on any error
set -e

# Change to the backend directory
cd "$(dirname "$0")/.."

# Get the project root directory (one level up from backend)
PROJECT_ROOT="$(dirname "$(pwd)")"

# Check if .env file exists in project root
if [ ! -f "${PROJECT_ROOT}/.env" ]; then
    echo "❌ Error: .env file not found in project root!"
    echo "Please create a .env file in ${PROJECT_ROOT} with the following variables:"
    echo "RUNON_CLIENT_ID=your_client_id"
    echo "RUNON_API_KEY=your_api_key"
    echo "RUNON_SEARCH_ENGINE_ID=your_search_engine_id"
    exit 1
fi

# Create symlink to .env file if it doesn't exist in backend
if [ ! -f ".env" ]; then
    echo "🔗 Creating symlink to .env file..."
    ln -sf "${PROJECT_ROOT}/.env" .env
fi

# Load environment variables (ignoring comments and empty lines)
echo "📚 Loading environment variables..."
while IFS= read -r line; do
    # Skip comments and empty lines
    [[ $line =~ ^#.*$ ]] && continue
    [[ -z $line ]] && continue
    
    # Export the variable
    export "$line"
done < <(grep -v '^#' "${PROJECT_ROOT}/.env" | grep -v '^$')

echo "🔍 Environment variables loaded. To test, run in a new terminal:"
echo "cd ${PROJECT_ROOT} && while IFS= read -r line; do [[ \$line =~ ^#.*$ ]] && continue; [[ -z \$line ]] && continue; export \"\$line\"; done < <(grep -v '^#' .env | grep -v '^$') && curl -X POST \"http://localhost:8000/events/search?query=Boston%20Marathon\" -H \"Authorization: Bearer \$RUNON_CLIENT_ID\" -H \"Content-Type: application/json\""

# Clean up existing virtual environment
if [ -d "venv" ]; then
    echo "🧹 Removing existing virtual environment..."
    rm -rf venv
    echo "✅ Existing virtual environment removed"
fi

# Create new virtual environment
echo "🔨 Creating new virtual environment..."
python3.9 -m venv venv
echo "✅ Virtual environment created"

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt
echo "✅ Dependencies installed"

# Export environment variables
echo "🔑 Exporting environment variables..."
while IFS= read -r line; do
    [[ $line =~ ^#.*$ ]] && continue
    [[ -z $line ]] && continue
    export "$line"
    # Print masked value for debugging
    key=$(echo "$line" | cut -d'=' -f1)
    echo "Exported $key=********"
done < <(grep -v '^#' ../.env | grep -v '^$')
echo "✅ Environment variables exported"

# Kill any existing uvicorn processes
echo "🧹 Cleaning up any existing server processes..."
pkill -f "uvicorn main:app" || true
sleep 2

# Run the server with environment variables
echo "🚀 Starting local server..."
PYTHONPATH=$PYTHONPATH:$(pwd) uvicorn main:app --reload --host 0.0.0.0 --port 8000 