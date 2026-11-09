# Sent File Fingerprint

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlNlbnRGaWxlRmluZ2VycHJpbnQ

Plain SHA-256 of one file's exact bytes, recorded at the moment of a send so a later read-back can be compared.

The keyed `payload_sha256` cannot be checked outside the session; this one can. Never present on a preview.


# Class Name

`SentFileFingerprint`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ByteLength` | `int` | Required | Byte length.<br><br>**Constraints**: `>= 0`, `<= 9999999` |
| `ContentType` | [`ContentTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/content-type.md) | Required | Content type. |
| `Filename` | `string` | Required | Filename.<br><br>**Constraints**: *Maximum Length*: `255` |
| `Sha256` | `string` | Required | Sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

SentFileFingerprint sentFileFingerprint = new SentFileFingerprint
{
    ByteLength = 62,
    ContentType = ContentTypeEnum.EnumImagejpeg,
    Filename = "filename6",
    Sha256 = "sha2564",
};
```



