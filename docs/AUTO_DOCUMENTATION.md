# Auto-Documentation Setup Guide

## 🤖 Automated Documentation Generation

This project uses LlamaIndex's CodeHierarchyNodeParser to automatically generate and maintain API documentation. Here are three ways to keep documentation updated automatically:

## Option 1: Git Hooks (Recommended for Local Development)

### Quick Setup
```bash
# Run the setup script
./scripts/setup_auto_docs.sh
```

This installs two Git hooks:
- **pre-commit**: Regenerates docs before every commit
- **post-merge**: Updates docs after pulling changes

### Manual Setup
```bash
# Create pre-commit hook
echo '#!/bin/sh
python src/core/auto_docs.py generate
git add docs/API_REFERENCE.md' > .git/hooks/pre-commit

chmod +x .git/hooks/pre-commit
```

### Benefits
- ✅ Zero manual intervention
- ✅ Docs always match committed code
- ✅ Works offline
- ✅ No external dependencies

## Option 2: GitHub Actions (CI/CD)

Already configured in `.github/workflows/auto-docs.yml`

### How it works:
1. Triggers on push/PR to main branch
2. Only runs when Python files change
3. Auto-commits updated documentation
4. Pushes back to repository

### Benefits
- ✅ Works for all contributors
- ✅ Centralized automation
- ✅ Consistent environment
- ✅ Visible in PR checks

## Option 3: File Watcher (Real-time Updates)

### Using watchdog (Python)
```bash
pip install watchdog

# Create watcher script
cat > scripts/watch_docs.py << 'EOF'
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time

class DocUpdateHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"Python file changed: {event.src_path}")
            subprocess.run(['python', 'src/core/auto_docs.py', 'generate'])

observer = Observer()
observer.schedule(DocUpdateHandler(), 'src', recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
EOF

python scripts/watch_docs.py
```

### Using fswatch (macOS/Linux)
```bash
# Install fswatch
brew install fswatch  # macOS
# or
apt-get install fswatch  # Linux

# Watch and regenerate
fswatch -o src/**/*.py | xargs -n1 -I{} python src/core/auto_docs.py generate
```

### Benefits
- ✅ Instant updates
- ✅ See changes immediately
- ✅ Great for development

## Option 4: IDE Integration

### VS Code Task
Add to `.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Update Documentation",
      "type": "shell",
      "command": "python src/core/auto_docs.py generate",
      "runOptions": {
        "runOn": "folderOpen"
      },
      "problemMatcher": []
    }
  ]
}
```

### VS Code Extension
Install "Run on Save" extension and add to `.vscode/settings.json`:
```json
{
  "runOnSave.commands": [
    {
      "match": ".*\\.py$",
      "command": "python src/core/auto_docs.py generate",
      "runIn": "backend"
    }
  ]
}
```

## Manual Commands

When needed, you can always run manually:

```bash
# Generate full documentation
python src/core/auto_docs.py generate

# Extract function signatures only
python src/core/auto_docs.py functions

# Refresh changed files (when implemented)
python src/core/auto_docs.py refresh
```

## How It Works

1. **CodeHierarchyNodeParser** parses all Python files
2. Extracts functions, classes, and docstrings
3. Generates markdown documentation
4. Saves to `docs/API_REFERENCE.md`

## Requirements

- Python 3.11+
- LlamaIndex installed
- `.env` file with API keys (for refresh feature)

## Disabling Automation

```bash
# Remove Git hooks
rm .git/hooks/pre-commit .git/hooks/post-merge

# Disable GitHub Actions
# Comment out the workflow in .github/workflows/auto-docs.yml
```

## Best Practices

1. **Use Git Hooks** for local development
2. **Use GitHub Actions** for team projects
3. **Use File Watcher** during active development
4. **Commit docs separately** if they're large

## Troubleshooting

### Documentation not updating?
```bash
# Check if hook is executable
ls -la .git/hooks/pre-commit

# Test generation manually
python src/core/auto_docs.py generate

# Check for errors
git commit --no-verify  # Skip hooks temporarily
```

### Generation fails?
```bash
# Check dependencies
pip install llama-index

# Verify imports
python -c "from llama_index.packs.code_hierarchy import CodeHierarchyNodeParser"
```

---

Choose the automation method that best fits your workflow. The Git hooks approach is recommended for most use cases as it requires zero configuration after initial setup.