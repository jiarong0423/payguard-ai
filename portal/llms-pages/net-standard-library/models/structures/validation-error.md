# Validation Error

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlZhbGlkYXRpb25FcnJvcg

ValidationError.


# Class Name

`ValidationError`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Ctx` | `object` | Optional | Ctx. |
| `Input` | `object` | Optional | Input. |
| `Loc` | [`List<ValidationErrorLoc>`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/validation-error-loc.md) | Required | This is List of a container for any-of cases. |
| `Msg` | `string` | Required | Msg. |
| `Type` | `string` | Required | Type. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;
using TradeGlotLocalConsole.Standard.Utilities;

ValidationError validationError = new ValidationError
{
    Loc = new List<ValidationErrorLoc>
    {
        ValidationErrorLoc.FromString("String9"),
    },
    Msg = "msg4",
    Type = "type2",
    Ctx = ApiHelper.JsonDeserialize<object>("{\"key1\":\"val1\",\"key2\":\"val2\"}"),
    Input = ApiHelper.JsonDeserialize<object>("{\"key1\":\"val1\",\"key2\":\"val2\"}"),
};
```



