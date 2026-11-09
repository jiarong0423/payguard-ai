# Transaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlRyYW5zYWN0aW9u

Transaction.


# Class Name

`Transaction`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `amount` | `string` | Required | Amount. | getAmount(): string | setAmount(string amount): void |
| `currency` | `string` | Required | Currency. | getCurrency(): string | setCurrency(string currency): void |
| `occurredAt` | `string` | Required | Occurred at. | getOccurredAt(): string | setOccurredAt(string occurredAt): void |
| `orderId` | `string` | Required | Order id. | getOrderId(): string | setOrderId(string orderId): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\TransactionBuilder;

$transaction = TransactionBuilder::init(
    'amount0',
    'currency8',
    'occurred_at2',
    'order_id2'
)->build();
```



