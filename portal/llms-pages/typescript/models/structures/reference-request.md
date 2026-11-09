# Reference Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlJlZmVyZW5jZVJlcXVlc3Q

ReferenceRequest.


# Interface Name

`ReferenceRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `asOf` | [`ReferenceRequestAsOf \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/reference-request-as-of.md) | Optional | This is a container for any-of cases. |
| `caseStage` | [`CaseStage2Enum \| undefined`](http://localhost:3000/llms-pages/typescript/models/enumerations/case-stage-2.md) | Optional | Case stage.<br><br>**Default**: `CaseStage2Enum.Any` |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `limit` | `number \| undefined` | Optional | Limit.<br><br>**Default**: `3`<br><br>**Constraints**: `>= 1`, `<= 10` |
| `materialTypes` | [`ReferenceRequestMaterialTypes \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/reference-request-material-types.md) | Optional | This is a container for any-of cases. |
| `maxSourceAgeDays` | [`ReferenceRequestMaxSourceAgeDays \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/reference-request-max-source-age-days.md) | Optional | This is a container for any-of cases. |
| `query` | `string` | Required | Query.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `512` |
| `requireKnownSourceDate` | `boolean \| undefined` | Optional | Require known source date.<br><br>**Default**: `false` |
| `theme` | [`ThemeEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/theme.md) | Required | Theme. |


# Example

```ts
import {
  CaseStage2Enum,
  MaterialType4Enum,
  ReferenceRequest,
  ThemeEnum,
} from 'tradeglot-local-consolelib';

const referenceRequest: ReferenceRequest = {
  jurisdiction: 'US',
  query: 'query4',
  theme: ThemeEnum.DisputeMediation,
  asOf: 'String7',
  caseStage: CaseStage2Enum.Any,
  limit: 3,
  materialTypes: [
    MaterialType4Enum.PublicCourtOrderCopy
  ],
  maxSourceAgeDays: 110,
  requireKnownSourceDate: false,
};
```



