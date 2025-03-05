from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claude-memory-manager",
    version="0.1.0",
    author="Claude Memory Manager Developer",
    author_email="your.email@example.com",
    description="A command-line tool for managing Claude Terminal Client memories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/claude-memory-manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "claude-memory=claude_memory:main",
        ],
    },
) 