from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="jrnlmd",
    version="0.1",
    author="Simone Gaiarin",
    author_email="simgunz@gmail.com",
    description=("Write bullet notes to a markdown journal"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    entry_points={
        "console_scripts": ['jrnlmd = jrnlmd.jrnlmd:entrypoint']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
