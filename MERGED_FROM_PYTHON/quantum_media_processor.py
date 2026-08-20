"""
Summary of quantum_media_processor.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import numpy as np
from PIL import Image
from scipy.fftpack import dct


class QuantumMediaProcessor:
    def __init__(self, chaos_factor=0.07):
        self.chaos_factor = chaos_factor

    def _quantum_dct(self, block):
        coeffs = dct(dct(block.T, norm="ortho").T, norm="ortho")
        threshold = np.percentile(np.abs(coeffs), 95) * self.chaos_factor
        coeffs[np.abs(coeffs) < threshold] *= np.random.choice(
            [0, 1], p=[0.3, 0.7], size=coeffs.shape
        )
        return coeffs

    def process_image(self, image_path, output_path):
        ycbcr = img.convert("YCbCr")
        for i in range(0, ycbcr.size[0], 8):
            for j in range(0, ycbcr.size[1], 8):
                block = ycbcr.crop((i, j, i + 8, j + 8))
                y, cb, cr = block.split()
                y_quant = self._quantum_dct(np.array(y))
                processed_block = Image.fromarray(y_quant.astype("uint8"), "L")
                if np.random.random() < self.chaos_factor:
                    processed_block = Image.blend(
                        processed_block, processed_block.rotate(45), 0.5
                    )
                ycbcr.paste(processed_block, (i, j))
        ycbcr.convert("RGB").save(output_path)
        return output_path
