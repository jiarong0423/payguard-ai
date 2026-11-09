# Restricted Original Summary

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlJlc3RyaWN0ZWRPcmlnaW5hbFN1bW1hcnk

RestrictedOriginalSummary.


# Class Name

`RestrictedOriginalSummary`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AttachmentCount` | `int` | Required | Attachment count.<br><br>**Constraints**: `>= 0`, `<= 20` | int getAttachmentCount() | setAttachmentCount(int attachmentCount) |
| `ContentReturned` | `String` | Required, Constant | Content returned.<br><br>**Value**: `"False"` | String getContentReturned() | setContentReturned(String contentReturned) |
| `Custody` | `String` | Required, Constant | Custody.<br><br>**Value**: `"SESSION_MEMORY_ONLY"` | String getCustody() | setCustody(String custody) |
| `DataClass` | `String` | Required, Constant | Data class.<br><br>**Value**: `"SYNTHETIC_RESTRICTED_EVIDENCE"` | String getDataClass() | setDataClass(String dataClass) |
| `PersistentStorage` | `String` | Required, Constant | Persistent storage.<br><br>**Value**: `"NOT_IMPLEMENTED"` | String getPersistentStorage() | setPersistentStorage(String persistentStorage) |
| `ProductionPiiVault` | `String` | Required, Constant | Production pii vault.<br><br>**Value**: `"NOT_IMPLEMENTED"` | String getProductionPiiVault() | setProductionPiiVault(String productionPiiVault) |
| `Profile` | `String` | Required, Constant | Profile.<br><br>**Value**: `"RESTRICTED_ORIGINAL_METADATA_V1"` | String getProfile() | setProfile(String profile) |
| `ProofRecordCount` | `int` | Required | Proof record count.<br><br>**Constraints**: `>= 0`, `<= 128` | int getProofRecordCount() | setProofRecordCount(int proofRecordCount) |
| `ProviderSubmission` | `String` | Required, Constant | Provider submission.<br><br>**Value**: `"NOT_PERFORMED"` | String getProviderSubmission() | setProviderSubmission(String providerSubmission) |
| `SchemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` | int getSchemaVersion() | setSchemaVersion(int schemaVersion) |


# Example

```java
import m18000.m0.m0.m127.models.RestrictedOriginalSummary;

RestrictedOriginalSummary restrictedOriginalSummary = new RestrictedOriginalSummary.Builder(
    20,
    "False",
    "SESSION_MEMORY_ONLY",
    "SYNTHETIC_RESTRICTED_EVIDENCE",
    "NOT_IMPLEMENTED",
    "NOT_IMPLEMENTED",
    "RESTRICTED_ORIGINAL_METADATA_V1",
    82,
    "NOT_PERFORMED",
    1
)
.build();
```



