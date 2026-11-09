# Case Route Match

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkNhc2VSb3V0ZU1hdGNo

CaseRouteMatch.


# Interface Name

`CaseRouteMatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | [`CaseRouteMatchCategory`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/case-route-match-category.md) | Required | This is a container for any-of cases. |
| `exactWords` | `string[]` | Required | Exact words.<br><br>**Constraints**: *Maximum Items*: `8`, *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z0-9]+$` |
| `matchType` | [`MatchTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/match-type.md) | Required | Match type. |
| `productId` | `string` | Required | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `score` | `number` | Required | Score.<br><br>**Constraints**: `>= 0`, `<= 1` |
| `title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```ts
import { CaseRouteMatch, MatchTypeEnum } from 'tradeglot-local-consolelib';

const caseRouteMatch: CaseRouteMatch = {
  category: 'String7',
  exactWords: [
    'exact_words4',
    'exact_words3'
  ],
  matchType: MatchTypeEnum.Exact,
  productId: 'product_id4',
  score: 1,
  title: 'title4',
};
```



