import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aVKapi",
    version="0.1.2",
    author="aiogram team",
    author_email="1282524@gmail.com",
    description="Python asyncio VK.com API library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aiogram/aVKapi",
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: AsyncIO",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
    ),
)
