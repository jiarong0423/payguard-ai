# Error Body

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkVycm9yQm9keQ

The error body every refusal uses.


# Class Name

`ErrorBodyError`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `error` | [`Error`](http://localhost:3000/llms-pages/typescript/models/structures/error.md) | Required | What was refused and why. |


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



