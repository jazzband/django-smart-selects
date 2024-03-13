Changes
=======

(unreleased)
------------------


1.7.0 (2024-03-13)
------------------

- Dropped support for Python 3.6 and 3.7! [medbenmakhlouf]
- Dropped support for Django 2.2, 3.0 and 3.1! [medbenmakhlouf]
- Add support for Python 3.10, 3.11 and 3.12. [medbenmakhlouf]
- Add Support for Django 4.1, 4.2 and 5.0! [medbenmakhlouf]


1.6.0 (2022-07-13)
------------------

- Dropped support for Python 2.7 and 3.5! [jezdez]
- Dropped support for Django 1.11, 2.0 and 2.1! [jezdez]
- Add support for Python 3.9. [jezdez]
- Move CI to GitHub Actions: https://github.com/jazzband/django-smart-selects/actions [jezdez]
- Docs: elaborate usage within templates [amiroff]
- Ensure at least one option in the <select> element (as required in HTML) [d9pouces]
- Migrate to GitHub Actions [jezdez]
- Add example of chained FK as inline [manelclos]
- Support Django 3.2 and 4.0 [manelclos]


1.5.9 (2020-08-28)
------------------

- add Django 3.1 as supported
  [d9pouces]


1.5.8 (2020-08-17)
------------------

- Reverting excessive lint correction that breaks init_value check
  [prodigel]


1.5.7 (2020-08-17)
------------------

- Init horizontal filtered on load
  [leibowitz]
- Add node variable initialization to fix node undefined error
  [leibowitz]


1.5.6 (2020-05-12)
------------------

- Add Sphinx project and move current docs to it
  [manelclos]
- Add pytest support
  [manelclos]
- Support django up to 3.0.x
  [manelclos]
- Fix chainedfk and chainedm2m not being defined (closes #253)
  [manelclos]
- Add multichained selects to Location example
  [manelclos]
- Force to load select2 js first
  [leibowitz]
- Fixed bug with missing "renderer" parameter in widgets.py render methods
  [glenngaetz]
- Fix renderer parameter in older django versions
  [manelclos]
- Add link to PyPI and installation instructions
  [Flimm]


1.5.5
-----

Version 1.5.5 was skipped due to bad packaging
