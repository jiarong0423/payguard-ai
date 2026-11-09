# Send Guard

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlNlbmRHdWFyZA

(r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4).


# Class Name

`SendGuard`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `account_status` | [`AccountStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/account-status.md) | Required | Account status. |
| `bound_dispute_masked` | str \| None | Optional | This is a container for any-of cases. |
| `case_reason` | str \| None | Optional | This is a container for any-of cases. |
| `case_ref` | `str` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `dispute_amount` | [ProviderMoney](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/provider-money.md) \| None | Optional | This is a container for any-of cases. |
| `dispute_masked` | `str` | Required | Dispute masked.<br><br>**Constraints**: *Pattern*: `^(?:PP-[A-Z0-9-]{2}\u2026[A-Z0-9-]{2}\|\u2026)$` |
| `dispute_reason` | str \| None | Optional | This is a container for any-of cases. |
| `dispute_seller_masked` | str \| None | Optional | This is a container for any-of cases. |
| `send_refusal` | [SendRefusal](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/send-refusal.md) \| None | Optional | This is a container for any-of cases. |
| `sending_account_masked` | str \| None | Optional | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.account_status_enum import AccountStatusEnum
from tradeglotlocalconsole.models.provider_money import ProviderMoney
from tradeglotlocalconsole.models.send_guard import SendGuard

send_guard = SendGuard(
    account_status=AccountStatusEnum.MATCH,
    case_ref='case_ref6',
    dispute_masked='dispute_masked0',
    bound_dispute_masked='String3',
    case_reason='String7',
    dispute_amount=ProviderMoney(
        currency_code='currency_code0',
        value='value6'
    ),
    dispute_reason='String9',
    dispute_seller_masked='String1'
)
```



