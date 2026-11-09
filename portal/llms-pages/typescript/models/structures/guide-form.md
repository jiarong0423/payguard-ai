# Guide Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkd1aWRlRm9ybQ

GuideForm.


# Interface Name

`GuideForm`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `kind` | [`Kind2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/kind-2.md) | Required | Kind. |
| `options` | [`GuideOption[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/guide-option.md) | Required | Options. |
| `placeholder` | [`GuideFormPlaceholder`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/guide-form-placeholder.md) | Required | This is a container for any-of cases. |


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



