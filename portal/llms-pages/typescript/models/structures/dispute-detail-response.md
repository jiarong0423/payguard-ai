# Dispute Detail Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkRpc3B1dGVEZXRhaWxSZXNwb25zZQ

DisputeDetailResponse.


# Interface Name

`DisputeDetailResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `createTime` | `string` | Required | Create time.<br><br>**Constraints**: *Pattern*: `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$` |
| `dataSourceLabel` | [`DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/data-source-label.md) | Required | Data source label. |
| `disputeAmount` | [`ProviderMoney`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/provider-money.md) | Required | ProviderMoney. |
| `disputeChannel` | [`DisputeDetailResponseDisputeChannel \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/dispute-detail-response-dispute-channel.md) | Optional | This is a container for any-of cases. |
| `disputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `disputeLifeCycleStage` | [`DisputeLifeCycleStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `disputeState` | [`DisputeDetailResponseDisputeState \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/dispute-detail-response-dispute-state.md) | Optional | This is a container for any-of cases. |
| `disputedTransactions` | [`DisputedTransaction[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/disputed-transaction.md) | Required | Disputed transactions.<br><br>**Constraints**: *Maximum Items*: `10` |
| `environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` |
| `evidenceClass` | [`EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `evidences` | [`DisputeEvidenceRow[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/dispute-evidence-row.md) | Required | Evidences.<br><br>**Constraints**: *Maximum Items*: `20` |
| `observedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `paypalDebugId` | [`DisputeDetailResponsePaypalDebugId \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/dispute-detail-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `providerSubmission` | [`ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `readback` | `string` | Required, Constant | Readback.<br><br>**Value**: `'GET_DETAIL'` |
| `reason` | [`Reason2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/reason-2.md) | Required | Reason. |
| `sellerResponseDueDate` | [`DisputeDetailResponseSellerResponseDueDate \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/dispute-detail-response-seller-response-due-date.md) | Optional | This is a container for any-of cases. |
| `source` | [`SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/source.md) | Required | Source. |
| `status` | [`Status3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/status-3.md) | Required | Status. |
| `updateTime` | [`DisputeDetailResponseUpdateTime \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/dispute-detail-response-update-time.md) | Optional | This is a container for any-of cases. |


# Example

```ts
import {
  DataSourceLabelEnum,
  DisputeDetailResponse,
  DisputeLifeCycleStageEnum,
  EvidenceClassEnum,
  ProviderSubmissionEnum,
  Reason2Enum,
  Source3Enum,
  SourceEnum,
  Status3Enum,
} from 'tradeglot-local-consolelib';

const disputeDetailResponse: DisputeDetailResponse = {
  createTime: 'create_time6',
  dataSourceLabel: DataSourceLabelEnum.Sandbox,
  disputeAmount: {
    currencyCode: 'currency_code6',
    value: 'value0',
  },
  disputeId: 'dispute_id2',
  disputeLifeCycleStage: DisputeLifeCycleStageEnum.UNKNOWN,
  disputedTransactions: [
    {
      sellerTransactionId: 'seller_transaction_id2',
      grossAmount: {
        currencyCode: 'currency_code0',
        value: 'value6',
      },
      sellerProtectionEligible: true,
      transactionStatus: 'String7',
    }
  ],
  environment: 'sandbox',
  evidenceClass: EvidenceClassEnum.SYNTHETICTESTRESPONSE,
  evidences: [
    {
      evidenceType: 'evidence_type2',
      source: Source3Enum.SUBMITTEDBYPARTNER,
      action: 'String1',
      date: 'String9',
    }
  ],
  observedAt: 'observed_at4',
  providerSubmission: ProviderSubmissionEnum.NOTPERFORMED,
  readback: 'GET_DETAIL',
  reason: Reason2Enum.MERCHANDISEORSERVICENOTRECEIVED,
  source: SourceEnum.PaypalSandbox,
  status: Status3Enum.CLOSED,
  disputeChannel: 'String5',
  disputeState: 'String9',
  paypalDebugId: 'String1',
  sellerResponseDueDate: 'String9',
  updateTime: 'String9',
};
```



