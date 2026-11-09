# Scenario Citation

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlNjZW5hcmlvQ2l0YXRpb24

ScenarioCitation.


# Class Name

`ScenarioCitation`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ChunkId` | `string` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `Jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `Locator` | `string` | Required | Locator.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1000` |
| `MaterialType` | [`MaterialTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/material-type.md) | Required | Material type. |
| `SourceId` | `string` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `TextSha256` | `string` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `Title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `512` |
| `Url` | `string` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2048` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

ScenarioCitation scenarioCitation = new ScenarioCitation
{
    ChunkId = "chunk_id8",
    Jurisdiction = "US",
    Locator = "locator8",
    MaterialType = MaterialTypeEnum.OfficialApiReference,
    SourceId = "source_id0",
    TextSha256 = "text_sha2566",
    Title = "title2",
    Url = "url0",
};
```



