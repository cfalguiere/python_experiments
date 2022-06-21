from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='Nonogram-experiments',
    packages=find_packages(include=['.']),
    version='0.0.1',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Claude Falguiere',
    author_email='',
    license='MIT',
    url='https://github.com/cfalguiere/python-experiments',
    platforms=['Any'],
    install_requires=['nox'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    python_requires='>=3.8',
)
