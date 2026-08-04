# Apply the final v2.0.0 release

## Option A: Apply the overlay to merged v1.5.0

```powershell
git checkout main
git pull origin main
git status
git checkout -b feature/release-2.0.0-final-platform
```

Extract `enterprise-aks-gitops-platform-v2.0.0-overlay.zip` into a temporary
folder. Copy its contents into the repository root and allow existing files to
be replaced.

## Option B: Use the complete snapshot

Extract `enterprise-aks-gitops-platform-v2.0.0-final.zip`. The resulting folder
contains the complete repository state, but not Git history. Use it as a clean
reference or copy its contents into the existing repository branch.

## Install dependencies

Activate the existing virtual environment or create one, then install all
repository validation dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pip install -r requirements-docs.txt
python -m pip install -r requirements-helm.txt
python -m pip install -r requirements-gitops.txt
python -m pip install -r requirements-identity.txt
python -m pip install -r requirements-observability.txt
python -m pip install -r requirements-final.txt
```

Helm and Docker must also be available on the workstation. Live platform tests
require `kubectl`, Azure CLI, and access to the intended AKS cluster.

## Format and validate

```powershell
python -m ruff format .
python -m ruff check . --fix

python -m ruff format --check .
python -m ruff check .
python -m mypy apps\sample-api\src
python -m pytest

powershell.exe -ExecutionPolicy Bypass `
  -File .\scripts\validate-v2.0.0.ps1
```

The complete validation script runs the previous release validation layers,
final environment contracts, Helm composition, GitOps checks, identity,
observability, and the strict MkDocs build.

## Review generated output

Generated directories and coverage files must remain untracked:

```powershell
git status --short

git diff --cached --name-only |
  Select-String "\.rendered|site/|coverage\.xml|__pycache__|\.pytest_cache"
```

The second command should return no output after staging.

## Commit and push

```powershell
git add .
git commit -m "feat: complete enterprise AKS GitOps platform v2"
git push -u origin feature/release-2.0.0-final-platform
```

## Release

After all checks pass and the pull request is merged:

```powershell
git checkout main
git pull origin main
git tag -a v2.0.0 `
  -m "Release v2.0.0: final enterprise AKS GitOps platform"
git push origin v2.0.0
```

Use `RELEASE_NOTES_V2.0.0.md` for the GitHub Release description.
