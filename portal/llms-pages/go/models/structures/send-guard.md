# Send Guard

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlNlbmRHdWFyZA

(r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4).


# Class Name

`SendGuard`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AccountStatus` | [`models.AccountStatusEnum`](http://localhost:3000/llms-pages/go/models/enumerations/account-status.md) | Required | Account status. |
| `BoundDisputeMasked` | [`*models.SendGuardBoundDisputeMasked`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/send-guard-bound-dispute-masked.md) | Optional | This is a container for any-of cases. |
| `CaseReason` | [`*models.SendGuardCaseReason`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/send-guard-case-reason.md) | Optional | This is a container for any-of cases. |
| `CaseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `DisputeAmount` | [`*models.SendGuardDisputeAmount`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/send-guard-dispute-amount.md) | Optional | This is a container for any-of cases. |
| `DisputeMasked` | `string` | Required | Dispute masked.<br><br>**Constraints**: *Pattern*: `^(?:PP-[A-Z0-9-]{2}\u2026[A-Z0-9-]{2}\|\u2026)$` |
| `DisputeReason` | [`*models.SendGuardDisputeReason`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/send-guard-dispute-reason.md) | Optional | This is a container for any-of cases. |
| `DisputeSellerMasked` | [`*models.SendGuardDisputeSellerMasked`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/send-guard-dispute-seller-masked.md) | Optional | This is a container for any-of cases. |
| `SendRefusal` | [`*models.SendGuardSendRefusal`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/send-guard-send-refusal.md) | Optional | This is a container for any-of cases. |
| `SendingAccountMasked` | [`*models.SendGuardSendingAccountMasked`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/send-guard-sending-account-masked.md) | Optional | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    sendGuard := models.SendGuard{
        AccountStatus:        models.AccountStatusEnum_UNKNOWN,
        BoundDisputeMasked:   models.ToPointer(models.SendGuardBoundDisputeMaskedContainer.FromString("String9")),
        CaseReason:           models.ToPointer(models.SendGuardCaseReasonContainer.FromString("String1")),
        CaseRef:              "case_ref2",
        DisputeAmount:        models.ToPointer(models.SendGuardDisputeAmountContainer.FromProviderMoney(models.ProviderMoney{
            CurrencyCode:         "currency_code0",
            Value:                "value6",
        })),
        DisputeMasked:        "dispute_masked6",
        DisputeReason:        models.ToPointer(models.SendGuardDisputeReasonContainer.FromString("String7")),
        DisputeSellerMasked:  models.ToPointer(models.SendGuardDisputeSellerMaskedContainer.FromString("String7")),
    }

}
```



