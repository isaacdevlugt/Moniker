import os.path
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version_file = {}
with open(os.path.join("moniker", "__version__.py"), "r") as f:
    exec(f.read(), version_file)

setuptools.setup(
    name="moniker",
    version=version_file["__version__"],
    author="Isaac De Vlugt",
    author_email="isaacdevlugt@gmail.com",
    description="Sampling with the Alias method",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/isaacdevlugt/Moniker",
    project_urls={"Bug Tracker": "https://github.com/isaacdevlugt/Moniker/issues",},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude="tests"),
    python_requires=">=3.1",
    install_requires=["numpy>=1.14.5"],
)
