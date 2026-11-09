# Error Body

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkVycm9yQm9keQ

The error body every refusal uses.


# Class Name

`ErrorBodyError`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `error` | [`Error`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/error.md) | Required | What was refused and why. |


# Example

```ts
try {
  // make the API call
} catch (error) {
  if (error instanceof ErrorBodyError) {
    console.log(error.result);
  }
}
```



