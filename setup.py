from setuptools import setup, find_packages

setup(
    name="task-manager",
    version="0.1.0",
    package_dir={"": "."},
    packages=find_packages(where="."),
    install_requires=[
        "fastapi",
        "uvicorn",
        "psycopg2-binary",
        "pydantic",
        "requests"
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-asyncio',
            'pytest-cov',
            'httpx'
        ]
    }
)