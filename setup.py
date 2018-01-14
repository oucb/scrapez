from setuptools import setup

setup(
    name='scrapez',
    packages=['scrapez'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_flash'
    ],
)
