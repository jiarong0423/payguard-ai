# HTTP Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationError`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Detail` | [`List<ValidationError>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/validation-error.md) | Optional | Detail. | List<ValidationError> getDetail() | setDetail(List<ValidationError> detail) |


# Example

```java
import java.io.IOException;
import java.util.Arrays;
import m18000.m0.m0.m127.ApiHelper;
import m18000.m0.m0.m127.models.HTTPValidationError;
import m18000.m0.m0.m127.models.ValidationError;
import m18000.m0.m0.m127.models.containers.ValidationErrorLoc;

HTTPValidationError hTTPValidationError = new HTTPValidationError.Builder()
    .detail(Arrays.asList(
        new ValidationError.Builder(
            Arrays.asList(
                ValidationErrorLoc.fromString(
                    "String7"
                ),
                ValidationErrorLoc.fromString(
                    "String8"
                ),
                ValidationErrorLoc.fromString(
                    "String9"
                )
            ),
            "msg2",
            "type4"
        )
        .ctx(ApiHelper.deserialize("{\"key1\":\"val1\",\"key2\":\"val2\"}"))
        .input(ApiHelper.deserialize("{\"key1\":\"val1\",\"key2\":\"val2\"}"))
        .build(),
        new ValidationError.Builder(
            Arrays.asList(
                ValidationErrorLoc.fromString(
                    "String7"
                ),
                ValidationErrorLoc.fromString(
                    "String8"
                ),
                ValidationErrorLoc.fromString(
                    "String9"
                )
            ),
            "msg2",
            "type4"
        )
        .ctx(ApiHelper.deserialize("{\"key1\":\"val1\",\"key2\":\"val2\"}"))
        .input(ApiHelper.deserialize("{\"key1\":\"val1\",\"key2\":\"val2\"}"))
        .build()
    ))
    .build();
```



