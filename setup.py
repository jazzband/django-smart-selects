from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_desc = f.read()

setup(
    name="django-smart-selects",
    use_scm_version={"version_scheme": "post-release"},
    setup_requires=["setuptools_scm"],
    description="Django application to handle chained model fields.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="Patrick Lauber",
    author_email="digi@treepy.com",
    url="https://github.com/jazzband/django-smart-selects",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["django>=2.2"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
    ],
)
