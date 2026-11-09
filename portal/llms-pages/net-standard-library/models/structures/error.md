# Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkVycm9y

What was refused and why.


# Class Name

`Error`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Code` | `string` | Required | Stable machine-readable reason, for example session_required. |
| `Message` | `string` | Required | A plain sentence for a person. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

Error error = new Error
{
    Code = "code2",
    Message = "message4",
};
```



