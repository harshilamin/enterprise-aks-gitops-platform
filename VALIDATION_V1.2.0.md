# v1.2.0 Validation Notes

The generated overlay was checked for:

- YAML syntax in static values and workflow files
- JSON syntax in `values.schema.json`
- Python syntax in the rendered-manifest validator
- MkDocs navigation references after merging with the v1.0.0 and v1.1.0 packages
- Required chart files and template delimiters
- No application-source changes

Actual Helm rendering, Kubeconform schema checks, and chart packaging must run locally or in GitHub Actions because Helm and Docker are not available in the generation environment.
