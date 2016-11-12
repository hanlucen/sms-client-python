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
    PROVIDER = settings.SMS.get('PROVIDER')
except Exception as e:
    logger.error('settings has not SMS config')
    raise e


class SMSProvider(object):

    def __init__(self):
        self.provider = self._create()

    def _create(self):
        if PROVIDER.get('NAME', '').lower() == 'yunxin':
            return YunXinProvider(
                PROVIDER.get('DOMAIN', ''),
                PROVIDER.get('USERNAME', ''),
                PROVIDER.get('PASSWORD', ''),
                PROVIDER.get('APP', '')
                )
        elif PROVIDER.get('NAME', '').lower() == 'yimei':
            return YiMeiProvider(
                PROVIDER.get('DOMAIN', ''),
                PROVIDER.get('USERNAME', ''),
                PROVIDER.get('PASSWORD', ''),
                PROVIDER.get('APP', '')
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
