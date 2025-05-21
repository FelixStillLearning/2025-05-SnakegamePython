#!/bin/bash

# Initialize Git repository
echo "Initializing Git repository..."
git init

# Add all files to the repository
echo "Adding files to repository..."
git add .

# Make the initial commit
echo "Making initial commit..."
git commit -m "Initial commit of Python Snake Game with Pixel Art"

echo ""
echo "Repository is ready! You can now:"
echo "1. Create a new repository on GitHub (without initializing it)"
echo "2. Connect your local repository with the following commands:"
echo ""
echo "   git remote add origin https://github.com/YourUsername/python-snake-game.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "Replace 'YourUsername' with your actual GitHub username and 'python-snake-game'"
echo "with your preferred repository name."
