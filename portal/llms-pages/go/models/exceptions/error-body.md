# Error Body

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkVycm9yQm9keQ

The error body every refusal uses.


# Class Name

`ErrorBodyException`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Error` | [`models.Error`](http://localhost:3000/llms-pages/go/models/structures/error.md) | Required | What was refused and why. |


# Example

```go
if err != nil {
    switch typedErr := err.(type) {
    case *errors.ErrorBodyException:
        log.Fatalln(typedErr)
    default:
        log.Fatalln(err)
    }
}
```



