group "default" {
  targets = ["cross"]
}

target "base" {
  dockerfile = "./Dockerfile.debian-static"
  context    = "."
  output     = ["build"]
}

target "cross" {
  inherits  = ["base"]
  platforms = [
    "linux/amd64",
    "linux/arm64"
  ]
}
