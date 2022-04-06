from setuptools import setup, find_packages
from dcm_filter_lib import __version__

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="dcm_filter_lib",
    version=__version__,
    description="DCM Filter Library",
    url="[url]",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alven Wu",
    author_email="[nsnhello@gmail.com]",
    packages=find_packages(include=['dcm_filter_lib']),
    entry_points={
        'console_scripts': ['dcm_filter=dcm_filter_lib._dcm_filter:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
