# Error

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkVycm9y

What was refused and why.


# Interface Name

`Error`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `code` | `string` | Required | Stable machine-readable reason, for example session_required. |
| `message` | `string` | Required | A plain sentence for a person. |


# Example

```ts
import { Error } from 'tradeglot-local-consolelib';

const error: Error = {
  code: 'code2',
  message: 'message4',
};
```



