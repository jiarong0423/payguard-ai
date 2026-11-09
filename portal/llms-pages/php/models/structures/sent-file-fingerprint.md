# Sent File Fingerprint

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlNlbnRGaWxlRmluZ2VycHJpbnQ

Plain SHA-256 of one file's exact bytes, recorded at the moment of a send so a later read-back can be compared.

The keyed `payload_sha256` cannot be checked outside the session; this one can. Never present on a preview.


# Class Name

`SentFileFingerprint`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `byteLength` | `int` | Required | Byte length.<br><br>**Constraints**: `>= 0`, `<= 9999999` | getByteLength(): int | setByteLength(int byteLength): void |
| `contentType` | [`string(ContentTypeEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/content-type.md) | Required | Content type. | getContentType(): string | setContentType(string contentType): void |
| `filename` | `string` | Required | Filename.<br><br>**Constraints**: *Maximum Length*: `255` | getFilename(): string | setFilename(string filename): void |
| `sha256` | `string` | Required | Sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getSha256(): string | setSha256(string sha256): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\SentFileFingerprintBuilder;
use TradeGlotLocalConsoleLib\Models\ContentTypeEnum;

$sentFileFingerprint = SentFileFingerprintBuilder::init(
    62,
    ContentTypeEnum::ENUM_IMAGEJPEG,
    'filename6',
    'sha2564'
)->build();
```



