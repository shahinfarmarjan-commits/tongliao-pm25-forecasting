# Publish this repository

The local repository is already initialized and committed. To publish it under your GitHub account, open PowerShell in this folder and run:

```powershell
gh auth login
gh repo create tongliao-pm25-forecasting --public --source=. --remote=origin --push
```

The repository was prepared as a public sanitized release. It excludes raw monitoring data, private correspondence, temporary files, credentials, unfinished working folders, and exact location details.
