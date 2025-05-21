# GitHub Upload Instructions

Follow these steps to upload your Python Snake Game to GitHub:

## Prerequisites
- Make sure Git is installed on your system
- Have a GitHub account

## Steps

1. **Initialize a Git repository in your project folder**
   ```
   cd "d:\Development\Eksperimen\2025-05-SnakegamePython"
   git init
   ```

2. **Add all files to the repository**
   ```
   git add .
   ```

3. **Make the initial commit**
   ```
   git commit -m "Initial commit of Python Snake Game with Pixel Art"
   ```

4. **Create a new repository on GitHub**
   - Go to [GitHub](https://github.com/)
   - Click on the "+" in the top right corner
   - Select "New repository"
   - Name your repository (e.g., "python-snake-game")
   - Provide a description (optional)
   - Do NOT initialize with README, .gitignore, or license
   - Click "Create repository"

5. **Connect your local repository with GitHub**
   ```
   git remote add origin https://github.com/YourUsername/python-snake-game.git
   git branch -M main
   git push -u origin main
   ```
   (Replace 'YourUsername' with your GitHub username and 'python-snake-game' with your repository name)

## Subsequent Changes

After making changes to your code:
1. Stage changes:
   ```
   git add .
   ```
2. Commit changes:
   ```
   git commit -m "Description of your changes"
   ```
3. Push to GitHub:
   ```
   git push
   ```
