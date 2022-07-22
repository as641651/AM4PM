from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='am4pa',
    version="0.1",
    description="Algorithms Measurements for Process Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/as641651/am4pa',
    author='Aravind Sankaran',
    author_email='aravindsankaran22@gmail.com',
    packages= find_packages(exclude=('test', )), # finds packages inside current directory
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">3",

)