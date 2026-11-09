# Reference Digests

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlJlZmVyZW5jZURpZ2VzdHM

ReferenceDigests.


# Class Name

`ReferenceDigests`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ChunksSha256` | `string` | Required | Chunks sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `SourcesSha256` | `string` | Required | Sources sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    referenceDigests := models.ReferenceDigests{
        ChunksSha256:  "chunks_sha2562",
        SourcesSha256: "sources_sha2564",
    }

}
```



