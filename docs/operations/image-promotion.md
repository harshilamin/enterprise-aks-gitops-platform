# Immutable Image Promotion

## First registry digest

After CI publishes the application image to ACR, GHCR, or another OCI registry, set the Development digest:

```powershell
.\scripts\promote-image.ps1 `
  -Command set `
  -Environment dev `
  -ImageRepository example.azurecr.io/enterprise-aks-sample-api `
  -Digest sha256:<64-hexadecimal-characters>
```

The command:

- Sets the image repository
- Clears the mutable tag
- Sets the immutable digest
- Preserves `IfNotPresent`
- Validates the digest format

## Promote Development to QA

```powershell
.\scripts\promote-image.ps1 `
  -Command promote `
  -FromEnvironment dev `
  -ToEnvironment qa
```

## Promote QA to Production

```powershell
.\scripts\promote-image.ps1 `
  -Command promote `
  -FromEnvironment qa `
  -ToEnvironment prod
```

Promotion cannot skip QA.

## Pull-request process

1. Run the promotion command.
2. Review only the target environment values change.
3. Run GitOps validation.
4. Commit the change on a promotion branch.
5. Open a pull request.
6. Merge after checks and approval.
7. Manually synchronize QA or Production in Argo CD.

## Confirm references

```powershell
.\scripts\promote-image.ps1 -Command status
```

The source and target must show the exact same repository and SHA-256 digest.
