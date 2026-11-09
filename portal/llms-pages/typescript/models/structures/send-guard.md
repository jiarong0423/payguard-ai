# Send Guard

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlNlbmRHdWFyZA

(r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4).


# Interface Name

`SendGuard`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `accountStatus` | [`AccountStatusEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/account-status.md) | Required | Account status. |
| `boundDisputeMasked` | [`SendGuardBoundDisputeMasked \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/send-guard-bound-dispute-masked.md) | Optional | This is a container for any-of cases. |
| `caseReason` | [`SendGuardCaseReason \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/send-guard-case-reason.md) | Optional | This is a container for any-of cases. |
| `caseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `disputeAmount` | [`SendGuardDisputeAmount \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/send-guard-dispute-amount.md) | Optional | This is a container for any-of cases. |
| `disputeMasked` | `string` | Required | Dispute masked.<br><br>**Constraints**: *Pattern*: `^(?:PP-[A-Z0-9-]{2}\u2026[A-Z0-9-]{2}\|\u2026)$` |
| `disputeReason` | [`SendGuardDisputeReason \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/send-guard-dispute-reason.md) | Optional | This is a container for any-of cases. |
| `disputeSellerMasked` | [`SendGuardDisputeSellerMasked \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/send-guard-dispute-seller-masked.md) | Optional | This is a container for any-of cases. |
| `sendRefusal` | [`SendGuardSendRefusal \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/send-guard-send-refusal.md) | Optional | This is a container for any-of cases. |
| `sendingAccountMasked` | [`SendGuardSendingAccountMasked \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/send-guard-sending-account-masked.md) | Optional | This is a container for any-of cases. |


# Example

```ts
import { AccountStatusEnum, SendGuard } from 'tradeglot-local-consolelib';

const sendGuard: SendGuard = {
  accountStatus: AccountStatusEnum.UNKNOWN,
  caseRef: 'case_ref2',
  disputeMasked: 'dispute_masked6',
  boundDisputeMasked: 'String9',
  caseReason: 'String1',
  disputeAmount: {
    currencyCode: 'currency_code0',
    value: 'value6',
  },
  disputeReason: 'String7',
  disputeSellerMasked: 'String7',
};
```



