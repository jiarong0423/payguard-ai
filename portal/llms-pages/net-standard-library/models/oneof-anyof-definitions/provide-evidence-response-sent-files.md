# Provide Evidence Response Sent Files

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlc3BvbnNlU2VudEZpbGVz


# Class Name

`ProvideEvidenceResponseSentFiles`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`List<SentFileFingerprint>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/sent-file-fingerprint.md) | ProvideEvidenceResponseSentFiles.FromListOfSentFileFingerprint(List<SentFileFingerprint> listOfSentFileFingerprint) |


# List<SentFileFingerprint>

## Initialization Code

### Example

```csharp
ProvideEvidenceResponseSentFiles value = ProvideEvidenceResponseSentFiles.FromListOfSentFileFingerprint(
    new List<SentFileFingerprint>
    {
        new SentFileFingerprint
        {
            ByteLength = 196,
            ContentType = ContentTypeEnum.EnumImagepng,
            Filename = "filename6",
            Sha256 = "sha2566",
        },
    }
);
```



