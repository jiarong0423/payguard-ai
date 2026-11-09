# Message Time Event

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRk1lc3NhZ2VUaW1lRXZlbnQ

MessageTimeEvent.


# Class Name

`MessageTimeEvent`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `at` | `string` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` | getAt(): string | setAt(string at): void |
| `channel` | [`string(ChannelEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/channel.md) | Required | Channel. | getChannel(): string | setChannel(string channel): void |
| `direction` | [`string(DirectionEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/direction.md) | Required | Direction. | getDirection(): string | setDirection(string direction): void |
| `kind` | `string` | Required, Constant | Kind.<br><br>**Value**: `'MESSAGE'` | getKind(): string | setKind(string kind): void |
| `messageDigest` | `string` | Required | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` | getMessageDigest(): string | setMessageDigest(string messageDigest): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'SELLER_PROVIDED_UNVERIFIED'` | getSource(): string | setSource(string source): void |
| `topic` | [`string(TopicEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/topic.md) | Required | Topic. | getTopic(): string | setTopic(string topic): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\MessageTimeEventBuilder;
use TradeGlotLocalConsoleLib\Models\ChannelEnum;
use TradeGlotLocalConsoleLib\Models\DirectionEnum;
use TradeGlotLocalConsoleLib\Models\TopicEnum;

$messageTimeEvent = MessageTimeEventBuilder::init(
    'at6',
    ChannelEnum::EMAIL,
    DirectionEnum::INBOUND,
    'message_digest4',
    TopicEnum::PAYMENT_NOTICE
)->build();
```



