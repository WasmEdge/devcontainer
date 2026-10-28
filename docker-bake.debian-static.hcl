group "default" {
  targets = ["cross"]
}

target "base" {
  dockerfile = "Dockerfile.debian-static"
  context    = "."
  contexts   = {
    source = "../WasmEdge-0.18.1"
  }
  output     = ["build"]
}

target "cross" {
  inherits  = ["base"]
  platforms = [
    "linux/amd64",
    "linux/arm64"
  ]
}
