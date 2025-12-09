"""Setup configuration for CNPJ Validator package."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cnpj-validator",
    version="1.0.0",
    author="Rafael Feltrim",
    author_email="",
    description="Sistema completo de validação de CNPJ para treinamento em QA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RaFeltrim/CNPJ-QA-Training",
    project_urls={
        "Bug Tracker": "https://github.com/RaFeltrim/CNPJ-QA-Training/issues",
        "Documentation": "https://github.com/RaFeltrim/CNPJ-QA-Training/tree/master/docs",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "cnpj-validate=cnpj_validator.cnpj_validator:main",
        ],
    },
)
