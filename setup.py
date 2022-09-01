from setuptools import setup, find_packages


desc = """
A extension for compose 
static-site handling, 
flask blueprints, 
reverse proxy for over server,
or others thing together.
"""


setup(
    name = 'Flask-Composer',
    packages = find_packages(),
    zip_safe = False,
    requires = [
        'flask',
        'requests'
    ],
    version = '0.1.0',
    description = desc,
    author = 'KohakuBlueleaf',
    author_email = 'apolloyeh0123@gmail.com',
    keywords = [
        'flask',
        'extension',
        'composer'
    ],
)