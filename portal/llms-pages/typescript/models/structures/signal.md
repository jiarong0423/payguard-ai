# Signal

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlNpZ25hbA

Signal.


# Interface Name

`Signal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | [`SignalCategory \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/signal-category.md) | Optional | This is a container for any-of cases. |
| `confidence` | [`SignalConfidence \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/signal-confidence.md) | Optional | This is a container for any-of cases. |
| `source` | [`Source2Enum \| undefined`](http://localhost:3000/llms-pages/typescript/models/enumerations/source-2.md) | Optional | Source. |


# Example

```ts
import {
  ConfidenceEnum,
  Signal,
  Source2Enum,
} from 'tradeglot-local-consolelib';

const signal: Signal = {
  category: 'String1',
  confidence: ConfidenceEnum.HIGH,
  source: Source2Enum.Channel3,
};
```



