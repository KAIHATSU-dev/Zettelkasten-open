from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zettelkasten-open",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to analyze and find connections in Obsidian notes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/zettelkasten-open",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "zettelkasten-open=Zettelkasten:main",
        ],
    },
    python_requires=">=3.6",
)