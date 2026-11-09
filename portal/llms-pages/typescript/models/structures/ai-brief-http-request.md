# Ai Brief Http Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkFpQnJpZWZIdHRwUmVxdWVzdA

What the console may send: the stage and, for disputes, which case. Session facts are never caller input.


# Interface Name

`AiBriefHttpRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseRef` | [`AiBriefHttpRequestCaseRef \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/ai-brief-http-request-case-ref.md) | Optional | This is a container for any-of cases. |
| `stage` | [`StageEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/stage.md) | Required | Stage. |


# Example

```ts
import { AiBriefHttpRequest, StageEnum } from 'tradeglot-local-consolelib';

const aiBriefHttpRequest: AiBriefHttpRequest = {
  stage: StageEnum.VelocityGuard,
  caseRef: 'String9',
};
```



