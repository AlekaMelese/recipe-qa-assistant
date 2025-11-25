# GitHub Setup and Push Guide

This guide will help you push your Recipe Q&A Assistant project to GitHub.

## 📋 Prerequisites

1. **GitHub Account**: Create one at [github.com](https://github.com) if you don't have one
2. **Git Installed**: Check with `git --version`
3. **SSH Key or Personal Access Token** (for authentication)

## 🚀 Step-by-Step Instructions

### Step 1: Create a New Repository on GitHub

1. Go to [github.com](https://github.com) and log in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in the details:
   - **Repository name**: `recipe-qa-assistant` (or your preferred name)
   - **Description**: `Conversational Recipe Q&A Assistant using RAG with TF-IDF and Claude 3 Haiku`
   - **Visibility**: Choose **Public** or **Private**
   - **DO NOT** initialize with README (we already have one)
   - **DO NOT** add .gitignore or license yet
4. Click **"Create repository"**

### Step 2: Prepare Your Local Repository

Navigate to your project directory:

```bash
cd /scratch/aayalew25/Food/FoodNew/Project
```

### Step 3: Initialize Git Repository

If not already initialized:

```bash
# Initialize git repository
git init

# Check status
git status
```

### Step 4: Remove API Keys from Code (IMPORTANT!)

**⚠️ SECURITY WARNING**: Never commit API keys to GitHub!

Before pushing, you need to remove your API key from the code files:

#### Files to edit:

1. **src/conversation_handler.py** (lines 145-146)
2. **src/rag_pipeline.py** (lines 261-262)
3. **src/run_all_tests.py** (check for hardcoded API keys)
4. **src/baseline_comparison.py** (check for hardcoded API keys)

#### Remove the API key:

```bash
# Edit each file and replace hardcoded API key with environment variable

# Example for conversation_handler.py:
# BEFORE:
# api_key = "YOUR-API-KEY-REMOVED"

# AFTER:
# import os
# api_key = os.getenv("ANTHROPIC_API_KEY")
# if not api_key:
#     raise ValueError("Please set ANTHROPIC_API_KEY environment variable")
```

#### Quick script to remove API keys:

```bash
cd src

# Backup files first
cp conversation_handler.py conversation_handler.py.backup
cp rag_pipeline.py rag_pipeline.py.backup

# Use sed to replace API key (run this carefully!)
# This is just an example - you should manually review each file
```

**Or manually edit these files before committing!**

### Step 5: Add Files to Git

```bash
# Add all files
git add .

# Check what will be committed
git status

# If you see files that shouldn't be committed (like API keys), remove them:
# git reset HEAD <file-to-remove>
```

### Step 6: Create First Commit

```bash
git commit -m "Initial commit: Recipe Q&A Assistant with RAG

- Implemented TF-IDF retrieval system (NDCG@3: 0.814)
- Integrated Claude 3 Haiku for natural language generation
- Added conversation handler with clarification support
- Included evaluation metrics and baseline comparison
- Complete documentation and project report"
```

### Step 7: Configure Remote Repository

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/recipe-qa-assistant.git

# Or using SSH (if you have SSH key set up):
# git remote add origin git@github.com:YOUR_USERNAME/recipe-qa-assistant.git

# Verify remote
git remote -v
```

### Step 8: Push to GitHub

#### Option A: Using HTTPS (requires Personal Access Token)

```bash
# Set default branch name to main
git branch -M main

# Push to GitHub
git push -u origin main
```

You'll be prompted for:
- **Username**: Your GitHub username
- **Password**: Your Personal Access Token (NOT your GitHub password)

**To create a Personal Access Token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name (e.g., "Recipe QA Project")
4. Select scopes: `repo` (full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

#### Option B: Using SSH (if you have SSH key configured)

```bash
git branch -M main
git push -u origin main
```

### Step 9: Verify Upload

1. Go to your repository on GitHub: `https://github.com/YOUR_USERNAME/recipe-qa-assistant`
2. You should see all your files including:
   - README.md (will display on the main page)
   - src/ folder with all Python scripts
   - evaluation/ folder with results
   - All documentation files

### Step 10: Update README with Your Information

On GitHub, you can edit README.md directly:

1. Click on `README.md`
2. Click the pencil icon (Edit this file)
3. Update:
   - Replace `[Your Name]` with your actual name
   - Replace `[your-email@example.com]` with your email
   - Replace `[@your-username]` with your GitHub username
   - Update the clone URL in the Quick Start section
4. Commit changes

Or edit locally and push:

```bash
# Edit README.md locally
nano README.md  # or use your preferred editor

# Commit and push
git add README.md
git commit -m "Update README with personal information"
git push
```

## 🔒 Security Best Practices

### 1. Never Commit API Keys

Always use environment variables:

```python
import os

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Please set ANTHROPIC_API_KEY environment variable")
```

### 2. Use .gitignore

The `.gitignore` file is already created. It prevents:
- API keys and secrets
- Python cache files
- Large CSV files
- Environment variables

### 3. If You Accidentally Committed an API Key

**⚠️ IMMEDIATELY:**

1. **Revoke the API key** on Anthropic's website
2. Remove from Git history:

```bash
# Install BFG Repo-Cleaner or use git filter-branch
# This is complex - better to delete repo and start fresh

# Simpler approach: Delete the GitHub repo and recreate it
```

3. Generate a new API key
4. Never hardcode it again!

## 📝 Adding a Description to Your GitHub Repository

### Method 1: On GitHub Website

1. Go to your repository
2. Click the **⚙️ Settings** icon (top right, near "About")
3. In the "Description" field, add:
   ```
   Conversational Recipe Q&A Assistant using RAG with TF-IDF retrieval and Claude 3 Haiku. Achieves NDCG@3: 0.814 and Recall@3: 0.869. Built for NLP course project.
   ```
4. Click "Save changes"

### Method 2: Add Topics (Tags)

In the same "About" section, add topics:
- `nlp`
- `rag`
- `recipe-search`
- `conversational-ai`
- `claude`
- `tfidf`
- `python`
- `machine-learning`

## 🎨 Optional: Make Your Repository Look Professional

### 1. Add a License

```bash
# Create LICENSE file
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

git add LICENSE
git commit -m "Add MIT license"
git push
```

### 2. Add Project Images (Optional)

If you have screenshots or diagrams:

```bash
# Create images folder
mkdir -p images

# Add your images (screenshots, architecture diagrams, etc.)
# Then commit:
git add images/
git commit -m "Add project screenshots"
git push
```

Update README.md to include images:

```markdown
## Screenshots

![System Architecture](images/architecture.png)
![Demo Screenshot](images/demo.png)
```

### 3. Pin Important Files

On GitHub, you can create a GitHub Pages site or pin important notebooks.

## 🔄 Future Updates

When you make changes to your project:

```bash
# 1. Make your changes to files

# 2. Stage changes
git add .

# 3. Commit with descriptive message
git commit -m "Add feature: multi-language support"

# 4. Push to GitHub
git push
```

## 📚 Useful Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature-branch

# Switch branches
git checkout main

# Pull latest changes
git pull origin main

# View differences
git diff

# Undo unstaged changes
git checkout -- <file>

# Remove file from staging
git reset HEAD <file>
```

## 🆘 Troubleshooting

### Problem: "Permission denied (publickey)"

**Solution**: Use HTTPS instead of SSH, or set up SSH keys:

```bash
# Switch to HTTPS
git remote set-url origin https://github.com/YOUR_USERNAME/recipe-qa-assistant.git
```

### Problem: "Large file" error

**Solution**: The Recipes.csv file is too large for GitHub. It's already in `.gitignore`, but if you accidentally added it:

```bash
# Remove from staging
git rm --cached Final/Recipes.csv

# Or remove data/recipes_subset.json if it's too large
git rm --cached data/recipes_subset.json

# Commit and push
git commit -m "Remove large files"
git push
```

Consider using **Git LFS** (Large File Storage) for large files or hosting them elsewhere.

### Problem: "Failed to push"

**Solution**: Pull first, then push:

```bash
git pull origin main --rebase
git push origin main
```

### Problem: "Repository already exists"

**Solution**: If you accidentally initialized twice:

```bash
# Remove .git folder and start over
rm -rf .git
git init
# Follow steps again
```

## ✅ Final Checklist

Before pushing to GitHub, ensure:

- [ ] All API keys are removed from code
- [ ] `.gitignore` file is present
- [ ] README.md is complete and informative
- [ ] All files are committed
- [ ] Personal information is updated in README
- [ ] Repository description is added on GitHub
- [ ] Topics/tags are added
- [ ] License is included (optional but recommended)

## 🎓 Sharing Your Project

After pushing to GitHub, you can share your project:

1. **Add to Resume/CV**: Link to GitHub repo
2. **Share on LinkedIn**: Post about your project with GitHub link
3. **Include in Portfolio**: Add to personal website
4. **Submit for Course**: Share GitHub URL with instructor

Your repository URL will be:
```
https://github.com/YOUR_USERNAME/recipe-qa-assistant
```

## 📖 Additional Resources

- [GitHub Docs](https://docs.github.com/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Desktop](https://desktop.github.com/) - GUI alternative to command line
- [GitKraken](https://www.gitkraken.com/) - Another Git GUI tool

---

**Happy Coding! 🚀**

If you have any questions, refer to GitHub documentation or your course instructor.
