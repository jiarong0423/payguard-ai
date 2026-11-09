# HTTP Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationError`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `detail` | [`ValidationError[] \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/validation-error.md) | Optional | Detail. |


# Example

```ts
try {
  // make the API call
} catch (error) {
  if (error instanceof HTTPValidationError) {
    console.log(error.result);
  }
}
```



