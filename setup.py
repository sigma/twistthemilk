from setuptools import setup, find_packages
setup(
    name = "TwistTheMilk",
    version = "0.1",
    packages = find_packages(),

    install_requires = ['twisted>=8.1'],

    # metadata for upload to PyPI
    author = "Yann Hodique",
    author_email = "yann.hodique@gmail.com",
    description = "a python/twisted API for Remember the Milk",
    license = "GPL",
    url = "http://github.com/sigma/twistthemilk",
    )
