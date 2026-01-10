#!/usr/bin/env python3
"""TRINITY-OS Setup Script"""

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="trinity-os",
    version="1.0.0",
    author="AFO Kingdom",
    author_email="trinity-os@afo-kingdom.org",
    description="TRINITY-OS: AFO 왕국의 통합 자동화 운영체제",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lofibrainwav/TRINITY-OS",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.12",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "ruff>=0.1.0",
            "mypy>=1.0.0",
        ],
        "docker": [
            "docker>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "trinity-os=run_trinity_os:main",
            "sixxon=trinity_os.cli.sixxon:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
