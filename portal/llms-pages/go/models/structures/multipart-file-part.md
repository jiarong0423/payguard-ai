# Multipart File Part

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRk11bHRpcGFydEZpbGVQYXJ0

MultipartFilePart.


# Class Name

`MultipartFilePart`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ByteLength` | `int` | Required | Byte length.<br><br>**Constraints**: `>= 0`, `<= 9999999` |
| `ContentType` | [`models.ContentTypeEnum`](http://localhost:3000/llms-pages/go/models/enumerations/content-type.md) | Required | Content type. |
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



