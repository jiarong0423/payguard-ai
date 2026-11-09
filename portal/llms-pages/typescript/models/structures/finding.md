# Finding

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkZpbmRpbmc

Finding.


# Interface Name

`Finding`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | [`CategoryEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/category.md) | Required | Category. |
| `code` | `string` | Required, Constant | Code.<br><br>**Value**: `'keyword_requires_policy_review'` |


# Example

```ts
import { CategoryEnum, Finding } from 'tradeglot-local-consolelib';

const finding: Finding = {
  category: CategoryEnum.UnsupportedFinancialPromise,
  code: 'keyword_requires_policy_review',
};
```



