# Multipart File Part

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRk11bHRpcGFydEZpbGVQYXJ0

MultipartFilePart.


# Class Name

`MultipartFilePart`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ByteLength` | `int` | Required | Byte length.<br><br>**Constraints**: `>= 0`, `<= 9999999` |
| `ContentType` | [`models.ContentTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/content-type.md) | Required | Content type. |
| `Filename` | `string` | Required | Filename.<br><br>**Constraints**: *Maximum Length*: `255` |
| `Name` | `string` | Required | Name.<br><br>**Constraints**: *Pattern*: `^file[0-9]{1,3}$` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    multipartFilePart := models.MultipartFilePart{
        ByteLength:  138,
        ContentType: models.ContentTypeEnum_ENUMIMAGEJPEG,
        Filename:    "filename0",
        Name:        "name8",
    }

}
```



