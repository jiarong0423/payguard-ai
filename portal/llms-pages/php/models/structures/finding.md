# Finding

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkZpbmRpbmc

Finding.


# Class Name

`Finding`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `category` | [`string(CategoryEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/category.md) | Required | Category. | getCategory(): string | setCategory(string category): void |
| `code` | `string` | Required, Constant | Code.<br><br>**Value**: `'keyword_requires_policy_review'` | getCode(): string | setCode(string code): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\FindingBuilder;
use TradeGlotLocalConsoleLib\Models\CategoryEnum;

$finding = FindingBuilder::init(
    CategoryEnum::UNSUPPORTED_FINANCIAL_PROMISE
)->build();
```



