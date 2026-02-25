"""Setup configuration for AI Model Evaluation Framework."""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r', encoding='utf-8') as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith('#')]

setup(
    name='ai-model-eval',
    version='1.0.0',
    author='AI Evaluation Team',
    author_email='team@example.com',
    description='A comprehensive framework for evaluating AI code generation models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/AI_ModelEval',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.8',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'ai-model-eval=src.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
