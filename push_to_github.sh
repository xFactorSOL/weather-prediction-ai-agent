#!/bin/bash
# Helper script to push to GitHub with authentication

echo "🔐 GitHub Authentication Helper"
echo "================================"
echo ""
echo "If you have a Personal Access Token, paste it below."
echo "If not, get one at: https://github.com/settings/tokens"
echo ""
read -sp "Enter your GitHub Personal Access Token: " TOKEN
echo ""

if [ -z "$TOKEN" ]; then
    echo "❌ No token provided. Exiting."
    exit 1
fi

# Set remote with token
git remote set-url origin https://${TOKEN}@github.com/xfactorSOL/weather-prediction-ai-agent.git

echo "✅ Remote configured with token"
echo "🚀 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "📍 Repository: https://github.com/xfactorSOL/weather-prediction-ai-agent"
else
    echo ""
    echo "❌ Push failed. Check your token and repository access."
fi
