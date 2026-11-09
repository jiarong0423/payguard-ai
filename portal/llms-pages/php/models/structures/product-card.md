# Product Card

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlByb2R1Y3RDYXJk

A Channel3 catalogue product reduced to what identifies the item; no prices, offers or buy links.


# Class Name

`ProductCard`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `brand` | string | Required | This is a container for any-of cases. | getBrand(): string | setBrand(string brand): void |
| `category` | string | Required | This is a container for any-of cases. | getCategory(): string | setCategory(string category): void |
| `imageUrl` | string | Required | This is a container for any-of cases. | getImageUrl(): string | setImageUrl(string imageUrl): void |
| `keyFeatures` | `string[]` | Required | Key features.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `100`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` | getKeyFeatures(): array | setKeyFeatures(array keyFeatures): void |
| `materials` | `string[]` | Required | Materials.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `40`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` | getMaterials(): array | setMaterials(array materials): void |
| `productId` | `string` | Required | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` | getProductId(): string | setProductId(string productId): void |
| `title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` | getTitle(): string | setTitle(string title): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ProductCardBuilder;

$productCard = ProductCardBuilder::init(
    'String9',
    'String3',
    'String1',
    [
        'key_features0',
        'key_features1'
    ],
    [
        'materials5'
    ],
    'product_id0',
    'title0'
)->build();
```



