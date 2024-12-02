# Contributing Guide for Resume Analyzer

Welcome to the Resume Analyzer contributing guide! This document provides an overview of the contribution workflow, from opening an issue and creating a pull request (PR) to reviewing and merging the PR.

## New Contributor Guide
To get an overview of the project, start by reading the [README](./README.md) file.

## Issues

### Create a New Issue
If you find a bug or have a feature request, check if an issue already exists. If it doesn’t, you can open a new issue. Provide as much detail as possible to help us understand and address the issue.

### Solve an Issue
Browse through existing issues to find one that interests you. You can filter issues by labels to find a match for your expertise. We don’t assign issues, so feel free to open a PR for any issue you’d like to work on.

## Making Changes

### Make Changes in the UI
For minor changes such as fixing typos or updating documentation, you can use the GitHub UI. Click "Edit" at the top of any documentation page to make your changes and submit a PR for review.

### Make Changes Locally
For more significant changes, follow these steps to set up a local development environment:

#### Fork the Repository
1. **Fork the Repo:** Create your own copy of the repository by forking it.
2. **Clone the Repo:** Clone your forked repository to your local machine.
   ```bash
   git clone https://github.com/your-username/resume-analyzer.git
   cd resume-analyzer
   ```
3. **Create a Branch:** Create a new branch for your changes.
   ```bash
   git checkout -b your-branch-name
   ```

#### Install Dependencies
Make sure you have the necessary dependencies installed. Use Poetry for dependency management:
```bash
pip install poetry
poetry install
```

#### Make Your Changes
Make your changes to the code or documentation.

### Commit Your Updates
Commit your changes with a clear and descriptive message.
```bash
git add .
git commit -m "Your descriptive commit message"
```

### Pull Request
1. **Push to GitHub:** Push your changes to your forked repository.
   ```bash
   git push origin your-branch-name
   ```
2. **Create a PR:** Go to the original repository and create a pull request from your branch. Fill out the PR template to help reviewers understand your changes.

3. **Link to Issues:** If your PR addresses an issue, link it in the PR description.

4. **Review Process:** A maintainer will review your PR. They may request changes, ask questions, or provide feedback. Make the necessary updates and push them to your branch.

5. **Resolve Conversations:** As you address feedback, mark each conversation as resolved.

### Your PR is Merged!
Once your PR is approved and merged, your contributions will be publicly visible. Thank you for contributing to Resume Analyzer!
