# Aup Acknowledge Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVxdWVzdA

AupAcknowledgeRequest.


# Interface Name

`AupAcknowledgeRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `choice` | [`ChoiceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/choice.md) | Required | Choice. |
| `descriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `evaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |


# Example

```ts
import {
  AupAcknowledgeRequest,
  ChoiceEnum,
} from 'tradeglot-local-consolelib';

const aupAcknowledgeRequest: AupAcknowledgeRequest = {
  choice: ChoiceEnum.ACKNOWLEDGEANDCONTINUE,
  descriptionDigest: 'description_digest0',
  evaluationId: 'evaluation_id6',
};
```



