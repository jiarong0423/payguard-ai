# Provide Evidence Response Sent Files

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlc3BvbnNlU2VudEZpbGVz


# Class Name

`ProvideEvidenceResponseSentFiles`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`List<SentFileFingerprint>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/sent-file-fingerprint.md) | ProvideEvidenceResponseSentFiles.fromListOfSentFileFingerprint(List<SentFileFingerprint> listOfSentFileFingerprint) |


# List<SentFileFingerprint>

## Initialization Code

### Example

```java
ProvideEvidenceResponseSentFiles.fromListOfSentFileFingerprint(
        Arrays.asList(
            new SentFileFingerprint.Builder(
                196,
                ContentTypeEnum.ENUM_IMAGEPNG,
                "filename6",
                "sha2566"
            )
            .build()
        )
    )
```



