import unittest

from blobs import sparkline, summarize


class BlobTest(unittest.TestCase):
    def test_summarize(self):
        s = summarize({"baseFeePerBlobGas": [hex(1), hex(3), hex(2), hex(5)], "blobGasUsedRatio": [0.5, 1.0, 0.0]})
        self.assertEqual(s["next"], 5)
        self.assertEqual((s["min"], s["max"]), (1, 3))
        self.assertAlmostEqual(s["avg"], 2)
        self.assertAlmostEqual(s["util"], 0.5)

    def test_no_blob_data(self):
        self.assertIsNone(summarize({"baseFeePerGas": ["0x1"]}))

    def test_sparkline(self):
        self.assertEqual(sparkline([1, 1, 1]), "▁▁▁")
        self.assertEqual(sparkline([0, 7])[0], "▁")
        self.assertEqual(sparkline([0, 7])[-1], "█")


if __name__ == "__main__":
    unittest.main()
