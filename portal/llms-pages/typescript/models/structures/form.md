# Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkZvcm0

Form.


# Interface Name

`Form`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `kind` | [`Kind2Enum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/kind-2.md) | Optional | Kind. |
| `options` | [`GuideOption[] \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/guide-option.md) | Optional | Options. |
| `placeholder` | [`FormPlaceholder \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/form-placeholder.md) | Optional | This is a container for any-of cases. |


# Example

```ts
import { Form, Kind2Enum } from 'tradeglot-local-consolelib';

const form: Form = {
  kind: Kind2Enum.Text,
  options: [
    {
      label: 'label2',
      value: 'value4',
    },
    {
      label: 'label2',
      value: 'value4',
    },
    {
      label: 'label2',
      value: 'value4',
    }
  ],
  placeholder: 'String9',
};
```



