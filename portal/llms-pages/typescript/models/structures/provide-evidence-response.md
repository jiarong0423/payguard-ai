# Provide Evidence Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlc3BvbnNl

ProvideEvidenceResponse.


# Interface Name

`ProvideEvidenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `confirmToken` | [`ProvideEvidenceResponseConfirmToken \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/provide-evidence-response-confirm-token.md) | Optional | This is a container for any-of cases. |
| `contentType` | `string` | Required, Constant | Content type.<br><br>**Value**: `'multipart/form-data'` |
| `dataSourceLabel` | [`DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/data-source-label.md) | Required | Data source label. |
| `disputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` |
| `evidenceClass` | [`EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `externalSend` | [`ExternalSendEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/external-send.md) | Required | External send. |
| `files` | [`MultipartFilePart[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/multipart-file-part.md) | Required | Files.<br><br>**Constraints**: *Maximum Items*: `20` |
| `humanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `'True'` |
| `input` | [`EvidenceInput`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/evidence-input.md) | Required | EvidenceInput. |
| `method` | `string` | Required, Constant | Method.<br><br>**Value**: `'POST'` |
| `observedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `path` | `string` | Required | Path.<br><br>**Constraints**: *Pattern*: `^/v1/customer/disputes/PP-[A-Z0-9][A-Z0-9-]{2,62}/provide-evidence$` |
| `payloadSha256` | [`ProvideEvidenceResponsePayloadSha256 \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/provide-evidence-response-payload-sha-256.md) | Optional | This is a container for any-of cases. |
| `paypalDebugId` | [`ProvideEvidenceResponsePaypalDebugId \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/provide-evidence-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `providerSubmission` | [`ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `readback` | [`Readback1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/readback-1.md) | Required | Readback. |
| `sendGuard` | [`SendGuard`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/send-guard.md) | Required | (r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4). |
| `source` | [`SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/source.md) | Required | Source. |
| `submitFlagEnabled` | `boolean` | Required | Submit flag enabled. |


# Example

```ts
import {
  AccountStatusEnum,
  CarrierNameEnum,
  ContentTypeEnum,
  DataSourceLabelEnum,
  EvidenceClassEnum,
  ExternalSendEnum,
  ProvideEvidenceResponse,
  ProviderSubmissionEnum,
  Readback1Enum,
  SourceEnum,
} from 'tradeglot-local-consolelib';

const provideEvidenceResponse: ProvideEvidenceResponse = {
  caseRef: 'case_ref2',
  contentType: 'multipart/form-data',
  dataSourceLabel: DataSourceLabelEnum.Sandbox,
  disputeId: 'dispute_id0',
  environment: 'sandbox',
  evidenceClass: EvidenceClassEnum.AUTHENTICSANDBOXRESPONSE,
  externalSend: ExternalSendEnum.FROZEN,
  files: [
    {
      byteLength: 68,
      contentType: ContentTypeEnum.EnumImagepng,
      filename: 'filename6',
      name: 'name4',
    }
  ],
  humanReviewRequired: 'True',
  input: {
    evidences: [
      {
        evidenceInfo: {
          trackingInfo: [
            {
              carrierName: CarrierNameEnum.DHL,
              trackingNumber: 'tracking_number6',
              carrierNameOther: 'String1',
            }
          ],
        },
        evidenceType: 'evidence_type2',
        notes: 'notes2',
      }
    ],
  },
  method: 'POST',
  observedAt: 'observed_at2',
  path: 'path2',
  providerSubmission: ProviderSubmissionEnum.NOTPERFORMED,
  readback: Readback1Enum.PROVIDEEVIDENCEPREVIEW,
  sendGuard: {
    accountStatus: AccountStatusEnum.MATCH,
    caseRef: 'case_ref6',
    disputeMasked: 'dispute_masked0',
    boundDisputeMasked: 'String3',
    caseReason: 'String7',
    disputeAmount: {
      currencyCode: 'currency_code0',
      value: 'value6',
    },
    disputeReason: 'String9',
    disputeSellerMasked: 'String1',
  },
  source: SourceEnum.PaypalSandbox,
  submitFlagEnabled: false,
  confirmToken: 'String9',
  payloadSha256: 'String9',
  paypalDebugId: 'String9',
};
```



