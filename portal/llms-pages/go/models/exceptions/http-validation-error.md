# HTTP Validation Error

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationErrorException`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Detail` | [`[]models.ValidationError`](http://localhost:3000/llms-pages/go/models/structures/validation-error.md) | Optional | Detail. |


# Example

```go
if err != nil {
    switch typedErr := err.(type) {
    case *errors.HTTPValidationErrorException:
        log.Fatalln(typedErr)
    default:
        log.Fatalln(err)
    }
}
```



