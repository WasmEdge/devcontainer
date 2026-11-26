"""Small GHCR publication contract."""

import argparse
import json
import re


SHA = re.compile(r"[0-9a-f]{40}\Z")
DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")


def _identity_tag(prefix, source_sha, run_id, attempt):
    if not SHA.fullmatch(source_sha):
        raise ValueError("Invalid source SHA")
    if type(run_id) is not int or run_id <= 0 or type(attempt) is not int or attempt <= 0:
        raise ValueError("Run identity must be positive integers")
    tag = f"{prefix}-{source_sha}-run-{run_id}-attempt-{attempt}"
    if len(tag + "-stage-amd64") > 128:
        raise ValueError("Image staging tag exceeds 128 characters")
    return tag


def durable_tag(source_sha, run_id, attempt):
    return _identity_tag("build", source_sha, run_id, attempt)


def candidate_tag(pr, source_sha, run_id, attempt):
    if type(pr) is not int or pr <= 0:
        raise ValueError("PR number must be positive")
    return _identity_tag(f"pr-{pr}", source_sha, run_id, attempt)


def validate_digest(value):
    if not isinstance(value, str) or not DIGEST.fullmatch(value):
        raise ValueError("Invalid image digest")
    return value


def verify_index(index):
    found = {}
    for descriptor in index.get("manifests", []):
        digest = validate_digest(descriptor.get("digest"))
        annotations = descriptor.get("annotations", {})
        if annotations.get("vnd.docker.reference.type") == "attestation-manifest":
            continue
        platform = descriptor.get("platform", {})
        key = f"{platform.get('os')}/{platform.get('architecture')}"
        if key not in ("linux/amd64", "linux/arm64") or key in found:
            raise ValueError("Unexpected or duplicate runnable platform")
        found[key] = digest
    if set(found) != {"linux/amd64", "linux/arm64"}:
        raise ValueError("Both native platforms are required")
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("tag", "candidate", "verify-index", "validate-digest"))
    parser.add_argument("--source-sha")
    parser.add_argument("--run-id", type=int)
    parser.add_argument("--attempt", type=int)
    parser.add_argument("--pr", type=int)
    parser.add_argument("--index")
    parser.add_argument("--digest")
    args = parser.parse_args()
    if args.command == "tag":
        print(durable_tag(args.source_sha, args.run_id, args.attempt))
    elif args.command == "candidate":
        print(candidate_tag(args.pr, args.source_sha, args.run_id, args.attempt))
    elif args.command == "validate-digest":
        validate_digest(args.digest)
    else:
        with open(args.index, encoding="utf-8") as stream:
            print(json.dumps(verify_index(json.load(stream)), sort_keys=True))


if __name__ == "__main__":
    main()
