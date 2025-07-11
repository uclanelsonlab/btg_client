#!/usr/bin/env python3
"""
Setup script for BTG Virtual Geneticist API Client
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = 'README.md'
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "BTG Virtual Geneticist API Client"

# Read requirements
def read_requirements():
    requirements_path = 'requirements.txt'
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="btg-client",
    version="1.1.0",
    description="A modular Python client for the BT Genomics Virtual Geneticist API",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="BT Genomics",
    author_email="support@btgenomics.com",
    url="https://github.com/btgenomics/btg-client",
    packages=find_packages(),
    py_modules=["btg_client"],
    install_requires=read_requirements(),
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        "console_scripts": [
            "btg-client=btg_client:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 