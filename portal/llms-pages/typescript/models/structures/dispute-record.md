# Dispute Record

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkRpc3B1dGVSZWNvcmQ

DisputeRecord.


# Interface Name

`DisputeRecord`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `createTime` | `string` | Required | Create time.<br><br>**Constraints**: *Pattern*: `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$` |
| `disputeAmount` | [`ProviderMoney`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/provider-money.md) | Required | ProviderMoney. |
| `disputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `disputeLifeCycleStage` | [`DisputeLifeCycleStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `disputeState` | [`DisputeRecordDisputeState \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/dispute-record-dispute-state.md) | Optional | This is a container for any-of cases. |
| `reason` | [`Reason2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/reason-2.md) | Required | Reason. |
| `sellerResponseDueDate` | [`DisputeRecordSellerResponseDueDate \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/dispute-record-seller-response-due-date.md) | Optional | This is a container for any-of cases. |
| `status` | [`Status3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/status-3.md) | Required | Status. |
| `updateTime` | [`DisputeRecordUpdateTime \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/dispute-record-update-time.md) | Optional | This is a container for any-of cases. |


# Example

```ts
import {
  DisputeLifeCycleStageEnum,
  DisputeRecord,
  Reason2Enum,
  Status3Enum,
} from 'tradeglot-local-consolelib';

const disputeRecord: DisputeRecord = {
  createTime: 'create_time0',
  disputeAmount: {
    currencyCode: 'currency_code6',
    value: 'value0',
  },
  disputeId: 'dispute_id6',
  disputeLifeCycleStage: DisputeLifeCycleStageEnum.ARBITRATION,
  reason: Reason2Enum.MERCHANDISEORSERVICENOTRECEIVED,
  status: Status3Enum.OPEN,
  disputeState: 'String7',
  sellerResponseDueDate: 'String3',
  updateTime: 'String7',
};
```



