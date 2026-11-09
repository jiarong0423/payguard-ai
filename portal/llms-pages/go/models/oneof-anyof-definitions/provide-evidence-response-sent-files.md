# Provide Evidence Response Sent Files

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlc3BvbnNlU2VudEZpbGVz


# Class Name

`ProvideEvidenceResponseSentFiles`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`[]models.SentFileFingerprint`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/sent-file-fingerprint.md) | models.ProvideEvidenceResponseSentFilesContainer.FromArrayOfSentFileFingerprint([]models.SentFileFingerprint arrayOfSentFileFingerprint) |


# []models.SentFileFingerprint

## Initialization Code

### Example

```go
value := models.ProvideEvidenceResponseSentFilesContainer.FromArrayOfSentFileFingerprint([]models.SentFileFingerprint{
    models.SentFileFingerprint{
        ByteLength:  196,
        ContentType: models.ContentTypeEnum_ENUMIMAGEPNG,
        Filename:    "filename6",
        Sha256:      "sha2566",
    },
})
```



