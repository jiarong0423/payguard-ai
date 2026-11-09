# Restricted Original Summary

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlJlc3RyaWN0ZWRPcmlnaW5hbFN1bW1hcnk

RestrictedOriginalSummary.


# Class Name

`RestrictedOriginalSummary`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AttachmentCount` | `int` | Required | Attachment count.<br><br>**Constraints**: `>= 0`, `<= 20` |
| `ContentReturned` | `string` | Required, Constant | Content returned.<br><br>**Value**: `"False"` |
| `Custody` | `string` | Required, Constant | Custody.<br><br>**Value**: `"SESSION_MEMORY_ONLY"` |
| `DataClass` | `string` | Required, Constant | Data class.<br><br>**Value**: `"SYNTHETIC_RESTRICTED_EVIDENCE"` |
| `PersistentStorage` | `string` | Required, Constant | Persistent storage.<br><br>**Value**: `"NOT_IMPLEMENTED"` |
| `ProductionPiiVault` | `string` | Required, Constant | Production pii vault.<br><br>**Value**: `"NOT_IMPLEMENTED"` |
| `Profile` | `string` | Required, Constant | Profile.<br><br>**Value**: `"RESTRICTED_ORIGINAL_METADATA_V1"` |
| `ProofRecordCount` | `int` | Required | Proof record count.<br><br>**Constraints**: `>= 0`, `<= 128` |
| `ProviderSubmission` | `string` | Required, Constant | Provider submission.<br><br>**Value**: `"NOT_PERFORMED"` |
| `SchemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

RestrictedOriginalSummary restrictedOriginalSummary = new RestrictedOriginalSummary
{
    AttachmentCount = 20,
    ContentReturned = "False",
    Custody = "SESSION_MEMORY_ONLY",
    DataClass = "SYNTHETIC_RESTRICTED_EVIDENCE",
    PersistentStorage = "NOT_IMPLEMENTED",
    ProductionPiiVault = "NOT_IMPLEMENTED",
    Profile = "RESTRICTED_ORIGINAL_METADATA_V1",
    ProofRecordCount = 82,
    ProviderSubmission = "NOT_PERFORMED",
    SchemaVersion = 1,
};
```



