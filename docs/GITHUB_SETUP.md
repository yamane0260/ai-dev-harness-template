# GitHub Setup

Recommended repository: private `ai-dev-harness-template`, then enable GitHub's **Template repository** setting.

## If you downloaded the clean ZIP

```sh
cd ai-dev-harness-template
git init -b main
git add .
git commit -m "Initial AI development harness template"
gh auth login
gh repo create ai-dev-harness-template --private --source . --remote origin --push
```

## If you cloned the provided Git bundle

```sh
git clone ai-dev-harness-template.bundle ai-dev-harness-template
cd ai-dev-harness-template
git remote remove origin
gh auth login
gh repo create ai-dev-harness-template --private --source . --remote origin --push
```

Then enable **Template repository** in GitHub repository **Settings > General**.

For each real project, create a new repository from the template, run the `bootstrap-project` skill, and configure branch/ruleset settings so the `verify` Actions check is required before merge where your GitHub plan supports it.
