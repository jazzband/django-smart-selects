from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_desc = f.read()

setup(name="django-smart-selects",
      version="1.5.4",
      description="Django application to handle chained model fields.",
      long_description=long_desc,
      long_description_content_type='text/markdown',
      author="Patrick Lauber",
      author_email="digi@treepy.com",
      url="https://github.com/jazzband/django-smart-selects",
      packages=find_packages(),
      include_package_data=True,
      install_requires=["django>=1.8, <2.1"],
      tests_require=[
          'flake8',
      ],
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      )
