# Card

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkNhcmQ

Card.


# Class Name

`Card`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `brand` | String \| nil | Optional | This is a container for any-of cases. |
| `category` | String \| nil | Optional | This is a container for any-of cases. |
| `image_url` | String \| nil | Optional | This is a container for any-of cases. |
| `key_features` | `Array[String]` | Optional | Key features.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `100`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `materials` | `Array[String]` | Optional | Materials.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `40`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `product_id` | `String` | Optional | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `title` | `String` | Optional | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```ruby
card = Card.new(
  'String1',
  'String5',
  'String3',
  [
    'key_features2'
  ],
  [
    'materials7',
    'materials8',
    'materials9'
  ]
)
```



