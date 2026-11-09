# Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlZhbGlkYXRpb25FcnJvcg

ValidationError.


# Class Name

`ValidationError`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Ctx` | `Object` | Optional | Ctx. | Object getCtx() | setCtx(Object ctx) |
| `Input` | `Object` | Optional | Input. | Object getInput() | setInput(Object input) |
| `Loc` | [`List<ValidationErrorLoc>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/validation-error-loc.md) | Required | This is List of a container for any-of cases. | List<ValidationErrorLoc> getLoc() | setLoc(List<ValidationErrorLoc> loc) |
| `Msg` | `String` | Required | Msg. | String getMsg() | setMsg(String msg) |
| `Type` | `String` | Required | Type. | String getType() | setType(String type) |


# Example

```java
import java.io.IOException;
import java.util.Arrays;
import m18000.m0.m0.m127.ApiHelper;
import m18000.m0.m0.m127.models.ValidationError;
import m18000.m0.m0.m127.models.containers.ValidationErrorLoc;

ValidationError validationError = new ValidationError.Builder(
    Arrays.asList(
        ValidationErrorLoc.fromString(
            "String9"
        )
    ),
    "msg4",
    "type2"
)
.ctx(ApiHelper.deserialize("{\"key1\":\"val1\",\"key2\":\"val2\"}"))
.input(ApiHelper.deserialize("{\"key1\":\"val1\",\"key2\":\"val2\"}"))
.build();
```



