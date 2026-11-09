# Send Guard

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlNlbmRHdWFyZA

(r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4).


# Class Name

`SendGuard`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AccountStatus` | [`AccountStatusEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/account-status.md) | Required | Account status. |
| `BoundDisputeMasked` | [`SendGuardBoundDisputeMasked`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/send-guard-bound-dispute-masked.md) | Optional | This is a container for any-of cases. |
| `CaseReason` | [`SendGuardCaseReason`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/send-guard-case-reason.md) | Optional | This is a container for any-of cases. |
| `CaseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `DisputeAmount` | [`SendGuardDisputeAmount`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/send-guard-dispute-amount.md) | Optional | This is a container for any-of cases. |
| `DisputeMasked` | `string` | Required | Dispute masked.<br><br>**Constraints**: *Pattern*: `^(?:PP-[A-Z0-9-]{2}\u2026[A-Z0-9-]{2}\|\u2026)$` |
| `DisputeReason` | [`SendGuardDisputeReason`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/send-guard-dispute-reason.md) | Optional | This is a container for any-of cases. |
| `DisputeSellerMasked` | [`SendGuardDisputeSellerMasked`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/send-guard-dispute-seller-masked.md) | Optional | This is a container for any-of cases. |
| `SendRefusal` | [`SendGuardSendRefusal`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/send-guard-send-refusal.md) | Optional | This is a container for any-of cases. |
| `SendingAccountMasked` | [`SendGuardSendingAccountMasked`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/send-guard-sending-account-masked.md) | Optional | This is a container for any-of cases. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

SendGuard sendGuard = new SendGuard
{
    AccountStatus = AccountStatusEnum.UNKNOWN,
    CaseRef = "case_ref2",
    DisputeMasked = "dispute_masked6",
    BoundDisputeMasked = SendGuardBoundDisputeMasked.FromString("String9"),
    CaseReason = SendGuardCaseReason.FromString("String1"),
    DisputeAmount = SendGuardDisputeAmount.FromProviderMoney(
        new ProviderMoney
        {
            CurrencyCode = "currency_code0",
            MValue = "value6",
        }
    ),
    DisputeReason = SendGuardDisputeReason.FromString("String7"),
    DisputeSellerMasked = SendGuardDisputeSellerMasked.FromString("String7"),
};
```



