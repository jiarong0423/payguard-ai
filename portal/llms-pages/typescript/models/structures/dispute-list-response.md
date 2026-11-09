# Dispute List Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkRpc3B1dGVMaXN0UmVzcG9uc2U

DisputeListResponse.


# Interface Name

`DisputeListResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `dataSourceLabel` | [`DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/data-source-label.md) | Required | Data source label. |
| `environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` |
| `evidenceClass` | [`EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `items` | [`DisputeRecord[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/dispute-record.md) | Required | Items.<br><br>**Constraints**: *Maximum Items*: `20` |
| `observedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `paypalDebugId` | [`DisputeListResponsePaypalDebugId \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/dispute-list-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `providerSubmission` | [`ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `readback` | `string` | Required, Constant | Readback.<br><br>**Value**: `'GET_LIST'` |
| `source` | [`SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/source.md) | Required | Source. |


# Example

```ts
import {
  DataSourceLabelEnum,
  DisputeLifeCycleStageEnum,
  DisputeListResponse,
  EvidenceClassEnum,
  ProviderSubmissionEnum,
  Reason2Enum,
  SourceEnum,
  Status3Enum,
} from 'tradeglot-local-consolelib';

const disputeListResponse: DisputeListResponse = {
  dataSourceLabel: DataSourceLabelEnum.Sandbox,
  environment: 'sandbox',
  evidenceClass: EvidenceClassEnum.SYNTHETICTESTRESPONSE,
  items: [
    {
      createTime: 'create_time4',
      disputeAmount: {
        currencyCode: 'currency_code6',
        value: 'value0',
      },
      disputeId: 'dispute_id0',
      disputeLifeCycleStage: DisputeLifeCycleStageEnum.PREARBITRATION,
      reason: Reason2Enum.CREDITNOTPROCESSED,
      status: Status3Enum.UNDERREVIEW,
      disputeState: 'String1',
      sellerResponseDueDate: 'String7',
      updateTime: 'String1',
    }
  ],
  observedAt: 'observed_at4',
  providerSubmission: ProviderSubmissionEnum.NOTPERFORMED,
  readback: 'GET_LIST',
  source: SourceEnum.PaypalSandbox,
  paypalDebugId: 'String1',
};
```



