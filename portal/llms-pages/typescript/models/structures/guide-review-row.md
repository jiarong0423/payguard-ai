# Guide Review Row

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3Um93

GuideReviewRow.


# Interface Name

`GuideReviewRow`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `item` | `string` | Required | Item. |
| `source` | [`Source9Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/source-9.md) | Required | Source. |
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



