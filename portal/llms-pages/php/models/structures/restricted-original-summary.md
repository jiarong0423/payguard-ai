# Restricted Original Summary

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlJlc3RyaWN0ZWRPcmlnaW5hbFN1bW1hcnk

RestrictedOriginalSummary.


# Class Name

`RestrictedOriginalSummary`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `attachmentCount` | `int` | Required | Attachment count.<br><br>**Constraints**: `>= 0`, `<= 20` | getAttachmentCount(): int | setAttachmentCount(int attachmentCount): void |
| `contentReturned` | `string` | Required, Constant | Content returned.<br><br>**Value**: `'False'` | getContentReturned(): string | setContentReturned(string contentReturned): void |
| `custody` | `string` | Required, Constant | Custody.<br><br>**Value**: `'SESSION_MEMORY_ONLY'` | getCustody(): string | setCustody(string custody): void |
| `dataClass` | `string` | Required, Constant | Data class.<br><br>**Value**: `'SYNTHETIC_RESTRICTED_EVIDENCE'` | getDataClass(): string | setDataClass(string dataClass): void |
| `persistentStorage` | `string` | Required, Constant | Persistent storage.<br><br>**Value**: `'NOT_IMPLEMENTED'` | getPersistentStorage(): string | setPersistentStorage(string persistentStorage): void |
| `productionPiiVault` | `string` | Required, Constant | Production pii vault.<br><br>**Value**: `'NOT_IMPLEMENTED'` | getProductionPiiVault(): string | setProductionPiiVault(string productionPiiVault): void |
| `profile` | `string` | Required, Constant | Profile.<br><br>**Value**: `'RESTRICTED_ORIGINAL_METADATA_V1'` | getProfile(): string | setProfile(string profile): void |
| `proofRecordCount` | `int` | Required | Proof record count.<br><br>**Constraints**: `>= 0`, `<= 128` | getProofRecordCount(): int | setProofRecordCount(int proofRecordCount): void |
| `providerSubmission` | `string` | Required, Constant | Provider submission.<br><br>**Value**: `'NOT_PERFORMED'` | getProviderSubmission(): string | setProviderSubmission(string providerSubmission): void |
| `schemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` | getSchemaVersion(): int | setSchemaVersion(int schemaVersion): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\RestrictedOriginalSummaryBuilder;

$restrictedOriginalSummary = RestrictedOriginalSummaryBuilder::init(
    20,
    82
)->build();
```



