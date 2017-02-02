All versions of django-smart-selects prior to version 1.2.8 are vulnerable to an XSS attack as detailed in [issue 171](https://github.com/digi604/django-smart-selects/issues/171#issuecomment-276774103). As a result, all previous versions have been removed from PyPI to prevent users from installing insecure versions. All users are urged to upgrade as soon as possible.

## Checklist

- [ ] This issue is not about installing previous versions of django-smart-selects older than 1.2.8. I understand that previous versions are insecure.
- [ ] I have verified that that issue exists against the `master` branch of django-smart-selects.
- [ ] I have searched for similar issues in both open and closed tickets and cannot find a duplicate.
- [ ] I have debugged the issue to the smart_selects app.
- [ ] I have reduced the issue to the simplest possible case.
- [ ] I have included all relevant sections of `models.py`, `forms.py`, and `views.py` with problems.

## Steps to reproduce

## Expected behavior

## Actual behavior
