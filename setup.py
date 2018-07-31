import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mp3tom4b",
    version="1.0",
    author="David Steele",
    author_email="dsteele@gmail.com",
    description="Convert mp3 files to an m4b audiobook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davesteele/mp3tom4b",
    python_requires=">=3.6",
    install_requires=["mutagen"],
    packages=["mp3tom4b"],
    entry_points={
        "console_scripts": ["mp3tom4b = mp3tom4b.mp3tom4b:main"],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "LICENSE :: OSI APPROVED :: GNU GENERAL PUBLIC LICENSE V3 (GPLV3)",
        "Operating System :: Linux",
    ),
)

