# HTTP Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationErrorException`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Detail` | [`List<ValidationError>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/validation-error.md) | Optional | Detail. | List<ValidationError> getDetail() | setDetail(List<ValidationError> detail) |


# Example

```java
try {
    // make the API call
} catch (HTTPValidationErrorException e) {
    e.printStackTrace();
} catch (ApiException e) {
    e.printStackTrace();
}
```



