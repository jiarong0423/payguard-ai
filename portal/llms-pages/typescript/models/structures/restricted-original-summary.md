# Restricted Original Summary

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlJlc3RyaWN0ZWRPcmlnaW5hbFN1bW1hcnk

RestrictedOriginalSummary.


# Interface Name

`RestrictedOriginalSummary`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `attachmentCount` | `number` | Required | Attachment count.<br><br>**Constraints**: `>= 0`, `<= 20` |
| `contentReturned` | `string` | Required, Constant | Content returned.<br><br>**Value**: `'False'` |
| `custody` | `string` | Required, Constant | Custody.<br><br>**Value**: `'SESSION_MEMORY_ONLY'` |
| `dataClass` | `string` | Required, Constant | Data class.<br><br>**Value**: `'SYNTHETIC_RESTRICTED_EVIDENCE'` |
| `persistentStorage` | `string` | Required, Constant | Persistent storage.<br><br>**Value**: `'NOT_IMPLEMENTED'` |
| `productionPiiVault` | `string` | Required, Constant | Production pii vault.<br><br>**Value**: `'NOT_IMPLEMENTED'` |
| `profile` | `string` | Required, Constant | Profile.<br><br>**Value**: `'RESTRICTED_ORIGINAL_METADATA_V1'` |
| `proofRecordCount` | `number` | Required | Proof record count.<br><br>**Constraints**: `>= 0`, `<= 128` |
| `providerSubmission` | `string` | Required, Constant | Provider submission.<br><br>**Value**: `'NOT_PERFORMED'` |
| `schemaVersion` | `number` | Required, Constant | Schema version.<br><br>**Value**: `1` |


# Example

```ts
import { RestrictedOriginalSummary } from 'tradeglot-local-consolelib';

const restrictedOriginalSummary: RestrictedOriginalSummary = {
  attachmentCount: 20,
  contentReturned: 'False',
  custody: 'SESSION_MEMORY_ONLY',
  dataClass: 'SYNTHETIC_RESTRICTED_EVIDENCE',
  persistentStorage: 'NOT_IMPLEMENTED',
  productionPiiVault: 'NOT_IMPLEMENTED',
  profile: 'RESTRICTED_ORIGINAL_METADATA_V1',
  proofRecordCount: 82,
  providerSubmission: 'NOT_PERFORMED',
  schemaVersion: 1,
};
```



