# Multipart File Part

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRk11bHRpcGFydEZpbGVQYXJ0

MultipartFilePart.


# Class Name

`MultipartFilePart`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `byte_length` | `int` | Required | Byte length.<br><br>**Constraints**: `>= 0`, `<= 9999999` |
| `content_type` | [`ContentTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/content-type.md) | Required | Content type. |
| `filename` | `str` | Required | Filename.<br><br>**Constraints**: *Maximum Length*: `255` |
| `name` | `str` | Required | Name.<br><br>**Constraints**: *Pattern*: `^file[0-9]{1,3}$` |


# Example

```python
from tradeglotlocalconsole.models.content_type_enum import ContentTypeEnum
from tradeglotlocalconsole.models.multipart_file_part import MultipartFilePart

multipart_file_part = MultipartFilePart(
    byte_length=18,
    content_type=ContentTypeEnum.ENUM_IMAGEJPEG,
    filename='filename4',
    name='name2'
)
```



