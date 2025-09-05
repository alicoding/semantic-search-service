#!/bin/bash
# Setup automatic documentation generation via Git hooks

echo "🔧 Setting up automatic documentation generation..."

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
# Auto-generate API documentation before each commit
echo "📚 Auto-generating API documentation..."
python src/core/auto_docs.py generate
if [ $? -eq 0 ]; then
    git add docs/API_REFERENCE.md
    echo "✅ Documentation updated and added to commit"
else
    echo "⚠️ Documentation generation failed, continuing with commit"
fi
exit 0
EOF

# Create post-merge hook
cat > .git/hooks/post-merge << 'EOF'
#!/bin/sh
# Auto-generate API documentation after pulling changes
echo "📚 Updating API documentation after merge..."
python src/core/auto_docs.py generate
if [ $? -eq 0 ]; then
    echo "✅ Documentation updated with latest changes"
else
    echo "⚠️ Documentation generation failed"
fi
exit 0
EOF

# Make hooks executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/post-merge

echo "✅ Git hooks installed successfully!"
echo ""
echo "Documentation will now auto-generate:"
echo "  - Before every commit (pre-commit hook)"
echo "  - After every pull/merge (post-merge hook)"
echo ""
echo "To disable, run: rm .git/hooks/pre-commit .git/hooks/post-merge"