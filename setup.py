from setuptools import find_packages, setup

import tracker

setup(
    name="crypto-tracker",
    description="Crypto tracker",
    packages=find_packages(),
    author=tracker.__author__,
    author_email=tracker.__author_email__,
    include_package_data=True,
    entry_points={"console_scripts": ["tracker = tracker.cli.__main__:crypto_tracker"]},
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        # "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)