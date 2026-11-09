# Connections Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkNvbm5lY3Rpb25zUmVzcG9uc2U

Deployment mode only. Never a key, a key's presence, a value or a variable name.


# Interface Name

`ConnectionsResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `mode` | [`ModeEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/mode.md) | Required | Mode. |


# Example

```ts
import { ConnectionsResponse, ModeEnum } from 'tradeglot-local-consolelib';

const connectionsResponse: ConnectionsResponse = {
  mode: ModeEnum.Local,
};
```



