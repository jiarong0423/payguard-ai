# Finding

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkZpbmRpbmc

Finding.


# Class Name

`Finding`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Category` | [`models.CategoryEnum`](http://localhost:3000/llms-pages/go/models/enumerations/category.md) | Required | Category. |
| `Code` | `string` | Required, Constant | Code.<br><br>**Value**: `"keyword_requires_policy_review"` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    finding := models.Finding{
        Category: models.CategoryEnum_UNSUPPORTEDFINANCIALPROMISE,
        Code:     "keyword_requires_policy_review",
    }

}
```



