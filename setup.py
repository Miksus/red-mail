from setuptools import setup, find_packages
import versioneer

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="redmail",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Mikael Koli",
    author_email="koli.mikael@gmail.com",
    url="https://github.com/Miksus/red-mail.git",
    packages=find_packages(),
    description="Email sending library",
    long_description=long_description,
    long_description_content_type="text/markdown",
     classifiers=[
        "Operating System :: OS Independent",

        "Programming Language :: Python :: 3",

        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
     ],
     include_package_data=True, # for MANIFEST.in
     python_requires='>=3.6.0',

    install_requires = [
        'jinja2',
    ],
)
