# Document Redaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkRvY3VtZW50UmVkYWN0aW9u

DocumentRedaction.


# Class Name

`DocumentRedaction`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `counts` | `array<string,int>` | Required | Counts.<br><br>**Constraints**: `>= 1`, `<= 128` | getCounts(): array | setCounts(array counts): void |
| `exportProfile` | `string` | Required, Constant | Export profile.<br><br>**Value**: `'INTERNAL_REVIEW_ONLY_V1'` | getExportProfile(): string | setExportProfile(string exportProfile): void |
| `limitations` | `string[]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `8`, *Minimum Length*: `1`, *Maximum Length*: `1000` | getLimitations(): array | setLimitations(array limitations): void |
| `limitedDetection` | `string` | Required, Constant | Limited detection.<br><br>**Value**: `'True'` | getLimitedDetection(): string | setLimitedDetection(string limitedDetection): void |
| `manualReviewRequired` | `string` | Required, Constant | Manual review required.<br><br>**Value**: `'True'` | getManualReviewRequired(): string | setManualReviewRequired(string manualReviewRequired): void |
| `method` | `string` | Required, Constant | Method.<br><br>**Value**: `'HMAC-SHA256 document pseudonymization v1'` | getMethod(): string | setMethod(string method): void |
| `redactedText` | `string` | Required | Redacted text.<br><br>**Constraints**: *Maximum Length*: `32768` | getRedactedText(): string | setRedactedText(string redactedText): void |
| `replacementCount` | `int` | Required | Replacement count.<br><br>**Constraints**: `>= 0`, `<= 128` | getReplacementCount(): int | setReplacementCount(int replacementCount): void |
| `reversibility` | `string` | Required, Constant | Reversibility.<br><br>**Value**: `'False'` | getReversibility(): string | setReversibility(string reversibility): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` | getSource(): string | setSource(string source): void |
| `types` | [`string(TypeEnum)[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/type.md) | Required | Types.<br><br>**Constraints**: *Maximum Items*: `7` | getTypes(): array | setTypes(array types): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\DocumentRedactionBuilder;
use TradeGlotLocalConsoleLib\Models\TypeEnum;

$documentRedaction = DocumentRedactionBuilder::init(
    [
        'key0' => 128,
        'key1' => 1,
        'key2' => 1
    ],
    [
        'limitations3'
    ],
    'redacted_text2',
    128,
    [
        TypeEnum::ID_LIKE,
        TypeEnum::NAME,
        TypeEnum::ADDRESS
    ]
)->build();
```



