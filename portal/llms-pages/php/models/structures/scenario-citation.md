# Scenario Citation

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlNjZW5hcmlvQ2l0YXRpb24

ScenarioCitation.


# Class Name

`ScenarioCitation`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `chunkId` | `string` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` | getChunkId(): string | setChunkId(string chunkId): void |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` | getJurisdiction(): string | setJurisdiction(string jurisdiction): void |
| `locator` | `string` | Required | Locator.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1000` | getLocator(): string | setLocator(string locator): void |
| `materialType` | [`string(MaterialTypeEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/material-type.md) | Required | Material type. | getMaterialType(): string | setMaterialType(string materialType): void |
| `sourceId` | `string` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` | getSourceId(): string | setSourceId(string sourceId): void |
| `textSha256` | `string` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getTextSha256(): string | setTextSha256(string textSha256): void |
| `title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `512` | getTitle(): string | setTitle(string title): void |
| `url` | `string` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2048` | getUrl(): string | setUrl(string url): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ScenarioCitationBuilder;
use TradeGlotLocalConsoleLib\Models\MaterialTypeEnum;

$scenarioCitation = ScenarioCitationBuilder::init(
    'chunk_id8',
    'locator8',
    MaterialTypeEnum::OFFICIAL_API_REFERENCE,
    'source_id0',
    'text_sha2566',
    'title2',
    'url0'
)->build();
```



