group "default" {
  targets = ["cross"]
}

target "base" {
  dockerfile = "Dockerfile.alpine-static"
  context    = "."
  contexts   = {
    source = "../WasmEdge-0.18.1"
    "wasmedge/wasmedge:alpine-base-3.23" = "target:alpine-base"
  }
  output     = ["build"]
}

target "alpine-base" {
  dockerfile = "Dockerfile.alpine-base"
  context    = "."
  platforms  = ["linux/amd64", "linux/arm64"]
  tags       = ["wasmedge/wasmedge:alpine-base-3.23"]
}

target "cross" {
  inherits  = ["base"]
  platforms = [
    "linux/amd64",
    "linux/arm64"
  ]
}
