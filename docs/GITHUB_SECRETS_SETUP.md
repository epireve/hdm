# Setting Up GitHub Secrets for Turso Database

This guide explains how to set up the required GitHub secrets for the HDM Research Database visualization.

## Required Secrets

You need to add two secrets to your GitHub repository:
- `TURSO_DATABASE_URL`: Your Turso database URL
- `TURSO_AUTH_TOKEN`: Your Turso authentication token

## Steps to Add Secrets

1. **Go to your repository on GitHub**
   - Navigate to https://github.com/epireve/hdm

2. **Access Repository Settings**
   - Click on "Settings" tab in your repository
   - In the left sidebar, expand "Secrets and variables"
   - Click on "Actions"

3. **Add Repository Secrets**
   - Click "New repository secret"
   - For the first secret:
     - Name: `TURSO_DATABASE_URL`
     - Value: Your database URL (e.g., `libsql://hdm-research-tracker-epireve.aws-ap-northeast-1.turso.io`)
   - Click "Add secret"
   
   - Click "New repository secret" again
   - For the second secret:
     - Name: `TURSO_AUTH_TOKEN`
     - Value: Your authentication token (the long JWT token)
   - Click "Add secret"

4. **Verify GitHub Actions**
   - Go to the "Actions" tab in your repository
   - You should see a workflow called "Deploy to GitHub Pages"
   - If it's not running, click on it and select "Run workflow"

5. **Enable GitHub Pages**
   - Go to Settings → Pages
   - Under "Source", select "GitHub Actions"
   - Save the changes

## How It Works

1. When you push to the `main` branch, GitHub Actions runs automatically
2. The workflow creates a `config.js` file with your secrets
3. The file is included in the GitHub Pages deployment
4. Your visualization page can then access the database

## Troubleshooting

- **"Database configuration not found" error**: The GitHub Actions workflow hasn't run yet. Wait a few minutes after pushing.
- **Workflow not running**: Check the Actions tab for any errors
- **Still not working**: Verify your secret names match exactly (case-sensitive)

## Local Development

For local development, create a `visualization/js/config.js` file:

```javascript
window.TURSO_CONFIG = {
    DATABASE_URL: 'your-database-url',
    AUTH_TOKEN: 'your-auth-token'
};
```

This file is gitignored and won't be committed to the repository.