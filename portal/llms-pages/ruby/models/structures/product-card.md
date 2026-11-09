# Product Card

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlByb2R1Y3RDYXJk

A Channel3 catalogue product reduced to what identifies the item; no prices, offers or buy links.


# Class Name

`ProductCard`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `brand` | String | Required | This is a container for any-of cases. |
| `category` | String | Required | This is a container for any-of cases. |
| `image_url` | String | Required | This is a container for any-of cases. |
| `key_features` | `Array[String]` | Required | Key features.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `100`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `materials` | `Array[String]` | Required | Materials.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `40`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `product_id` | `String` | Required | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `title` | `String` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```ruby
product_card = ProductCard.new(
  'String3',
  'String7',
  'String5',
  [
    'key_features4'
  ],
  [
    'materials9',
    'materials0',
    'materials1'
  ],
  'product_id4',
  'title4'
)
```



