# Add Tracking Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkFkZFRyYWNraW5nUmVzcG9uc2U

AddTrackingResponse.


# Interface Name

`AddTrackingResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`TrackerBatch`](http://localhost:3000/llms-pages/typescript/models/structures/tracker-batch.md) | Required | TrackerBatch. |
| `caseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `confirmToken` | [`AddTrackingResponseConfirmToken \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/add-tracking-response-confirm-token.md) | Optional | This is a container for any-of cases. |
| `contentType` | `string` | Required, Constant | Content type.<br><br>**Value**: `'application/json'` |
| `dataSourceLabel` | [`DataSourceLabelEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/data-source-label.md) | Required | Data source label. |
| `disputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` |
| `evidenceClass` | [`EvidenceClassEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `externalSend` | [`ExternalSendEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/external-send.md) | Required | External send. |
| `humanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `'True'` |
| `method` | `string` | Required, Constant | Method.<br><br>**Value**: `'POST'` |
| `observedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `path` | `string` | Required, Constant | Path.<br><br>**Value**: `'/v1/shipping/trackers-batch'` |
| `payloadSha256` | [`AddTrackingResponsePayloadSha256 \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/add-tracking-response-payload-sha-256.md) | Optional | This is a container for any-of cases. |
| `paypalDebugId` | [`AddTrackingResponsePaypalDebugId \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/add-tracking-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `providerSubmission` | [`ProviderSubmissionEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `readback` | [`ReadbackEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/readback.md) | Required | Readback. |
| `sendGuard` | [`SendGuard`](http://localhost:3000/llms-pages/typescript/models/structures/send-guard.md) | Required | (r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4). |
| `source` | [`SourceEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/source.md) | Required | Source. |
| `submitFlagEnabled` | `boolean` | Required | Submit flag enabled. |


# Example

```ts
import {
  AccountStatusEnum,
  AddTrackingResponse,
  CarrierEnum,
  DataSourceLabelEnum,
  EvidenceClassEnum,
  ExternalSendEnum,
  ProviderSubmissionEnum,
  ReadbackEnum,
  SourceEnum,
} from 'tradeglot-local-consolelib';

const addTrackingResponse: AddTrackingResponse = {
  body: {
    trackers: [
      {
        carrier: CarrierEnum.JPJAPANPOST,
        status: 'SHIPPED',
        trackingNumber: 'tracking_number0',
        transactionId: 'transaction_id0',
        carrierNameOther: 'String5',
      }
    ],
  },
  caseRef: 'case_ref6',
  contentType: 'application/json',
  dataSourceLabel: DataSourceLabelEnum.Sandbox,
  disputeId: 'dispute_id4',
  environment: 'sandbox',
  evidenceClass: EvidenceClassEnum.AUTHENTICSANDBOXRESPONSE,
  externalSend: ExternalSendEnum.FROZEN,
  humanReviewRequired: 'True',
  method: 'POST',
  observedAt: 'observed_at6',
  path: '/v1/shipping/trackers-batch',
  providerSubmission: ProviderSubmissionEnum.NOTPERFORMED,
  readback: ReadbackEnum.ADDTRACKINGPREVIEW,
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



