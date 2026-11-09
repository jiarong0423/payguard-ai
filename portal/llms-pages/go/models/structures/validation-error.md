# Validation Error

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlZhbGlkYXRpb25FcnJvcg

ValidationError.


# Class Name

`ValidationError`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Ctx` | `*interface{}` | Optional | Ctx. |
| `Input` | `*interface{}` | Optional | Input. |
| `Loc` | [`[]models.ValidationErrorLoc`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/validation-error-loc.md) | Required | This is Array of a container for any-of cases. |
| `Msg` | `string` | Required | Msg. |
| `Type` | `string` | Required | Type. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    validationError := models.ValidationError{
        Ctx:                  models.ToPointer(interface{}("[key1, val1][key2, val2]")),
        Input:                models.ToPointer(interface{}("[key1, val1][key2, val2]")),
        Loc:                  []models.ValidationErrorLoc{
            models.ValidationErrorLocContainer.FromString("String9"),
        },
        Msg:                  "msg4",
        Type:                 "type2",
    }

}
```



