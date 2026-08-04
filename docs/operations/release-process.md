# Release Process

After all checks pass and the pull request is merged:

```powershell
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release v1.0.0: repository foundation"
git push origin v1.0.0
```

Every release requires an updated changelog, documentation, successful checks, and a documented rollback path.
