# Finding

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkZpbmRpbmc

Finding.


# Interface Name

`Finding`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | [`CategoryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/category.md) | Required | Category. |
| `code` | `string` | Required, Constant | Code.<br><br>**Value**: `'keyword_requires_policy_review'` |


# Example

```ts
import { CategoryEnum, Finding } from 'tradeglot-local-consolelib';

const finding: Finding = {
  category: CategoryEnum.UnsupportedFinancialPromise,
  code: 'keyword_requires_policy_review',
};
```



