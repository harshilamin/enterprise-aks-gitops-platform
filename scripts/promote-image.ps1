param(
    [Parameter(Mandatory)]
    [ValidateSet("set", "promote", "status")]
    [string]$Command,

    [ValidateSet("dev", "qa", "prod")]
    [string]$Environment,

    [ValidateSet("dev", "qa", "prod")]
    [string]$FromEnvironment,

    [ValidateSet("dev", "qa", "prod")]
    [string]$ToEnvironment,

    [string]$ImageRepository,

    [string]$Digest,

    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$arguments = @(
    ".\scripts\promote_image.py",
    "--repository-root",
    ".",
    $Command
)

switch ($Command) {
    "set" {
        if (-not $Environment -or -not $ImageRepository -or -not $Digest) {
            throw "set requires -Environment, -ImageRepository, and -Digest."
        }

        $arguments += @(
            "--environment", $Environment,
            "--image-repository", $ImageRepository,
            "--digest", $Digest
        )
    }

    "promote" {
        if (-not $FromEnvironment -or -not $ToEnvironment) {
            throw "promote requires -FromEnvironment and -ToEnvironment."
        }

        $arguments += @(
            "--from-environment", $FromEnvironment,
            "--to-environment", $ToEnvironment
        )
    }
}

if ($DryRun) {
    $arguments += "--dry-run"
}

python @arguments

if ($LASTEXITCODE -ne 0) {
    throw "Image promotion failed with exit code $LASTEXITCODE."
}
