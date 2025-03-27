# Docker Build Setup for AnswerAI

This document provides instructions for setting up GitHub Actions to build and push Docker images for AnswerAI (white-labeled version of OpenWebUI).

## Repository Setup

### 1. Enable GitHub Packages

First, ensure that GitHub Packages is enabled for your repository:

1. Go to your repository on GitHub
2. Click on "Settings"
3. Navigate to "Packages" in the left sidebar
4. Ensure that "Enable improved container support" is checked

### 2. Configure Repository Permissions

To allow GitHub Actions to push to the GitHub Container Registry (ghcr.io), you need to configure the proper permissions:

1. Go to your repository on GitHub
2. Click on "Settings"
3. Navigate to "Actions" > "General" in the left sidebar
4. Under "Workflow permissions", select "Read and write permissions"
5. Save the changes

### 3. Create a Personal Access Token (Optional)

If you continue to face permission issues, you can create a Personal Access Token (PAT) with the necessary permissions:

1. Go to your GitHub profile settings
2. Navigate to "Developer settings" > "Personal access tokens" > "Tokens (classic)"
3. Click "Generate new token"
4. Give it a descriptive name like "Docker Image Push"
5. Select the following scopes:
   - `repo` (all)
   - `write:packages`
   - `read:packages`
   - `delete:packages`
6. Click "Generate token"
7. Copy the token and store it securely

### 4. Add the PAT to Repository Secrets (Optional)

1. Go to your repository on GitHub
2. Click on "Settings"
3. Navigate to "Secrets and variables" > "Actions" in the left sidebar
4. Click "New repository secret"
5. Name: `GITHUB_PAT`
6. Value: Paste the PAT you generated
7. Click "Add secret"

### 5. Update the Workflow File (Optional)

If you're using a PAT, update the workflow file (`.github/workflows/docker-build.yml`):

```yaml
- name: Log in to the Container registry
  uses: docker/login-action@v3
  with:
    registry: ${{ env.REGISTRY }}
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_PAT }}
```

## Running the Workflow

The workflow will automatically run when you push to the `websu` branch. You can also manually trigger it:

1. Go to your repository on GitHub
2. Click on "Actions"
3. Select the "Build and Push Docker Image" workflow
4. Click "Run workflow"
5. Select the `websu` branch
6. Click "Run workflow"

## Using the Docker Image

Once the workflow completes successfully, you can pull and run the Docker image:

```bash
docker pull ghcr.io/your-username/open-webui:websu
docker run -p 8080:8080 ghcr.io/your-username/open-webui:websu
```

Replace `your-username` with your GitHub username.