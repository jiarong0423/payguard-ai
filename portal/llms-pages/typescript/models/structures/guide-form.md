# Guide Form

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkd1aWRlRm9ybQ

GuideForm.


# Interface Name

`GuideForm`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `kind` | [`Kind2Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/kind-2.md) | Required | Kind. |
| `options` | [`GuideOption[]`](http://localhost:3000/llms-pages/typescript/models/structures/guide-option.md) | Required | Options. |
| `placeholder` | [`GuideFormPlaceholder`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-form-placeholder.md) | Required | This is a container for any-of cases. |


# Example

```ts
import { GuideForm, Kind2Enum } from 'tradeglot-local-consolelib';

const guideForm: GuideForm = {
  kind: Kind2Enum.Choice,
  options: [
    {
      label: 'label2',
      value: 'value4',
    }
  ],
  placeholder: 'String3',
};
```



