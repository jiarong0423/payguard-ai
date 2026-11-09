# Card

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkNhcmQ

Card.


# Class Name

`Card`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `brand` | string\|null | Optional | This is a container for any-of cases. | getBrand(): ?string | setBrand(?string brand): void |
| `category` | string\|null | Optional | This is a container for any-of cases. | getCategory(): ?string | setCategory(?string category): void |
| `imageUrl` | string\|null | Optional | This is a container for any-of cases. | getImageUrl(): ?string | setImageUrl(?string imageUrl): void |
| `keyFeatures` | `?(string[])` | Optional | Key features.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `100`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` | getKeyFeatures(): ?array | setKeyFeatures(?array keyFeatures): void |
| `materials` | `?(string[])` | Optional | Materials.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `40`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` | getMaterials(): ?array | setMaterials(?array materials): void |
| `productId` | `?string` | Optional | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` | getProductId(): ?string | setProductId(?string productId): void |
| `title` | `?string` | Optional | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` | getTitle(): ?string | setTitle(?string title): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\CardBuilder;

$card = CardBuilder::init()
    ->brand(
        'String1'
    )
    ->category(
        'String5'
    )
    ->imageUrl(
        'String3'
    )
    ->keyFeatures(
        [
            'key_features2'
        ]
    )
    ->materials(
        [
            'materials7',
            'materials8',
            'materials9'
        ]
    )
    ->build();
```



