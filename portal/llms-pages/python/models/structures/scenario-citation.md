# Scenario Citation

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlNjZW5hcmlvQ2l0YXRpb24

ScenarioCitation.


# Class Name

`ScenarioCitation`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chunk_id` | `str` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `jurisdiction` | `str` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `locator` | `str` | Required | Locator.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1000` |
| `material_type` | [`MaterialTypeEnum`](http://localhost:3000/llms-pages/python/models/enumerations/material-type.md) | Required | Material type. |
| `source_id` | `str` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `text_sha_256` | `str` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `title` | `str` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `512` |
| `url` | `str` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2048` |


# Example

```python
from tradeglotlocalconsole.models.material_type_enum import MaterialTypeEnum
from tradeglotlocalconsole.models.scenario_citation import ScenarioCitation

scenario_citation = ScenarioCitation(
    chunk_id='chunk_id0',
    locator='locator0',
    material_type=MaterialTypeEnum.OFFICIAL_API_REFERENCE,
    source_id='source_id2',
    text_sha_256='text_sha2564',
    title='title4',
    url='url2'
)
```



