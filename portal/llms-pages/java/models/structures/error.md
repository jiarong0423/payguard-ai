# Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkVycm9y

What was refused and why.


# Class Name

`Error`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Code` | `String` | Required | Stable machine-readable reason, for example session_required. | String getCode() | setCode(String code) |
| `Message` | `String` | Required | A plain sentence for a person. | String getMessage() | setMessage(String message) |


# Example

```java
import m18000.m0.m0.m127.models.Error;

Error error = new Error.Builder(
    "code2",
    "message4"
)
.build();
```



