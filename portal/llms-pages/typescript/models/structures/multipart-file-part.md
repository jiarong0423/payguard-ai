# Multipart File Part

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRk11bHRpcGFydEZpbGVQYXJ0

MultipartFilePart.


# Interface Name

`MultipartFilePart`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `byteLength` | `number` | Required | Byte length.<br><br>**Constraints**: `>= 0`, `<= 9999999` |
| `contentType` | [`ContentTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/content-type.md) | Required | Content type. |
| `filename` | `string` | Required | Filename.<br><br>**Constraints**: *Maximum Length*: `255` |
| `name` | `string` | Required | Name.<br><br>**Constraints**: *Pattern*: `^file[0-9]{1,3}$` |


# Example

```ts
import {
  ContentTypeEnum,
  MultipartFilePart,
} from 'tradeglot-local-consolelib';

const multipartFilePart: MultipartFilePart = {
  byteLength: 138,
  contentType: ContentTypeEnum.EnumImagejpeg,
  filename: 'filename0',
  name: 'name8',
};
```



