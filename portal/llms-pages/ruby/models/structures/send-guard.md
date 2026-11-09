# Send Guard

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlNlbmRHdWFyZA

(r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4).


# Class Name

`SendGuard`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `account_status` | [`AccountStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/account-status.md) | Required | Account status. |
| `bound_dispute_masked` | String \| nil | Optional | This is a container for any-of cases. |
| `case_reason` | String \| nil | Optional | This is a container for any-of cases. |
| `case_ref` | `String` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `dispute_amount` | [ProviderMoney](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/provider-money.md) \| nil | Optional | This is a container for any-of cases. |
| `dispute_masked` | `String` | Required | Dispute masked.<br><br>**Constraints**: *Pattern*: `^(?:PP-[A-Z0-9-]{2}\u2026[A-Z0-9-]{2}\|\u2026)$` |
| `dispute_reason` | String \| nil | Optional | This is a container for any-of cases. |
| `dispute_seller_masked` | String \| nil | Optional | This is a container for any-of cases. |
| `send_refusal` | [SendRefusal](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/send-refusal.md) \| nil | Optional | This is a container for any-of cases. |
| `sending_account_masked` | String \| nil | Optional | This is a container for any-of cases. |


# Example

```ruby
send_guard = SendGuard.new(
  AccountStatusEnum::MATCH,
  'case_ref6',
  'dispute_masked0',
  'String3',
  'String7',
  ProviderMoney.new(
    'currency_code0',
    'value6'
  ),
  'String9',
  'String1'
)
```



