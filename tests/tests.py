import os

import pytest

from pycades import pycades


@pytest.fixture
def load_cert(request):
    with open(os.path.join(os.path.dirname(__file__), 'certs/Kornevoy-sertifikat-GUTS-2022.CER'), "rb") as file:
        certificate = pycades.Certificate()
        certificate.Import(file.read())
    return certificate


def test_get_base_info(load_cert):
    # Дата, с которой сертификат действителен.
    assert load_cert.ValidFromDate == '08.01.2022 13:32:39'
    # Дата, до которой сертификат действителен
    assert load_cert.ValidToDate == '08.01.2040 13:32:39'
    # Серийный номер.
    assert load_cert.SerialNumber == '00951FA3477C61043AADFA858627823442'

    name = (
        'CN=Минцифры России, ИНН ЮЛ=7710474375, ОГРН=1047702026701, O=Минцифры '
        'России, STREET="Пресненская набережная, дом 10, строение 2", L=г. Москва, '
        'S=77 Москва, C=RU, E=dit@digital.gov.ru'
    )
    # Если не установлены зависимости КриптоПро то вернется этот вариант,
    # и вообще библиотека начинает вести себя не предсказуемо
    name_when_no_lib = (
        '2.5.4.3=Минцифры России, 1.2.643.100.4=7710474375, 1.2.643.100.1=1047702026701, '
        '2.5.4.10=Минцифры России, 2.5.4.9="Пресненская набережная, дом 10, строение 2", '
        '2.5.4.7=г. Москва, 2.5.4.8=77 Москва, 2.5.4.6=RU, 1.2.840.113549.1.9.1=dit@digital.gov.ru'
    )
    # Издатель сертификата.
    # raise Exception(load_cert.IssuerName)
    assert load_cert.IssuerName in [name, name_when_no_lib]
    # Имя субъекта.
    assert load_cert.SubjectName in [name, name_when_no_lib]
    # Версия сертификата.
    assert load_cert.Version == 3


def test_get_info_method(load_cert):
    # Возвращает имя субъекта.
    assert load_cert.GetInfo(pycades.CAPICOM_CERT_INFO_SUBJECT_SIMPLE_NAME) == 'Минцифры России'
    # Возвращает имя издателя сертификата.
    assert load_cert.GetInfo(pycades.CAPICOM_CERT_INFO_ISSUER_SIMPLE_NAME) == 'Минцифры России'
    # Возвращает адрес электронной почты субъекта
    assert load_cert.GetInfo(pycades.CAPICOM_CERT_INFO_SUBJECT_EMAIL_NAME) == 'dit@digital.gov.ru'
    # Возвращает адрес электронной почты издателя сертификата.
    assert load_cert.GetInfo(pycades.CAPICOM_CERT_INFO_ISSUER_EMAIL_NAME) == 'dit@digital.gov.ru'
    # Возвращает UPN субъекта сертификата
    assert load_cert.GetInfo(pycades.CAPICOM_CERT_INFO_SUBJECT_UPN) == ''
    # Возвращает UPN издателя сертификата
    assert load_cert.GetInfo(pycades.CAPICOM_CERT_INFO_ISSUER_UPN) == ''
    # Возвращает DNS-имя субъекта сертификата. .
    assert load_cert.GetInfo(pycades.CAPICOM_CERT_INFO_SUBJECT_DNS_NAME) == 'Минцифры России'
    # Возвращает DNS-имя издателя сертификата.
    assert load_cert.GetInfo(pycades.CAPICOM_CERT_INFO_ISSUER_DNS_NAME) == 'Минцифры России'


def test_get_ep_info_from_file(load_cert):
    """
        Метод сбора данных из сертификата для дальнейшего отображения
        Пример:
            Документ подписан электронной подписью {subject_name}
            Организация: {organization_name}
            Сертификат: {serial_number}
            Выдан: {issuer_name}
            Период действия сертификата: {valid_from_date} - {valid_to_date}
    """
    company_name = None
    subject_name = None
    for info in load_cert.SubjectName.split(','):
        if ' 2.5.4.10=' in info:
            company_name = info[10:]
        elif ' O=' in info:
            company_name = info[3:]
        elif '2.5.4.3=' in info:
            subject_name = info[8:]
        elif 'CN=' in info:
            subject_name = info[3:]

    result = {
        'subject_name': subject_name,
        'organization_name': company_name,
        'issuer_name': load_cert.GetInfo(pycades.CAPICOM_CERT_INFO_ISSUER_SIMPLE_NAME),
        'serial_number': load_cert.SerialNumber,
        'valid_from_date': load_cert.ValidFromDate,
        'valid_to_date': load_cert.ValidToDate,
    }
    assert result == {
        'subject_name': 'Минцифры России',
        'organization_name': 'Минцифры России',
        'issuer_name': 'Минцифры России',
        'serial_number': '00951FA3477C61043AADFA858627823442',
        'valid_from_date': '08.01.2022 13:32:39',
        'valid_to_date': '08.01.2040 13:32:39',
    }


def test_certificate_valid(load_cert):
    """Является ли сертификат валидным."""
    assert load_cert.IsValid().Result is True


def test_get_public_key(load_cert):
    """Получение публичного ключа."""
    public_key = 'BEBaSmukHWuPC4xav3a89jNu3xarv4N/j68a4PZRPij83W70R8LjrW4ZSfdqIJkv\nou5oQwxj7FobT1XblfSm6kCO\n'
    assert load_cert.PublicKey().EncodedKey.Value() == public_key
