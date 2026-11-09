# Inject Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkluamVjdFJlcXVlc3Q

InjectRequest.


# Interface Name

`InjectRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `scenario` | [`Scenario5Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/scenario-5.md) | Required | Scenario. |


# Example

```ts
import { InjectRequest, Scenario5Enum } from 'tradeglot-local-consolelib';

const injectRequest: InjectRequest = {
  scenario: Scenario5Enum.Burst,
};
```



