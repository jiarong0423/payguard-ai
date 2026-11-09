# HTTP Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationErrorException`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Detail` | [`List<ValidationError>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/validation-error.md) | Optional | Detail. |


# Example

```csharp
try
{
    // make the API call
}
catch (ApiException e)
{
    if (e is HTTPValidationErrorException)
    {
        // TODO: Handle HTTPValidationErrorException
        Console.WriteLine(e.Message);
    }
}
```



