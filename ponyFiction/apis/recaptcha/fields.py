from django.conf import settings
from django import forms
from django.utils.encoding import smart_unicode
from ponyFiction.apis.recaptcha.widgets import ReCaptcha
from ponyFiction.apis.recaptcha.client import captcha

class ReCaptchaField(forms.CharField):
    default_error_messages = {
        'captcha_invalid': u'Invalid captcha'
    }

    def __init__(self, *args, **kwargs):
        self.widget = ReCaptcha
        self.required = True
        super(ReCaptchaField, self).__init__(*args, **kwargs)

    def clean(self, values):
        super(ReCaptchaField, self).clean(values[1])
        recaptcha_challenge_value = smart_unicode(values[0])
        recaptcha_response_value = smart_unicode(values[1])
        check_captcha = captcha.submit(recaptcha_challenge_value, 
            recaptcha_response_value, settings.RECAPTCHA_PRIVATE_KEY, {})
        if not check_captcha.is_valid:
            raise forms.util.ValidationError(self.error_messages['captcha_invalid'])
        return values[0]