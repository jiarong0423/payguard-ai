# Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlZhbGlkYXRpb25FcnJvcg

ValidationError.


# Class Name

`ValidationError`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `ctx` | `?array` | Optional | Ctx. | getCtx(): ?array | setCtx(?array ctx): void |
| `input` | `?array` | Optional | Input. | getInput(): ?array | setInput(?array input): void |
| `loc` | array<string\|int> | Required | This is Array of a container for any-of cases. | getLoc(): array | setLoc(array loc): void |
| `msg` | `string` | Required | Msg. | getMsg(): string | setMsg(string msg): void |
| `type` | `string` | Required | Type. | getType(): string | setType(string type): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ValidationErrorBuilder;
use TradeGlotLocalConsoleLib\ApiHelper;

$validationError = ValidationErrorBuilder::init(
    [
        'String9'
    ],
    'msg4',
    'type2'
)
    ->ctx(ApiHelper::deserialize('{"key1":"val1","key2":"val2"}'))
    ->input(ApiHelper::deserialize('{"key1":"val1","key2":"val2"}'))
    ->build();
```



