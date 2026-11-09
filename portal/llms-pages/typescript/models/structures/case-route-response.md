# Case Route Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkNhc2VSb3V0ZVJlc3BvbnNl

Fuzzy case routing: which goods group (and so which dispute items) applies. Code decides; advisory only.


# Interface Name

`CaseRouteResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `affectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `'False'` |
| `decidedBy` | `string` | Required, Constant | Decided by.<br><br>**Value**: `'code'` |
| `filteredOut` | `number` | Required | Filtered out.<br><br>**Constraints**: `>= 0`, `<= 1000` |
| `items` | `string[]` | Required | Items.<br><br>**Constraints**: *Maximum Items*: `12` |
| `matchedWord` | [`CaseRouteResponseMatchedWord`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/case-route-response-matched-word.md) | Required | This is a container for any-of cases. |
| `matches` | [`CaseRouteMatch[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/case-route-match.md) | Required | Matches.<br><br>**Constraints**: *Maximum Items*: `3` |
| `query` | [`CaseRouteResponseQuery`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/case-route-response-query.md) | Required | This is a container for any-of cases. |
| `reason` | [`Reason1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/reason-1.md) | Required | Reason. |
| `route` | [`RouteEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/route.md) | Required | Route. |


# Example

```ts
import {
  CaseRouteResponse,
  MatchTypeEnum,
  Reason1Enum,
  RouteEnum,
} from 'tradeglot-local-consolelib';

const caseRouteResponse: CaseRouteResponse = {
  affectsDecision: 'False',
  decidedBy: 'code',
  filteredOut: 76,
  items: [
    'items3',
    'items4',
    'items5'
  ],
  matchedWord: 'String5',
  matches: [
    {
      category: 'String1',
      exactWords: [
        'exact_words2',
        'exact_words3',
        'exact_words4'
      ],
      matchType: MatchTypeEnum.Exact,
      productId: 'product_id8',
      score: 1,
      title: 'title2',
    }
  ],
  query: 'String7',
  reason: Reason1Enum.NoCloseMatch,
  route: RouteEnum.Physical,
};
```



