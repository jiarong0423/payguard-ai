# Guide Item Form

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkd1aWRlSXRlbUZvcm0


# Data Type

`GuideForm`


# Cases

| Type |
|  --- |
| [`GuideForm`](http://localhost:3000/llms-pages/php/models/structures/guide-form.md) |


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



