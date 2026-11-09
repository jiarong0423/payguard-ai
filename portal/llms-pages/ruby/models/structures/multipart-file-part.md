# Multipart File Part

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRk11bHRpcGFydEZpbGVQYXJ0

MultipartFilePart.


# Class Name

`MultipartFilePart`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `byte_length` | `Integer` | Required | Byte length.<br><br>**Constraints**: `>= 0`, `<= 9999999` |
| `content_type` | [`ContentTypeEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/content-type.md) | Required | Content type. |
| `filename` | `String` | Required | Filename.<br><br>**Constraints**: *Maximum Length*: `255` |
| `name` | `String` | Required | Name.<br><br>**Constraints**: *Pattern*: `^file[0-9]{1,3}$` |


# Example

```ruby
multipart_file_part = MultipartFilePart.new(
  18,
  ContentTypeEnum::ENUM_IMAGEJPEG,
  'filename4',
  'name2'
)
```



