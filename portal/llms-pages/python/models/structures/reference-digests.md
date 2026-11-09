# Reference Digests

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlJlZmVyZW5jZURpZ2VzdHM

ReferenceDigests.


# Class Name

`ReferenceDigests`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chunks_sha_256` | `str` | Required | Chunks sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `sources_sha_256` | `str` | Required | Sources sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |


# Example

```python
from tradeglotlocalconsole.models.reference_digests import ReferenceDigests

reference_digests = ReferenceDigests(
    chunks_sha_256='chunks_sha2564',
    sources_sha_256='sources_sha2566'
)
```



