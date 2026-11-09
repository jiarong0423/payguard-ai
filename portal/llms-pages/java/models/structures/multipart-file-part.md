# Multipart File Part

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRk11bHRpcGFydEZpbGVQYXJ0

MultipartFilePart.


# Class Name

`MultipartFilePart`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `ByteLength` | `int` | Required | Byte length.<br><br>**Constraints**: `>= 0`, `<= 9999999` | int getByteLength() | setByteLength(int byteLength) |
| `ContentType` | [`ContentTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/content-type.md) | Required | Content type. | ContentTypeEnum getContentType() | setContentType(ContentTypeEnum contentType) |
| `Filename` | `String` | Required | Filename.<br><br>**Constraints**: *Maximum Length*: `255` | String getFilename() | setFilename(String filename) |
| `Name` | `String` | Required | Name.<br><br>**Constraints**: *Pattern*: `^file[0-9]{1,3}$` | String getName() | setName(String name) |


# Example

```java
import m18000.m0.m0.m127.models.ContentTypeEnum;
import m18000.m0.m0.m127.models.MultipartFilePart;

MultipartFilePart multipartFilePart = new MultipartFilePart.Builder(
    138,
    ContentTypeEnum.ENUM_IMAGEJPEG,
    "filename0",
    "name8"
)
.build();
```



