# Reference Digests

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlJlZmVyZW5jZURpZ2VzdHM

ReferenceDigests.


# Class Name

`ReferenceDigests`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chunks_sha_256` | `String` | Required | Chunks sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `sources_sha_256` | `String` | Required | Sources sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |


# Example

```ruby
reference_digests = ReferenceDigests.new(
  'chunks_sha2564',
  'sources_sha2566'
)
```



