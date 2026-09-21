from typing import Protocol

from django.conf import settings
from django.utils.module_loading import import_string


class SmsDeliveryUnavailable(Exception):
    pass


class SmsDeliveryAdapter(Protocol):
    def send_verification_code(self, *, phone_number: str, code: str) -> None: ...


class UnavailableSmsDeliveryAdapter:
    def send_verification_code(self, *, phone_number: str, code: str) -> None:
        raise SmsDeliveryUnavailable


def get_sms_delivery_adapter() -> SmsDeliveryAdapter:
    adapter_class = import_string(settings.SMS_DELIVERY_ADAPTER)
    return adapter_class()
