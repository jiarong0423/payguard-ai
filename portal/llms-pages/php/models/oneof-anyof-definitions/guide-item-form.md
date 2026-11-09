# Guide Item Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkd1aWRlSXRlbUZvcm0


# Data Type

`GuideForm`


# Cases

| Type |
|  --- |
| [`GuideForm`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/guide-form.md) |


# GuideForm

## Initialization Code

### Example

```php
$value = GuideFormBuilder::init(
    Kind2Enum::CHOICE,
    [
        GuideOptionBuilder::init(
            'label2',
            'value4'
        )->build()
    ],
    'String9'
)->build();
```



