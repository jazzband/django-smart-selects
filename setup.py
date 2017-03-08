from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_desc = f.read()

setup(name="django-smart-selects",
      version="1.3.3",
      description="Django application to handle chained model fields.",
      long_description=long_desc,
      author="Patrick Lauber",
      author_email="digi@treepy.com",
      url="https://github.com/digi604/django-smart-selects",
      packages=find_packages(),
      include_package_data=True,
      tests_require=[
          'flake8',
      ],
      )
