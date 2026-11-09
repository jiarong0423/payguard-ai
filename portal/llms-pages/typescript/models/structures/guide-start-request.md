# Guide Start Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkd1aWRlU3RhcnRSZXF1ZXN0

GuideStartRequest.


# Interface Name

`GuideStartRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `goodsType` | [`GuideStartRequestGoodsType \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-start-request-goods-type.md) | Optional | This is a container for any-of cases. |
| `scenario` | [`Scenario2Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/scenario-2.md) | Required | Scenario. |


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



