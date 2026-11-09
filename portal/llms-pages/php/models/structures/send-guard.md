# Send Guard

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlNlbmRHdWFyZA

(r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4).


# Class Name

`SendGuard`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `accountStatus` | [`string(AccountStatusEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/account-status.md) | Required | Account status. | getAccountStatus(): string | setAccountStatus(string accountStatus): void |
| `boundDisputeMasked` | string\|null | Optional | This is a container for any-of cases. | getBoundDisputeMasked(): ?string | setBoundDisputeMasked(?string boundDisputeMasked): void |
| `caseReason` | string\|null | Optional | This is a container for any-of cases. | getCaseReason(): ?string | setCaseReason(?string caseReason): void |
| `caseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` | getCaseRef(): string | setCaseRef(string caseRef): void |
| `disputeAmount` | [ProviderMoney](http://localhost:3000/llms-pages/php/models/structures/provider-money.md)\|null | Optional | This is a container for any-of cases. | getDisputeAmount(): ?ProviderMoney | setDisputeAmount(?ProviderMoney disputeAmount): void |
| `disputeMasked` | `string` | Required | Dispute masked.<br><br>**Constraints**: *Pattern*: `^(?:PP-[A-Z0-9-]{2}\u2026[A-Z0-9-]{2}\|\u2026)$` | getDisputeMasked(): string | setDisputeMasked(string disputeMasked): void |
| `disputeReason` | string\|null | Optional | This is a container for any-of cases. | getDisputeReason(): ?string | setDisputeReason(?string disputeReason): void |
| `disputeSellerMasked` | string\|null | Optional | This is a container for any-of cases. | getDisputeSellerMasked(): ?string | setDisputeSellerMasked(?string disputeSellerMasked): void |
| `sendRefusal` | string([SendRefusalEnum](http://localhost:3000/llms-pages/php/models/enumerations/send-refusal.md))\|null | Optional | This is a container for any-of cases. | getSendRefusal(): ?string | setSendRefusal(?string sendRefusal): void |
| `sendingAccountMasked` | string\|null | Optional | This is a container for any-of cases. | getSendingAccountMasked(): ?string | setSendingAccountMasked(?string sendingAccountMasked): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\SendGuardBuilder;
use TradeGlotLocalConsoleLib\Models\AccountStatusEnum;
use TradeGlotLocalConsoleLib\Models\Builders\ProviderMoneyBuilder;

$sendGuard = SendGuardBuilder::init(
    AccountStatusEnum::UNKNOWN,
    'case_ref2',
    'dispute_masked6'
)
    ->boundDisputeMasked(
        'String9'
    )
    ->caseReason(
        'String1'
    )
    ->disputeAmount(
        ProviderMoneyBuilder::init(
            'currency_code0',
            'value6'
        )->build()
    )
    ->disputeReason(
        'String7'
    )
    ->disputeSellerMasked(
        'String7'
    )
    ->build();
```



