import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uboto3",
    version="0.0.1",
    author="Maksym Sladkov",
    author_email="sladkovm@gmail.com",
    description="JSON centered wrapper for boto3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sladkovm/uboto3",
    py_modules=['uboto3'],
    install_requires=['boto3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
