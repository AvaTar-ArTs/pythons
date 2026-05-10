import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
Unit tests for the monkey patch for expand mask to handle packed sequences
"""

import unittest

import torch

from axolotl.monkeypatch.llama_expand_mask import _expand_mask


class TestExpandMask(unittest.TestCase):
    """
    Test class for attention mask expansion for packed sequences
    """

    def test_output(self):
        mask = torch.tensor([[1, 1, 1, 2], [2, 3, 3, 0]])
        dtype = torch.float32
        expected_output = torch.tensor(
            [
                [
                    [
                        [0.0000e00, -3.4028e38, -3.4028e38, -3.4028e38],
                        [0.0000e00, 0.0000e00, -3.4028e38, -3.4028e38],
                        [0.0000e00, 0.0000e00, 0.0000e00, -3.4028e38],
                        [-3.4028e38, -3.4028e38, -3.4028e38, 0.0000e00],
                    ]
                ],
                [
                    [
                        [0.0000e00, -3.4028e38, -3.4028e38, -3.4028e38],
                        [-3.4028e38, 0.0000e00, -3.4028e38, -3.4028e38],
                        [-3.4028e38, 0.0000e00, 0.0000e00, -3.4028e38],
                        [-3.4028e38, -3.4028e38, -3.4028e38, -3.4028e38],
                    ]
                ],
            ]
        )
        # Check that the output matches the expected output
        self.assertTrue(torch.allclose(_expand_mask(mask, dtype), expected_output))


try:
        unittest.main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)