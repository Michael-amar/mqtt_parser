from setuptools import setup, find_packages

setup(
    name="mqtt_parser",  # Replace with your library's name
    version="1.0.0",
    author="Michael Amar",
    author_email="michaela@bugsec.com",
    description="MQTT parser",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://gitlab.TWshop/michaela/mqtt_parser.git",  # URL to your project repository
    packages=find_packages(),  # Automatically find packages in your library
    package_data={ "": ["*.py"] },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
