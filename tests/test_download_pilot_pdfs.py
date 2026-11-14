"""Unit tests for the official pilot PDF downloader."""
import unittest

from scripts.download_pilot_pdfs import is_official_url, is_pdf_payload, sha256_bytes


class DownloadPilotPdfsTests(unittest.TestCase):
    def test_only_https_official_host_is_allowed(self):
        self.assertTrue(is_official_url("https://gate2026.iitg.ac.in/doc/file.pdf"))
        self.assertFalse(is_official_url("http://gate2026.iitg.ac.in/doc/file.pdf"))
        self.assertFalse(is_official_url("https://example.com/file.pdf"))
        self.assertFalse(is_official_url("https://gate2026.iitg.ac.in.example.com/file.pdf"))

    def test_pdf_magic_header_is_required(self):
        self.assertTrue(is_pdf_payload(b"%PDF-1.7\\nbody"))
        self.assertFalse(is_pdf_payload(b"<!doctype html>"))
        self.assertFalse(is_pdf_payload(b""))

    def test_sha256_is_deterministic(self):
        self.assertEqual(
            sha256_bytes(b"abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        )


if __name__ == "__main__":
    unittest.main()
