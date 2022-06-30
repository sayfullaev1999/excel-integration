from typing import Dict, Union

import random


def fraud_detector(service: str) -> float:
    """
        Детектор мошенничества
    :param service:
    :return:
    """
    return random.random()


def service_classifier(service: str) -> Dict[str, Union[str, int]]:
    """
        Классификатор услуг
    :param service:
    :return:
    """
    choices = {1: 'консультация', 2: 'лечение', 3: 'стационар', 4: 'диагностика', 5: 'лаборатория'}
    key = random.randint(1, 5)
    return {'service_class': key, 'service_name': choices[key]}
