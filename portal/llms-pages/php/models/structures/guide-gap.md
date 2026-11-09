# Guide Gap

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkd1aWRlR2Fw

GuideGap.


# Class Name

`GuideGap`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `conflicting` | `string[]` | Required | Conflicting. | getConflicting(): array | setConflicting(array conflicting): void |
| `missing` | `string[]` | Required | Missing. | getMissing(): array | setMissing(array missing): void |
| `partial` | `string[]` | Required | Partial. | getPartial(): array | setPartial(array partial): void |
| `present` | `string[]` | Required | Present. | getPresent(): array | setPresent(array present): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideGapBuilder;

$guideGap = GuideGapBuilder::init(
    [
        'conflicting9'
    ],
    [
        'missing4'
    ],
    [
        'partial4',
        'partial5'
    ],
    [
        'present9',
        'present0',
        'present1'
    ]
)->build();
```



