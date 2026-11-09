# Card

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkNhcmQ

Card.


# Interface Name

`Card`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `brand` | [`CardBrand \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/card-brand.md) | Optional | This is a container for any-of cases. |
| `category` | [`CardCategory \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/card-category.md) | Optional | This is a container for any-of cases. |
| `imageUrl` | [`CardImageUrl \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/card-image-url.md) | Optional | This is a container for any-of cases. |
| `keyFeatures` | `string[] \| undefined` | Optional | Key features.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `100`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `materials` | `string[] \| undefined` | Optional | Materials.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `40`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `productId` | `string \| undefined` | Optional | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `title` | `string \| undefined` | Optional | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```ts
import { Card } from 'tradeglot-local-consolelib';

const card: Card = {
  brand: 'String1',
  category: 'String5',
  imageUrl: 'String3',
  keyFeatures: [
    'key_features2'
  ],
  materials: [
    'materials7',
    'materials8',
    'materials9'
  ],
};
```



