# HTTP Validation Error

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationErrorException`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Detail` | [`List<ValidationError>`](http://localhost:3000/llms-pages/java/models/structures/validation-error.md) | Optional | Detail. | List<ValidationError> getDetail() | setDetail(List<ValidationError> detail) |


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



