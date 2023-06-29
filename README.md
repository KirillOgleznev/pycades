# pycades

Данный проект создан для удобной установки pycades в свой проект

pycades представляет собой расширение для Python3, которое реализует интерфейс, аналогичный [CAdESCOM](https://docs.cryptopro.ru/cades/reference/cadescom).

[Источник расширения](https://docs.cryptopro.ru/cades/pycades)

[GitHub](https://github.com/KirillOgleznev/pycades)
    
    pip install pycades

Если не установлены зависимости КриптоПро CSP, то библиотека начинает вести себя непредсказуемо и 
некоторые методы перестают работать, для лучшей работы желательно установить их установить [с оф сайта](https://docs.cryptopro.ru/cades/pycades/pycades-build)
или найти их в [гите /libs](https://github.com/KirillOgleznev/pycades/tree/main/libs) (достаточно будет установить КриптоПро CSP, [/libs/linux-amd64_deb](https://github.com/KirillOgleznev/pycades/tree/main/libs/linux-amd64_deb) через install.sh)


[Официальная документация](https://docs.cryptopro.ru/cades/pycades)

[Пример использования](https://docs.cryptopro.ru/cades/pycades/pycades-samples)

# Несколько примеров
<sup>больше можно посмотреть в директории с тестами</sup>

Загрузка сертификата из фала:
```python
from pycades import pycades


if __name__ == "__main__":
    with open('./certs/Kornevoy-sertifikat-GUTS-2022.CER', "rb") as f:
        cert = pycades.Certificate()
        cert.Import(f.read())
    print(cert.IsValid().Result)
```
Получение данных сертификата:
```python
from pycades import pycades


def test_get_info_method(cert):
    # Возвращает имя субъекта.
    assert cert.GetInfo(pycades.CAPICOM_CERT_INFO_SUBJECT_SIMPLE_NAME) == 'Минцифры России'
    # Возвращает имя издателя сертификата.
    assert cert.GetInfo(pycades.CAPICOM_CERT_INFO_ISSUER_SIMPLE_NAME) == 'Минцифры России'
    # Возвращает адрес электронной почты субъекта
    assert cert.GetInfo(pycades.CAPICOM_CERT_INFO_SUBJECT_EMAIL_NAME) == 'dit@digital.gov.ru'
    # Возвращает адрес электронной почты издателя сертификата.
    assert cert.GetInfo(pycades.CAPICOM_CERT_INFO_ISSUER_EMAIL_NAME) == 'dit@digital.gov.ru'
    # Возвращает UPN субъекта сертификата
    assert cert.GetInfo(pycades.CAPICOM_CERT_INFO_SUBJECT_UPN) == ''
    # Возвращает UPN издателя сертификата
    assert cert.GetInfo(pycades.CAPICOM_CERT_INFO_ISSUER_UPN) == ''
    # Возвращает DNS-имя субъекта сертификата. .
    assert cert.GetInfo(pycades.CAPICOM_CERT_INFO_SUBJECT_DNS_NAME) == 'Минцифры России'
    # Возвращает DNS-имя издателя сертификата.
    assert cert.GetInfo(pycades.CAPICOM_CERT_INFO_ISSUER_DNS_NAME) == 'Минцифры России'


def test_get_base_info(cert):
    # Дата, с которой сертификат действителен.
    assert cert.ValidFromDate == '08.01.2022 13:32:39'
    # Дата, до которой сертификат действителен
    assert cert.ValidToDate == '08.01.2040 13:32:39'
    # Серийный номер.
    assert cert.SerialNumber == '00951FA3477C61043AADFA858627823442'

    name = (
        'CN=Минцифры России, ИНН ЮЛ=7710474375, ОГРН=1047702026701, O=Минцифры '
        'России, STREET="Пресненская набережная, дом 10, строение 2", L=г. Москва, '
        'S=77 Москва, C=RU, E=dit@digital.gov.ru'
    )
    # Издатель сертификата.
    assert cert.IssuerName == name
    # Имя субъекта.
    assert cert.SubjectName == name
    # Отпечаток.
    assert cert.Thumbprint == '2F0CB09BE3550EF17EC4F29C90ABD18BFCAAD63A'
    # Версия сертификата.
    assert cert.Version == 3

```