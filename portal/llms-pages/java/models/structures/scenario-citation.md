# Scenario Citation

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlNjZW5hcmlvQ2l0YXRpb24

ScenarioCitation.


# Class Name

`ScenarioCitation`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `ChunkId` | `String` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` | String getChunkId() | setChunkId(String chunkId) |
| `Jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` | String getJurisdiction() | setJurisdiction(String jurisdiction) |
| `Locator` | `String` | Required | Locator.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1000` | String getLocator() | setLocator(String locator) |
| `MaterialType` | [`MaterialTypeEnum`](http://localhost:3000/llms-pages/java/models/enumerations/material-type.md) | Required | Material type. | MaterialTypeEnum getMaterialType() | setMaterialType(MaterialTypeEnum materialType) |
| `SourceId` | `String` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` | String getSourceId() | setSourceId(String sourceId) |
| `TextSha256` | `String` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getTextSha256() | setTextSha256(String textSha256) |
| `Title` | `String` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `512` | String getTitle() | setTitle(String title) |
| `Url` | `String` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2048` | String getUrl() | setUrl(String url) |


# Example

```java
import m18000.m0.m0.m127.models.MaterialTypeEnum;
import m18000.m0.m0.m127.models.ScenarioCitation;

ScenarioCitation scenarioCitation = new ScenarioCitation.Builder(
    "chunk_id8",
    "US",
    "locator8",
    MaterialTypeEnum.OFFICIAL_API_REFERENCE,
    "source_id0",
    "text_sha2566",
    "title2",
    "url0"
)
.build();
```



