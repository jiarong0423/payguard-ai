# Reference Digests

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlJlZmVyZW5jZURpZ2VzdHM

ReferenceDigests.


# Class Name

`ReferenceDigests`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `ChunksSha256` | `String` | Required | Chunks sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getChunksSha256() | setChunksSha256(String chunksSha256) |
| `SourcesSha256` | `String` | Required | Sources sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getSourcesSha256() | setSourcesSha256(String sourcesSha256) |


# Example

```java
import m18000.m0.m0.m127.models.ReferenceDigests;

ReferenceDigests referenceDigests = new ReferenceDigests.Builder(
    "chunks_sha2562",
    "sources_sha2564"
)
.build();
```



