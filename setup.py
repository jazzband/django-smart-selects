from setuptools import setup, find_packages

setup(name="django-smart-selects",
           version="1.0.4",
           description="Django application to handle chained model fields.",
           author="Patrick Lauber",
           packages=find_packages(),
           include_package_data=True,
)

