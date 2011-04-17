from django.conf import settings

LINKEDIN_API_KEY    = getattr(settings, 'LINKEDIN_API_KEY', None)
LINKEDIN_SECRET_KEY = getattr(settings, 'LINKEDIN_SECRET_KEY', None)

assert all([req in locals() for req in ['LINKEDIN_API_KEY', 'LINKEDIN_SECRET_KEY']]), 'You must specify LINKEDIN_API_KEY and LINKEDIN_SECRET_KEY in your django.settings'