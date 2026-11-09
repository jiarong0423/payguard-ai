# Send Guard

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlNlbmRHdWFyZA

(r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4).


# Class Name

`SendGuard`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AccountStatus` | [`AccountStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/account-status.md) | Required | Account status. | AccountStatusEnum getAccountStatus() | setAccountStatus(AccountStatusEnum accountStatus) |
| `BoundDisputeMasked` | [`SendGuardBoundDisputeMasked`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/send-guard-bound-dispute-masked.md) | Optional | This is a container for any-of cases. | SendGuardBoundDisputeMasked getBoundDisputeMasked() | setBoundDisputeMasked(SendGuardBoundDisputeMasked boundDisputeMasked) |
| `CaseReason` | [`SendGuardCaseReason`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/send-guard-case-reason.md) | Optional | This is a container for any-of cases. | SendGuardCaseReason getCaseReason() | setCaseReason(SendGuardCaseReason caseReason) |
| `CaseRef` | `String` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` | String getCaseRef() | setCaseRef(String caseRef) |
| `DisputeAmount` | [`SendGuardDisputeAmount`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/send-guard-dispute-amount.md) | Optional | This is a container for any-of cases. | SendGuardDisputeAmount getDisputeAmount() | setDisputeAmount(SendGuardDisputeAmount disputeAmount) |
| `DisputeMasked` | `String` | Required | Dispute masked.<br><br>**Constraints**: *Pattern*: `^(?:PP-[A-Z0-9-]{2}\u2026[A-Z0-9-]{2}\|\u2026)$` | String getDisputeMasked() | setDisputeMasked(String disputeMasked) |
| `DisputeReason` | [`SendGuardDisputeReason`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/send-guard-dispute-reason.md) | Optional | This is a container for any-of cases. | SendGuardDisputeReason getDisputeReason() | setDisputeReason(SendGuardDisputeReason disputeReason) |
| `DisputeSellerMasked` | [`SendGuardDisputeSellerMasked`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/send-guard-dispute-seller-masked.md) | Optional | This is a container for any-of cases. | SendGuardDisputeSellerMasked getDisputeSellerMasked() | setDisputeSellerMasked(SendGuardDisputeSellerMasked disputeSellerMasked) |
| `SendRefusal` | [`SendGuardSendRefusal`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/send-guard-send-refusal.md) | Optional | This is a container for any-of cases. | SendGuardSendRefusal getSendRefusal() | setSendRefusal(SendGuardSendRefusal sendRefusal) |
| `SendingAccountMasked` | [`SendGuardSendingAccountMasked`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/send-guard-sending-account-masked.md) | Optional | This is a container for any-of cases. | SendGuardSendingAccountMasked getSendingAccountMasked() | setSendingAccountMasked(SendGuardSendingAccountMasked sendingAccountMasked) |


# Example

```java
import m18000.m0.m0.m127.models.AccountStatusEnum;
import m18000.m0.m0.m127.models.ProviderMoney;
import m18000.m0.m0.m127.models.SendGuard;
import m18000.m0.m0.m127.models.containers.SendGuardBoundDisputeMasked;
import m18000.m0.m0.m127.models.containers.SendGuardCaseReason;
import m18000.m0.m0.m127.models.containers.SendGuardDisputeAmount;
import m18000.m0.m0.m127.models.containers.SendGuardDisputeReason;
import m18000.m0.m0.m127.models.containers.SendGuardDisputeSellerMasked;

SendGuard sendGuard = new SendGuard.Builder(
    AccountStatusEnum.UNKNOWN,
    "case_ref2",
    "dispute_masked6"
)
.boundDisputeMasked(SendGuardBoundDisputeMasked.fromString(
        "String9"
    ))
.caseReason(SendGuardCaseReason.fromString(
        "String1"
    ))
.disputeAmount(SendGuardDisputeAmount.fromProviderMoney(
        new ProviderMoney.Builder(
            "currency_code0",
            "value6"
        )
        .build()
    ))
.disputeReason(SendGuardDisputeReason.fromString(
        "String7"
    ))
.disputeSellerMasked(SendGuardDisputeSellerMasked.fromString(
        "String7"
    ))
.build();
```



