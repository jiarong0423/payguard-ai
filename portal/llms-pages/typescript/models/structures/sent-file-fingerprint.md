# Sent File Fingerprint

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlNlbnRGaWxlRmluZ2VycHJpbnQ

Plain SHA-256 of one file's exact bytes, recorded at the moment of a send so a later read-back can be compared.

The keyed `payload_sha256` cannot be checked outside the session; this one can. Never present on a preview.


# Interface Name

`SentFileFingerprint`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `byteLength` | `number` | Required | Byte length.<br><br>**Constraints**: `>= 0`, `<= 9999999` |
| `contentType` | [`ContentTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/content-type.md) | Required | Content type. |
| `filename` | `string` | Required | Filename.<br><br>**Constraints**: *Maximum Length*: `255` |
| `sha256` | `string` | Required | Sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |


# Example

```ts
import {
  ContentTypeEnum,
  SentFileFingerprint,
} from 'tradeglot-local-consolelib';

const sentFileFingerprint: SentFileFingerprint = {
  byteLength: 62,
  contentType: ContentTypeEnum.EnumImagejpeg,
  filename: 'filename6',
  sha256: 'sha2564',
};
```



