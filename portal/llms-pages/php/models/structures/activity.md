# Activity

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkFjdGl2aXR5

Activity.


# Class Name

`Activity`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `at` | `string` | Required | At. | getAt(): string | setAt(string at): void |
| `id` | `string` | Required | Id. | getId(): string | setId(string id): void |
| `kind` | `string` | Required | Kind. | getKind(): string | setKind(string kind): void |
| `label` | `string` | Required | Label. | getLabel(): string | setLabel(string label): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` | getSource(): string | setSource(string source): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ActivityBuilder;

$activity = ActivityBuilder::init(
    'at4',
    'id8',
    'kind6',
    'label8'
)->build();
```



