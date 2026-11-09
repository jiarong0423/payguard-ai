# Error Body

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkVycm9yQm9keQ

The error body every refusal uses.


# Class Name

`ErrorBodyException`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Error` | [`Error`](http://localhost:3000/llms-pages/net-standard-library/models/structures/error.md) | Required | What was refused and why. |


# Example

```csharp
try
{
    // make the API call
}
catch (ApiException e)
{
    if (e is ErrorBodyException)
    {
        // TODO: Handle ErrorBodyException
        Console.WriteLine(e.Message);
    }
}
```



