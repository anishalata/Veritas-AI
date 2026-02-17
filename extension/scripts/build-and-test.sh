#!/bin/bash

# Build and test script for Veritas AI extension

echo "🔨 Building Veritas AI extension..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "📦 Extension built to: extension/dist/"
    echo ""
    echo "🚀 Next steps:"
    echo "1. Open Chrome and navigate to chrome://extensions/"
    echo "2. Enable 'Developer mode' (toggle in top-right)"
    echo "3. Click 'Load unpacked'"
    echo "4. Select the 'dist' folder from: $(pwd)/dist"
    echo ""
    echo "🧪 To test:"
    echo "- Navigate to any news article"
    echo "- Click the Veritas AI extension icon"
    echo "- Click 'Analyze Article'"
    echo ""
else
    echo "❌ Build failed. Check errors above."
    exit 1
fi
