# Inject Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkluamVjdFJlcXVlc3Q

InjectRequest.


# Interface Name

`InjectRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `scenario` | [`Scenario5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/scenario-5.md) | Required | Scenario. |


# Example

```ts
import { InjectRequest, Scenario5Enum } from 'tradeglot-local-consolelib';

const injectRequest: InjectRequest = {
  scenario: Scenario5Enum.Burst,
};
```



