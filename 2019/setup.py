import setuptools

setuptools.setup(
    name="aoc",
    version="1.0.0",
    description="",
    license="",

    author="Mitchell Murphy",
    author_email="",
    
    install_requires=[
        "numpy",
        "python-dotenv"
    ],
    packages=[
        "aoc",
        "aoc.data",
        "aoc.features",
        "aoc.models",
        "aoc.visualisation"
    ],
    zip_safe=False
)
