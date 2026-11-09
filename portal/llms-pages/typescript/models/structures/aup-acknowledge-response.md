# Aup Acknowledge Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVzcG9uc2U

AupAcknowledgeResponse.


# Interface Name

`AupAcknowledgeResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `acknowledgementToken` | [`AupAcknowledgeResponseAcknowledgementToken`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/aup-acknowledge-response-acknowledgement-token.md) | Required | This is a container for any-of cases. |
| `choice` | [`ChoiceEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/choice.md) | Required | Choice. |
| `complianceDecision` | `string` | Required, Constant | Compliance decision.<br><br>**Value**: `'NOT_MADE'` |
| `descriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `evaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `expiresAt` | [`AupAcknowledgeResponseExpiresAt`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/aup-acknowledge-response-expires-at.md) | Required | This is a container for any-of cases. |
| `externalActionAuthorized` | `string` | Required, Constant | External action authorized.<br><br>**Value**: `'False'` |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |
| `warningCopyVersion` | `string` | Required, Constant | Warning copy version.<br><br>**Value**: `'aup-warning-v1'` |


# Example

```ts
import {
  AupAcknowledgeResponse,
  ChoiceEnum,
} from 'tradeglot-local-consolelib';

const aupAcknowledgeResponse: AupAcknowledgeResponse = {
  acknowledgementToken: 'String9',
  choice: ChoiceEnum.ACKNOWLEDGEANDCONTINUE,
  complianceDecision: 'NOT_MADE',
  descriptionDigest: 'description_digest6',
  evaluationId: 'evaluation_id2',
  expiresAt: 'String9',
  externalActionAuthorized: 'False',
  source: 'synthetic',
  warningCopyVersion: 'aup-warning-v1',
};
```



