# HTTP Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationError`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `detail` | [`?(ValidationError[])`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/validation-error.md) | Optional | Detail. | getDetail(): ?array | setDetail(?array detail): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\HTTPValidationErrorBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\ValidationErrorBuilder;
use TradeGlotLocalConsoleLib\ApiHelper;

$hTTPValidationError = HTTPValidationErrorBuilder::init()
    ->detail(
        [
            ValidationErrorBuilder::init(
                [
                    'String7',
                    'String8',
                    'String9'
                ],
                'msg2',
                'type4'
            )
                ->ctx(ApiHelper::deserialize('{"key1":"val1","key2":"val2"}'))
                ->input(ApiHelper::deserialize('{"key1":"val1","key2":"val2"}'))
                ->build(),
            ValidationErrorBuilder::init(
                [
                    'String7',
                    'String8',
                    'String9'
                ],
                'msg2',
                'type4'
            )
                ->ctx(ApiHelper::deserialize('{"key1":"val1","key2":"val2"}'))
                ->input(ApiHelper::deserialize('{"key1":"val1","key2":"val2"}'))
                ->build()
        ]
    )
    ->build();
```



