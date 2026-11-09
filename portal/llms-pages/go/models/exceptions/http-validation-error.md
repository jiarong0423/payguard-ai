# HTTP Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationErrorException`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Detail` | [`[]models.ValidationError`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/validation-error.md) | Optional | Detail. |


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



