'''
Created on 2016年11月11日

@author: hanlucen
'''

from django.conf import settings
import string
import random
from django.utils import timezone
from django.core.cache import cache
import logging

logger = logging.getLogger('default')

try:
    SMS = settings.SMS
except Exception as e:
    logger.error('settings has not SMS config')
    raise e

MOBILE_CAPTCHA_CHACE_PATH = getattr(
    SMS.get('MOBILE_CAPTCHA'),
    'MOBILE_CAPTCHA_CHACE_PATH',
    'send_mobile_captcha'
    )

MOBILE_CAPTCHA_VALID_DURATION = getattr(
    SMS('MOBILE_CAPTCHA'), 'MOBILE_CAPTCHA_VALID_DURATION', 60 * 10)


def create_random_string(
        length, letters=True, digits=True, filters=['O', 'o', '0']):
    if letters and not digits:
        raw_string = string.ascii_letters
    elif not letters and digits:
        raw_string = string.digits
    else:
        raw_string = string.ascii_letters + string.digits
    return ''.join(random.sample(filter((
        lambda x: False if x in filters else True), raw_string), length), '')

serie_hour_map = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G',
    7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N',
    14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T',
    20: 'U', 21: 'V', 22: 'W', 23: 'X',
}


def create_message_serie():
    now = timezone.now()
    return '%s%02d%02d' % (serie_hour_map[now.hour], now.minute, now.second)


class MobileCaptcha(object):

    def __init__(self, mobile):
        self.mobile = mobile
        self.cache_key = '%s:%s' % (MOBILE_CAPTCHA_CHACE_PATH, mobile)

    def create_captcha(self, num=6, letters=False):
        serie = create_message_serie()
        captcha = create_random_string(num, letters=letters)
        cache.set(self.cache_key, '%s_%s' % (serie, captcha),
                  MOBILE_CAPTCHA_VALID_DURATION)
        return serie, captcha

    def verify_captcha(self, serie, captcha):
        value = cache.get(self.cache_key)
        if value:
            _serie, _captcha = value.split('_')
            if _serie == serie and _captcha.lower() == captcha.lower():
                return True
        return False
