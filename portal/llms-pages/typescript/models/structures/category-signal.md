# Category Signal

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkNhdGVnb3J5U2lnbmFs

CategorySignal.


# Interface Name

`CategorySignal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | [`CategorySignalCategory`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/category-signal-category.md) | Required | This is a container for any-of cases. |
| `confidence` | [`CategorySignalConfidence`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/category-signal-confidence.md) | Required | This is a container for any-of cases. |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'channel3'` |


# Example

```ts
import { CategorySignal, ConfidenceEnum } from 'tradeglot-local-consolelib';

const categorySignal: CategorySignal = {
  category: 'String1',
  confidence: ConfidenceEnum.HIGH,
  source: 'channel3',
};
```



