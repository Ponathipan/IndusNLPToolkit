from setuptools import setup, find_packages
import subprocess

# Install dependency from GitHub
# subprocess.call(['pip', 'install', 'git+https://github.com/libindic/indic-trans.git'])

setup(
    name="IndusNLPToolkit",
    version="1.0.0",
    description="A toolkit for processing and analyzing Hindi and related dialects.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    maintainer="Maker's Lab Team",
    maintainer_email="makerslab@techmahindra.com",
    author="Maker's Lab Team",
    author_email="makerslab@techmahindra.com",
    url="https://github.com/Tech-Mahindra-Makers-Lab/The-Indus-Project",
    packages=find_packages(),
    install_requires=['numpy',
                      'tqdm',
                      'nltk',
                      'pyyaml',
                      'pbr',
                      'six',
                      'future',
                      'cython',
                      'numpy',
                      'scipy'
                      ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Text Processing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords=[
        "hindi nlp text-processing",
        "indus nlp toolkit",
    ],
    package_data={
        "indusnlp": ["data/*"],
    },
    python_requires=">=3.7",
)
