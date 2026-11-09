# Product Card

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlByb2R1Y3RDYXJk

A Channel3 catalogue product reduced to what identifies the item; no prices, offers or buy links.


# Interface Name

`ProductCard`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `brand` | [`ProductCardBrand`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/product-card-brand.md) | Required | This is a container for any-of cases. |
| `category` | [`ProductCardCategory`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/product-card-category.md) | Required | This is a container for any-of cases. |
| `imageUrl` | [`ProductCardImageUrl`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/product-card-image-url.md) | Required | This is a container for any-of cases. |
| `keyFeatures` | `string[]` | Required | Key features.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `100`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `materials` | `string[]` | Required | Materials.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `40`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `productId` | `string` | Required | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```ts
import { ProductCard } from 'tradeglot-local-consolelib';

const productCard: ProductCard = {
  brand: 'String9',
  category: 'String3',
  imageUrl: 'String1',
  keyFeatures: [
    'key_features0',
    'key_features1'
  ],
  materials: [
    'materials5'
  ],
  productId: 'product_id0',
  title: 'title0',
};
```



