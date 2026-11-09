# HTTP Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationError`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Detail` | [`List<ValidationError>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/validation-error.md) | Optional | Detail. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;
using TradeGlotLocalConsole.Standard.Utilities;

HTTPValidationError hTTPValidationError = new HTTPValidationError
{
    Detail = new List<ValidationError>
    {
        new ValidationError
        {
            Loc = new List<ValidationErrorLoc>
            {
                ValidationErrorLoc.FromString("String7"),
                ValidationErrorLoc.FromString("String8"),
                ValidationErrorLoc.FromString("String9"),
            },
            Msg = "msg2",
            Type = "type4",
            Ctx = ApiHelper.JsonDeserialize<object>("{\"key1\":\"val1\",\"key2\":\"val2\"}"),
            Input = ApiHelper.JsonDeserialize<object>("{\"key1\":\"val1\",\"key2\":\"val2\"}"),
        },
        new ValidationError
        {
            Loc = new List<ValidationErrorLoc>
            {
                ValidationErrorLoc.FromString("String7"),
                ValidationErrorLoc.FromString("String8"),
                ValidationErrorLoc.FromString("String9"),
            },
            Msg = "msg2",
            Type = "type4",
            Ctx = ApiHelper.JsonDeserialize<object>("{\"key1\":\"val1\",\"key2\":\"val2\"}"),
            Input = ApiHelper.JsonDeserialize<object>("{\"key1\":\"val1\",\"key2\":\"val2\"}"),
        },
    },
};
```



