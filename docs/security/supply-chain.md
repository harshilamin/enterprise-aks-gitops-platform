# Software Supply-Chain Security

The release workflow builds an immutable image, blocks critical vulnerabilities, creates a CycloneDX SBOM, signs the image with GitHub OIDC through Cosign, attaches the SBOM as an attestation, and verifies the signing identity.

Production policy begins in `Audit` mode so violations can be observed before enforcement. The production image policy requires a `sha256` digest.
