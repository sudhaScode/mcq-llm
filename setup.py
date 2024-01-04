from setuptools import setup, find_packages

from setuptools import setup, find_packages

setup(
    name="mcqgenerator",
    version="0.0.1",
    author="snb",
    author_email="sudha7995240121@gmail.com",
    install_requires=["openai", "langchain", "streamlit", "python-dotenv", "PyPDF2"],
    packages=find_packages(),
)
