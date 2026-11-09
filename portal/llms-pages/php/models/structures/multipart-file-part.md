# Multipart File Part

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRk11bHRpcGFydEZpbGVQYXJ0

MultipartFilePart.


# Class Name

`MultipartFilePart`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `byteLength` | `int` | Required | Byte length.<br><br>**Constraints**: `>= 0`, `<= 9999999` | getByteLength(): int | setByteLength(int byteLength): void |
| `contentType` | [`string(ContentTypeEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/content-type.md) | Required | Content type. | getContentType(): string | setContentType(string contentType): void |
| `filename` | `string` | Required | Filename.<br><br>**Constraints**: *Maximum Length*: `255` | getFilename(): string | setFilename(string filename): void |
| `name` | `string` | Required | Name.<br><br>**Constraints**: *Pattern*: `^file[0-9]{1,3}$` | getName(): string | setName(string name): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\MultipartFilePartBuilder;
use TradeGlotLocalConsoleLib\Models\ContentTypeEnum;

$multipartFilePart = MultipartFilePartBuilder::init(
    138,
    ContentTypeEnum::ENUM_IMAGEJPEG,
    'filename0',
    'name8'
)->build();
```



