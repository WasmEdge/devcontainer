# Devcontainer for WasmEdge

> [!WARNING]
> **Work in Progress**

This repository owns the Dockerfiles, dependency scripts, Bake definitions,
and GitHub Actions workflows used to build and validate WasmEdge development,
CI, static-library, and OpenWrt images.

## Layout

| Path | Contents |
| --- | --- |
| `.devcontainer/` | Development environment for `WasmEdge/devcontainer`. |
| `Dockerfile.*` | WasmEdge development, CI, plugin, static, legacy, and release image definitions. |
| `docker-bake.*.hcl` | Docker Buildx Bake definitions for the actively built image families. |
| `SHA256SUM.*` | Checksums used by the manylinux image definitions. |
| `build-manylinux.sh` | Legacy manylinux image build helper. |
| `scripts/` | Dockerfile-consumed dependency installers, build helpers, test data helpers, and patches, grouped by dependency family. |
| `.github/workflows/` | Image, static-library, and OpenWrt build and validation workflows. |
