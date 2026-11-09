# HTTP Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationError`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Detail` | [`[]models.ValidationError`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/validation-error.md) | Optional | Detail. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    hTTPValidationError := models.HTTPValidationError{
        Detail:               []models.ValidationError{
            models.ValidationError{
                Ctx:                  models.ToPointer(interface{}("[key1, val1][key2, val2]")),
                Input:                models.ToPointer(interface{}("[key1, val1][key2, val2]")),
                Loc:                  []models.ValidationErrorLoc{
                    models.ValidationErrorLocContainer.FromString("String7"),
                    models.ValidationErrorLocContainer.FromString("String8"),
                    models.ValidationErrorLocContainer.FromString("String9"),
                },
                Msg:                  "msg2",
                Type:                 "type4",
            },
            models.ValidationError{
                Ctx:                  models.ToPointer(interface{}("[key1, val1][key2, val2]")),
                Input:                models.ToPointer(interface{}("[key1, val1][key2, val2]")),
                Loc:                  []models.ValidationErrorLoc{
                    models.ValidationErrorLocContainer.FromString("String7"),
                    models.ValidationErrorLocContainer.FromString("String8"),
                    models.ValidationErrorLocContainer.FromString("String9"),
                },
                Msg:                  "msg2",
                Type:                 "type4",
            },
        },
    }

}
```



