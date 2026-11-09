# Reference Digests

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlJlZmVyZW5jZURpZ2VzdHM

ReferenceDigests.


# Interface Name

`ReferenceDigests`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chunksSha256` | `string` | Required | Chunks sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `sourcesSha256` | `string` | Required | Sources sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |


# Example

```ts
import { ReferenceDigests } from 'tradeglot-local-consolelib';

const referenceDigests: ReferenceDigests = {
  chunksSha256: 'chunks_sha2562',
  sourcesSha256: 'sources_sha2564',
};
```



