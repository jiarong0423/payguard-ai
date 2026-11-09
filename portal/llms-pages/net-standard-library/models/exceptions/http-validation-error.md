# HTTP Validation Error

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationErrorException`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Detail` | [`List<ValidationError>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/validation-error.md) | Optional | Detail. |


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



