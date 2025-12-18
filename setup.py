from setuptools import setup, find_packages

setup(
    name="project-sens",
    version="0.1.0",
    packages=find_packages(include=['server', 'server.*', 'cities', 'cities.*', 'data', 'data.*', 'states', 'states.*', 'countries', 'countries.*', 'security', 'security.*']),
    install_requires=[
        "flask",
        "flask-restx",
        "pymongo",
        "pytest",
        "pytest-cov",
        "flake8",
        "certifi",
    ],
    python_requires=">=3.8",
)
