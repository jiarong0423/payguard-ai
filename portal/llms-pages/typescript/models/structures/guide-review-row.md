# Guide Review Row

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3Um93

GuideReviewRow.


# Interface Name

`GuideReviewRow`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `item` | `string` | Required | Item. |
| `source` | [`Source9Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/source-9.md) | Required | Source. |
| `value` | `string` | Required | Value.<br><br>**Constraints**: *Maximum Length*: `120` |


# Example

```ts
import { GuideReviewRow, Source9Enum } from 'tradeglot-local-consolelib';

const guideReviewRow: GuideReviewRow = {
  item: 'item6',
  source: Source9Enum.Words,
  value: 'value6',
};
```



