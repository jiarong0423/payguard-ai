# HTTP Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Interface Name

`HTTPValidationError`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `detail` | [`ValidationError[] \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/validation-error.md) | Optional | Detail. |


# Example

```ts
import { HTTPValidationError } from 'tradeglot-local-consolelib';

const hTTPValidationError: HTTPValidationError = {
  detail: [
    {
      loc: [
        'String7',
        'String8',
        'String9'
      ],
      msg: 'msg2',
      type: 'type4',
      ctx: { 'key1': 'val1', 'key2': 'val2' },
      input: { 'key1': 'val1', 'key2': 'val2' },
    },
    {
      loc: [
        'String7',
        'String8',
        'String9'
      ],
      msg: 'msg2',
      type: 'type4',
      ctx: { 'key1': 'val1', 'key2': 'val2' },
      input: { 'key1': 'val1', 'key2': 'val2' },
    }
  ],
};
```



