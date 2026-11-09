# Guide State Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZQ

GuideStateResponse.


# Class Name

`GuideStateResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `String` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` |
| `analysis` | [GuideAnalysis](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-analysis.md) | Required | This is a container for any-of cases. |
| `asked` | `Array[String]` | Required | Asked.<br><br>**Constraints**: *Maximum Items*: `3` |
| `auto_confirmed` | `Array[String]` | Required | Auto confirmed. |
| `chooser_mode` | [`ChooserModeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/chooser-mode.md) | Required | Chooser mode. |
| `deferred` | `Array[String]` | Required | Deferred. |
| `flow_name` | String | Required | This is a container for any-of cases. |
| `form_result` | [GuideFormResult](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-form-result.md) | Required | This is a container for any-of cases. |
| `form_results` | [`Array[GuideFieldResult]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-field-result.md) | Required | Form results. |
| `gap` | [`GuideGap`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-gap.md) | Required | GuideGap. |
| `goods_type` | [GoodsType](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/goods-type.md) | Required | This is a container for any-of cases. |
| `items` | [`Array[GuideItem]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-item.md) | Required | Items. |
| `model_requested` | `TrueClass \| FalseClass` | Required | Model requested. |
| `model_text_shown` | `String` | Required, Constant | Model text shown.<br><br>**Value**: `'False'` |
| `prefill` | `Hash[String, String]` | Required | Prefill. |
| `reply` | [GuideReply](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-reply.md) | Required | This is a container for any-of cases. |
| `review` | [`Array[GuideReviewRow]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-review-row.md) | Required | Review. |
| `rounds_used` | `Integer` | Required | Rounds used. |
| `scenario` | [Scenario1](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/scenario-1.md) | Required | This is a container for any-of cases. |
| `schema_version` | `Integer` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `stage` | [Stage3](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/stage-3.md) | Required | This is a container for any-of cases. |
| `started` | `TrueClass \| FalseClass` | Required | Started. |
| `subtraction` | [GuideSubtraction](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-subtraction.md) | Required | This is a container for any-of cases. |
| `turns_limit` | `Integer` | Required | Turns limit. |
| `turns_used` | `Integer` | Required | Turns used. |
| `values_stored` | `String` | Required, Constant | Values stored.<br><br>**Value**: `'False'` |


# Example

```ruby
guide_state_response = GuideStateResponse.new(
  'True',
  GuideAnalysis.new(
    Reason5Enum::INVALID_REPLY,
    Status8Enum::REPLACED,
    186
  ),
  [
    'asked4',
    'asked5',
    'asked6'
  ],
  [
    'auto_confirmed0',
    'auto_confirmed1',
    'auto_confirmed2'
  ],
  ChooserModeEnum::KEYWORD,
  [
    'deferred7',
    'deferred8'
  ],
  'String3',
  GuideFormResult.new(
    'item2',
    false
  ),
  [
    GuideFieldResult.new(
      false,
      'item6',
      false
    )
  ],
  GuideGap.new(
    [
      'conflicting9',
      'conflicting8'
    ],
    [
      'missing2',
      'missing3',
      'missing4'
    ],
    [
      'partial4',
      'partial3',
      'partial2'
    ],
    [
      'present7',
      'present8'
    ]
  ),
  GoodsTypeEnum::PHYSICAL,
  [
    GuideItem.new(
      'String9',
      GuideForm.new(
        Kind2Enum::CHOICE,
        [
          GuideOption.new(
            'label2',
            'value4'
          )
        ],
        'String9'
      ),
      'id8',
      'label8',
      Source8Enum::OFFICIAL,
      Status9Enum::MISSING
    )
  ],
  false,
  'False',
  {
    'key0': 'prefill9'
  },
  GuideReply.new(
    ChooserEnum::FORM,
    [
      GuideDropped.new(
        'item2',
        Reason6Enum::OTHER_PARTY
      )
    ],
    FallbackReasonEnum::LATE,
    false,
    TemplateEnum::REVIEW,
    'text0'
  ),
  [
    GuideReviewRow.new(
      'item4',
      Source9Enum::WORDS,
      'value4'
    )
  ],
  100,
  Scenario1Enum::PREFLIGHT,
  1,
  Stage3Enum::FUNNEL,
  false,
  GuideSubtraction.new(
    64,
    190,
    178,
    'text0'
  ),
  88,
  242,
  'False'
)
```



