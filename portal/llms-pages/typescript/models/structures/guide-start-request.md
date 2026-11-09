# Guide Start Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkd1aWRlU3RhcnRSZXF1ZXN0

GuideStartRequest.


# Interface Name

`GuideStartRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `goodsType` | [`GuideStartRequestGoodsType \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/guide-start-request-goods-type.md) | Optional | This is a container for any-of cases. |
| `scenario` | [`Scenario2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/scenario-2.md) | Required | Scenario. |


# Example

```ts
import {
  GoodsTypeEnum,
  GuideStartRequest,
  Scenario2Enum,
} from 'tradeglot-local-consolelib';

const guideStartRequest: GuideStartRequest = {
  scenario: Scenario2Enum.Velocity,
  goodsType: GoodsTypeEnum.Physical,
};
```



