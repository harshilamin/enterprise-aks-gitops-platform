# Development Desired State

Development uses automatic Argo CD synchronization, pruning, and self-healing.

The initial image value uses the local portfolio tag so the chart remains easy to demonstrate. After publishing the image to a registry, use `scripts/promote-image.py set` to replace the tag with an immutable digest.
