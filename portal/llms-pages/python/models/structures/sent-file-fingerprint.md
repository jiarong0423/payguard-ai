# Sent File Fingerprint

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlNlbnRGaWxlRmluZ2VycHJpbnQ

Plain SHA-256 of one file's exact bytes, recorded at the moment of a send so a later read-back can be compared.

The keyed `payload_sha256` cannot be checked outside the session; this one can. Never present on a preview.


# Class Name

`SentFileFingerprint`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `byte_length` | `int` | Required | Byte length.<br><br>**Constraints**: `>= 0`, `<= 9999999` |
| `content_type` | [`ContentTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/content-type.md) | Required | Content type. |
| `filename` | `str` | Required | Filename.<br><br>**Constraints**: *Maximum Length*: `255` |
| `sha_256` | `str` | Required | Sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |


# Example

```python
from tradeglotlocalconsole.models.content_type_enum import ContentTypeEnum
from tradeglotlocalconsole.models.sent_file_fingerprint import SentFileFingerprint

sent_file_fingerprint = SentFileFingerprint(
    byte_length=210,
    content_type=ContentTypeEnum.ENUM_IMAGEJPEG,
    filename='filename4',
    sha_256='sha2564'
)
```



