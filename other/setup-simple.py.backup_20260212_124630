"""
Setup script for City 16-9 Gallery Generator
Following the dark patterns of simplegallery
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="city-gallery",
    version="1.0.0",
    author="Λ∀ʌ†ʌʀ 🦄 ∆ʀ†s",
    author_email="contact@avatararts.org",
    description="A dark, modular gallery generation system for urban photography",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avatararts/city-gallery",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "city-gallery-init=city_gallery.gallery_init:main",
            "city-gallery-build=city_gallery.gallery_build:main",
        ],
    },
    include_package_data=True,
    package_data={
        "city_gallery": [
            "templates/*.jinja",
            "public/css/*.css",
            "public/js/*.js",
        ],
    },
)
