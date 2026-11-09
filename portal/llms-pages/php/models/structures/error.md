# Error

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkVycm9y

What was refused and why.


# Class Name

`Error`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `code` | `string` | Required | Stable machine-readable reason, for example session_required. | getCode(): string | setCode(string code): void |
| `message` | `string` | Required | A plain sentence for a person. | getMessage(): string | setMessage(string message): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ErrorBuilder;

$error = ErrorBuilder::init(
    'code2',
    'message4'
)->build();
```



