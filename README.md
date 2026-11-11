# Devcontainer for WasmEdge

> [!WARNING]
> **Work in Progress**

This repository owns the Dockerfiles, dependency scripts, Bake definitions,
and image-building workflow for reusable WasmEdge development environments.
The consolidated `.github/workflows/docker.yml` builds CI base, Ubuntu,
manylinux, and Alpine LLD dependency images. Static-build and legacy definitions
are retained, but CI does not build them or OpenWrt images.

## Layout

| Path | Contents |
| --- | --- |
| `.devcontainer/` | Development environment for `WasmEdge/devcontainer`. |
| `Dockerfile.*` | WasmEdge development, CI, plugin, static, legacy, and release image definitions. |
| `docker-bake.*.hcl` | Docker Buildx Bake definitions for CI-built image families and retained Alpine/Debian static builds. |
| `SHA256SUM.*` | Checksums used by the manylinux image definitions. |
| `build-manylinux.sh` | Legacy manylinux image build helper. |
| `scripts/` | Dockerfile-consumed dependency installers, build helpers, test data helpers, and patches, grouped by dependency family. |
| `.github/workflows/` | Consolidated image build/publication workflow (`docker.yml`) and repository lint workflow (`super-linter.yml`). |
