# Event

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkV2ZW50


# Class Name

`Event`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `at` | `?string` | Optional | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` | getAt(): ?string | setAt(?string at): void |
| `channel` | [`?string(ChannelEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/channel.md) | Optional | Channel. | getChannel(): ?string | setChannel(?string channel): void |
| `direction` | [`?string(DirectionEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/direction.md) | Optional | Direction. | getDirection(): ?string | setDirection(?string direction): void |
| `kind` | [`?string(Kind1Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/kind-1.md) | Optional | Kind. | getKind(): ?string | setKind(?string kind): void |
| `messageDigest` | `?string` | Optional | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` | getMessageDigest(): ?string | setMessageDigest(?string messageDigest): void |
| `source` | [`?string(Source6Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/source-6.md) | Optional | Source. | getSource(): ?string | setSource(?string source): void |
| `topic` | [`?string(TopicEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/topic.md) | Optional | Topic. | getTopic(): ?string | setTopic(?string topic): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\EventBuilder;
use TradeGlotLocalConsoleLib\Models\ChannelEnum;
use TradeGlotLocalConsoleLib\Models\DirectionEnum;
use TradeGlotLocalConsoleLib\Models\Kind1Enum;

$event = EventBuilder::init()
    ->at('at6')
    ->channel(ChannelEnum::EMAIL)
    ->direction(DirectionEnum::INBOUND)
    ->kind(Kind1Enum::MESSAGE)
    ->messageDigest('message_digest6')
    ->build();
```



