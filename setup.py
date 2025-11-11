from setuptools import setup, find_packages

setup(
    name="productivity-suite",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click"
    ],
    entry_points={
        "console_scripts": [
            "prod=productivity.cli:cli"
        ]
    }
)
