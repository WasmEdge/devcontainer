"""Small GHCR publication contract tests."""

import importlib.util
from pathlib import Path
import subprocess
import unittest


MODULE = Path(__file__).resolve().parents[3] / ".github/scripts/devcontainer/publication.py"


def load_module():
    spec = importlib.util.spec_from_file_location("publication", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.publication = load_module()
        self.source = "a" * 40

    def test_durable_tag_contains_source_run_and_attempt(self):
        self.assertEqual(
            self.publication.durable_tag(self.source, 44964975569, 2),
            "build-" + self.source + "-run-44964975569-attempt-2",
        )

    def test_candidate_tag_uses_pr_merge_sha_run_and_attempt(self):
        self.assertEqual(
            self.publication.candidate_tag(123, self.source, 44964975569, 2),
            "pr-123-" + self.source + "-run-44964975569-attempt-2",
        )

    def test_tags_reject_invalid_identity(self):
        for function, args in (
            (self.publication.durable_tag, ("bad", 1, 1)),
            (self.publication.candidate_tag, (0, self.source, 1, 1)),
            (self.publication.candidate_tag, (123, "bad", 1, 1)),
            (self.publication.durable_tag, (self.source, 0, 1)),
        ):
            with self.assertRaises(ValueError):
                function(*args)

    def test_digest_validation(self):
        digest = "sha256:" + "1" * 64
        self.assertEqual(self.publication.validate_digest(digest), digest)
        for value in ("", "sha256:bad", "sha256:" + "1" * 63):
            with self.assertRaises(ValueError):
                self.publication.validate_digest(value)

    def test_validate_digest_cli_accepts_valid_digest(self):
        digest = "sha256:" + "1" * 64
        result = subprocess.run(
            ["python3", str(MODULE), "validate-digest", "--digest", digest],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_validate_digest_cli_rejects_invalid_digest(self):
        result = subprocess.run(
            ["python3", str(MODULE), "validate-digest", "--digest", "sha256:bad"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)

    def test_index_requires_exactly_amd64_and_arm64(self):
        index = {"manifests": [
            {"digest": "sha256:" + "1" * 64,
             "platform": {"os": "linux", "architecture": "amd64"}},
            {"digest": "sha256:" + "2" * 64,
             "platform": {"os": "linux", "architecture": "arm64"}},
        ]}
        self.assertEqual(self.publication.verify_index(index), {
            "linux/amd64": "sha256:" + "1" * 64,
            "linux/arm64": "sha256:" + "2" * 64,
        })
        index_with_attestation = {
            "manifests": index["manifests"] + [{
                "digest": "sha256:" + "3" * 64,
                "mediaType": "application/vnd.oci.image.manifest.v1+json",
                "platform": {"os": "unknown", "architecture": "unknown"},
                "annotations": {
                    "vnd.docker.reference.type": "attestation-manifest",
                },
            }],
        }
        self.assertEqual(self.publication.verify_index(index_with_attestation), {
            "linux/amd64": "sha256:" + "1" * 64,
            "linux/arm64": "sha256:" + "2" * 64,
        })
        for manifests in (index["manifests"][:1], index["manifests"] + [index["manifests"][0]],
                          index["manifests"] + [{"digest": "sha256:" + "3" * 64,
                          "platform": {"os": "linux", "architecture": "s390x"}}]):
            with self.assertRaises(ValueError):
                self.publication.verify_index({"manifests": manifests})


if __name__ == "__main__":
    unittest.main()
