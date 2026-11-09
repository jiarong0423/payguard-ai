# Reference Digests

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlJlZmVyZW5jZURpZ2VzdHM

ReferenceDigests.


# Class Name

`ReferenceDigests`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `chunksSha256` | `string` | Required | Chunks sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getChunksSha256(): string | setChunksSha256(string chunksSha256): void |
| `sourcesSha256` | `string` | Required | Sources sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getSourcesSha256(): string | setSourcesSha256(string sourcesSha256): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ReferenceDigestsBuilder;

$referenceDigests = ReferenceDigestsBuilder::init(
    'chunks_sha2562',
    'sources_sha2564'
)->build();
```



