# Health Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkhlYWx0aFJlc3BvbnNl

HealthResponse.


# Interface Name

`HealthResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `mode` | `string` | Required, Constant | Mode.<br><br>**Value**: `'demo'` |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |
| `status` | `string` | Required, Constant | Status.<br><br>**Value**: `'ok'` |
| `version` | `string` | Required | Version. |


# Example

```ts
import { HealthResponse } from 'tradeglot-local-consolelib';

const healthResponse: HealthResponse = {
  mode: 'demo',
  source: 'synthetic',
  status: 'ok',
  version: 'version0',
};
```



