# Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlZhbGlkYXRpb25FcnJvcg

ValidationError.


# Interface Name

`ValidationError`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ctx` | `unknown \| undefined` | Optional | Ctx. |
| `input` | `unknown \| undefined` | Optional | Input. |
| `loc` | [`ValidationErrorLoc[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/validation-error-loc.md) | Required | This is Array of a container for any-of cases. |
| `msg` | `string` | Required | Msg. |
| `type` | `string` | Required | Type. |


# Example

```ts
import { ValidationError } from 'tradeglot-local-consolelib';

const validationError: ValidationError = {
  loc: [
    'String9'
  ],
  msg: 'msg4',
  type: 'type2',
  ctx: { 'key1': 'val1', 'key2': 'val2' },
  input: { 'key1': 'val1', 'key2': 'val2' },
};
```



