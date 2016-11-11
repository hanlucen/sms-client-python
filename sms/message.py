'''
Created on 2016年11月11日

@author: hanlucen
'''

from sms_provider.provider import YunXinProvider, YiMeiProvider
from .captcha import MobileCaptcha
from django.conf import settings
import logging

logger = logging.getLogger('default')

try:
    SMS = settings.SMS
except Exception as e:
    logger.error('settings has not SMS config')
    raise e

PROVIDER_NAME = getattr(SMS.get('PROVIDER'), 'NAME', '')
PROVIDER_DOMAIN = getattr(SMS.get('PROVIDER'), 'DOMAIN', '')
PROVIDER_USERNAME = getattr(SMS('PROVIDER'), 'USERNAME', '')
PROVIDER_PASSWORD = getattr(SMS('PROVIDER'), 'PASSWORD', '')
PROVIDER_APP = getattr(SMS('PROVIDER'), 'APP', '')


class SMSProvider(object):

    def __init__(self):
        self.provider = self._create()

    def _create(self):
        if PROVIDER_NAME == 'YunXin':
            return YunXinProvider(
                PROVIDER_DOMAIN,
                PROVIDER_USERNAME,
                PROVIDER_PASSWORD,
                PROVIDER_APP
                )
        elif PROVIDER_NAME == 'YiMei':
            return YiMeiProvider(
                PROVIDER_DOMAIN,
                PROVIDER_USERNAME,
                PROVIDER_PASSWORD,
                PROVIDER_APP
                )
        else:
            logger.error('provider name are not supported')
            raise

    def send_message(self, receiver, message='', use_async=False):
        self.provider.send_message(receiver, message, use_async)

    def send_message_with_captcha(
            self, receiver, template='', use_async=False):
        serie, captcha = MobileCaptcha(receiver).create_captcha()
        try:
            msg = template % captcha
        except Exception as e:
            logger.error(e)
            raise
        self.provider.send_message(receiver, message=msg, use_async=use_async)
        return serie

    def verify_captcha(self, receiver, serie, captcha):
        return MobileCaptcha(receiver).verify_captcha(serie, captcha)


sms_provider = SMSProvider()
