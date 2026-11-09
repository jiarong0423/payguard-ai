# Scenario Citation

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlNjZW5hcmlvQ2l0YXRpb24

ScenarioCitation.


# Class Name

`ScenarioCitation`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chunk_id` | `String` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `locator` | `String` | Required | Locator.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1000` |
| `material_type` | [`MaterialTypeEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/material-type.md) | Required | Material type. |
| `source_id` | `String` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `text_sha_256` | `String` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `title` | `String` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `512` |
| `url` | `String` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2048` |


# Example

```ruby
scenario_citation = ScenarioCitation.new(
  'chunk_id0',
  'US',
  'locator0',
  MaterialTypeEnum::OFFICIAL_API_REFERENCE,
  'source_id2',
  'text_sha2564',
  'title4',
  'url2'
)
```



