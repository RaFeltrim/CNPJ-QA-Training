"""Setup configuration for CNPJ Validator package."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cnpj-validator-br",
    version="2.0.0",
    author="Rafael Feltrim",
    author_email="rafael.feltrim@example.com",
    description="Validador de CNPJ brasileiro com suporte ao formato alfanumérico 2026",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RaFeltrim/CNPJ-QA-Training",
    project_urls={
        "Bug Tracker": "https://github.com/RaFeltrim/CNPJ-QA-Training/issues",
        "Documentation": "https://github.com/RaFeltrim/CNPJ-QA-Training/tree/master/docs",
        "Source Code": "https://github.com/RaFeltrim/CNPJ-QA-Training",
        "Changelog": "https://github.com/RaFeltrim/CNPJ-QA-Training/blob/master/CHANGELOG.md",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "pytest-html>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "isort>=5.0.0",
            "bandit>=1.7.0",
        ],
        "api": [
            "fastapi>=0.100.0",
            "uvicorn>=0.22.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cnpj-validator=cnpj_validator.cli:main",
            "cnpj-validate=cnpj_validator.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "cnpj",
        "validator",
        "brazil",
        "brasil",
        "receita-federal",
        "alphanumeric",
        "validation",
        "qa",
        "testing",
    ],
)
