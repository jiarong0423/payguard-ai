# Sent File Fingerprint

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlNlbnRGaWxlRmluZ2VycHJpbnQ

Plain SHA-256 of one file's exact bytes, recorded at the moment of a send so a later read-back can be compared.

The keyed `payload_sha256` cannot be checked outside the session; this one can. Never present on a preview.


# Class Name

`SentFileFingerprint`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `ByteLength` | `int` | Required | Byte length.<br><br>**Constraints**: `>= 0`, `<= 9999999` | int getByteLength() | setByteLength(int byteLength) |
| `ContentType` | [`ContentTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/content-type.md) | Required | Content type. | ContentTypeEnum getContentType() | setContentType(ContentTypeEnum contentType) |
| `Filename` | `String` | Required | Filename.<br><br>**Constraints**: *Maximum Length*: `255` | String getFilename() | setFilename(String filename) |
| `Sha256` | `String` | Required | Sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getSha256() | setSha256(String sha256) |


# Example

```java
import m18000.m0.m0.m127.models.ContentTypeEnum;
import m18000.m0.m0.m127.models.SentFileFingerprint;

SentFileFingerprint sentFileFingerprint = new SentFileFingerprint.Builder(
    62,
    ContentTypeEnum.ENUM_IMAGEJPEG,
    "filename6",
    "sha2564"
)
.build();
```



