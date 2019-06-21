import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pyconfluent",
    version="0.0.1",
    author="Peter Newell",
    author_email="peter.newell@covetrus.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitbub.com/newellp2019/pyconfluent",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)