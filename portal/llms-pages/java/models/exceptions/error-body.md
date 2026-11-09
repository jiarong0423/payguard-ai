# Error Body

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkVycm9yQm9keQ

The error body every refusal uses.


# Class Name

`ErrorBodyException`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Error` | [`Error`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/error.md) | Required | What was refused and why. | Error getError() | setError(Error error) |


# Example

```java
try {
    // make the API call
} catch (ErrorBodyException e) {
    e.printStackTrace();
} catch (ApiException e) {
    e.printStackTrace();
}
```



