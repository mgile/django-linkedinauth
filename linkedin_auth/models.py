from django.db import models
from django.utils.translation import ugettext as _


def random_member_id():
    import string, random
    return ''.join(random.choice(string.letters + string.digits) for i in xrange(50))
## END random_member_id


class LinkedInProfileModel(models.Model):
    '''
    LinkedIn Profile Abstract Model
    
    This class provides the set of fields that will be automatically
    merged from the logged-in users' LinkedIn profile. If you do
    not wish to use this abstract model, please ensure you copy
    these fields within your own profile model.
    '''
    
    member_id               = models.CharField(max_length=255, blank=False, unique=True, verbose_name=_('LinkedIn Member ID'))
    headline                = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('LinkedIn Profile  Headline'), help_text=_('The headline from the users\' LinkedIn account.'))
    picture_url             = models.URLField(null=True, verbose_name=_('LinkedIn Picture URL'), help_text=_('A URL to a LinkedIn profile photo or a placeholder'))
    location                = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('LinkedIn Profile Location Name'), help_text=_('A humanized location string.'))
    industry                = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('LinkedIn Profile Industry'), help_text=_('The industry in which this LinkedIn user works.'))
    num_connections         = models.PositiveIntegerField(default=0, null=True, verbose_name=_('LinkedIn Profile Number of Connections'), help_text=_('The number of LinkedIn connections.'))
    num_connections_capped  = models.NullBooleanField(default=False, null=True, verbose_name=_('LinkedIn Profile Number of Connections Capped'), help_text=_('Has LinkedIn artificially capped this accounts number of connections as 500?'))
    summary                 = models.TextField(max_length=5000, blank=True, null=True, verbose_name=_('LinkedIn Profile Summary'), help_text=_('The LinkedIn users summary paragraph.'))
    main_address            = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('LinkedIn Profile Main Address'), help_text=_('The LinkedIn users main physical address, if available'))
    access_token            = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('LinkedIn Profile '), help_text=_('OAuth 1.0a Long-Lived Access Token Dictionary (example: {\'oauth_token_secret\': \'65ab8d4b-79c1-4a3b-ab92-ab18dfd610c2\', \'oauth_authorization_expires_in\': \'0\', \'oauth_token\': \'2c1c33d2-b5b8-4455-8b16-e86e94e81cc8\', \'oauth_expires_in\': \'0\'}'))
    
    profile_data            = models.TextField(max_length=5000, blank=False, null=True, verbose_name=_('LinkedIn Profile Raw Data'), help_text=_('The raw profile data returned from LinkedIn'))

    def __unicode__(self):
        return u'LinkedIn User (%s): %s %s' % (self.user.username, self.user.first_name, self.user.last_name)
    
    class Meta:
        abstract            = True
        ordering            = ['num_connections', 'member_id']
## END LinkedInProfileModel