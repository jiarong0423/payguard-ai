# Guide Item

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkd1aWRlSXRlbQ

GuideItem.


# Interface Name

`GuideItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chunk` | [`GuideItemChunk`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-item-chunk.md) | Required | This is a container for any-of cases. |
| `form` | [`GuideItemForm`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-item-form.md) | Required | This is a container for any-of cases. |
| `id` | `string` | Required | Id. |
| `label` | `string` | Required | Label. |
| `source` | [`Source8Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/source-8.md) | Required | Source. |
| `status` | [`Status9Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/status-9.md) | Required | Status. |


# Example

```ts
import {
  GuideItem,
  Kind2Enum,
  Source8Enum,
  Status9Enum,
} from 'tradeglot-local-consolelib';

const guideItem: GuideItem = {
  chunk: 'String7',
  form: {
    kind: Kind2Enum.Choice,
    options: [
      {
        label: 'label2',
        value: 'value4',
      }
    ],
    placeholder: 'String9',
  },
  id: 'id0',
  label: 'label0',
  source: Source8Enum.OFFICIAL,
  status: Status9Enum.UNCLEAR,
};
```



