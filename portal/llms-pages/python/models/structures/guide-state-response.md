# Guide State Response

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZQ

GuideStateResponse.


# Class Name

`GuideStateResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `str` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `analysis` | [GuideAnalysis](http://localhost:3000/llms-pages/python/models/structures/guide-analysis.md) | Required | This is a container for any-of cases. |
| `asked` | `List[str]` | Required | Asked.<br><br>**Constraints**: *Maximum Items*: `3` |
| `auto_confirmed` | `List[str]` | Required | Auto confirmed. |
| `chooser_mode` | [`ChooserModeEnum`](http://localhost:3000/llms-pages/python/models/enumerations/chooser-mode.md) | Required | Chooser mode. |
| `deferred` | `List[str]` | Required | Deferred. |
| `flow_name` | str | Required | This is a container for any-of cases. |
| `form_result` | [GuideFormResult](http://localhost:3000/llms-pages/python/models/structures/guide-form-result.md) | Required | This is a container for any-of cases. |
| `form_results` | [`List[GuideFieldResult]`](http://localhost:3000/llms-pages/python/models/structures/guide-field-result.md) | Required | Form results. |
| `gap` | [`GuideGap`](http://localhost:3000/llms-pages/python/models/structures/guide-gap.md) | Required | GuideGap. |
| `goods_type` | [GoodsType](http://localhost:3000/llms-pages/python/models/enumerations/goods-type.md) | Required | This is a container for any-of cases. |
| `items` | [`List[GuideItem]`](http://localhost:3000/llms-pages/python/models/structures/guide-item.md) | Required | Items. |
| `model_requested` | `bool` | Required | Model requested. |
| `model_text_shown` | `str` | Required, Constant | Model text shown.<br><br>**Value**: `"False"` |
| `prefill` | `Dict[str, str]` | Required | Prefill. |
| `reply` | [GuideReply](http://localhost:3000/llms-pages/python/models/structures/guide-reply.md) | Required | This is a container for any-of cases. |
| `review` | [`List[GuideReviewRow]`](http://localhost:3000/llms-pages/python/models/structures/guide-review-row.md) | Required | Review. |
| `rounds_used` | `int` | Required | Rounds used. |
| `scenario` | [Scenario1](http://localhost:3000/llms-pages/python/models/enumerations/scenario-1.md) | Required | This is a container for any-of cases. |
| `schema_version` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `stage` | [Stage3](http://localhost:3000/llms-pages/python/models/enumerations/stage-3.md) | Required | This is a container for any-of cases. |
| `started` | `bool` | Required | Started. |
| `subtraction` | [GuideSubtraction](http://localhost:3000/llms-pages/python/models/structures/guide-subtraction.md) | Required | This is a container for any-of cases. |
| `turns_limit` | `int` | Required | Turns limit. |
| `turns_used` | `int` | Required | Turns used. |
| `values_stored` | `str` | Required, Constant | Values stored.<br><br>**Value**: `"False"` |


# Example

```python
from tradeglotlocalconsole.models.chooser_enum import ChooserEnum
from tradeglotlocalconsole.models.chooser_mode_enum import ChooserModeEnum
from tradeglotlocalconsole.models.fallback_reason_enum import FallbackReasonEnum
from tradeglotlocalconsole.models.goods_type_enum import GoodsTypeEnum
from tradeglotlocalconsole.models.guide_analysis import GuideAnalysis
from tradeglotlocalconsole.models.guide_dropped import GuideDropped
from tradeglotlocalconsole.models.guide_field_result import GuideFieldResult
from tradeglotlocalconsole.models.guide_form import GuideForm
from tradeglotlocalconsole.models.guide_form_result import GuideFormResult
from tradeglotlocalconsole.models.guide_gap import GuideGap
from tradeglotlocalconsole.models.guide_item import GuideItem
from tradeglotlocalconsole.models.guide_option import GuideOption
from tradeglotlocalconsole.models.guide_reply import GuideReply
from tradeglotlocalconsole.models.guide_review_row import GuideReviewRow
from tradeglotlocalconsole.models.guide_state_response import GuideStateResponse
from tradeglotlocalconsole.models.guide_subtraction import GuideSubtraction
from tradeglotlocalconsole.models.kind_2_enum import Kind2Enum
from tradeglotlocalconsole.models.reason_5_enum import Reason5Enum
from tradeglotlocalconsole.models.reason_6_enum import Reason6Enum
from tradeglotlocalconsole.models.scenario_1_enum import Scenario1Enum
from tradeglotlocalconsole.models.source_8_enum import Source8Enum
from tradeglotlocalconsole.models.source_9_enum import Source9Enum
from tradeglotlocalconsole.models.stage_3_enum import Stage3Enum
from tradeglotlocalconsole.models.status_8_enum import Status8Enum
from tradeglotlocalconsole.models.status_9_enum import Status9Enum
from tradeglotlocalconsole.models.template_enum import TemplateEnum

guide_state_response = GuideStateResponse(
    analysis=GuideAnalysis(
        reason=Reason5Enum.INVALID_REPLY,
        status=Status8Enum.REPLACED,
        turn=186
    ),
    asked=[
        'asked4',
        'asked5',
        'asked6'
    ],
    auto_confirmed=[
        'auto_confirmed0',
        'auto_confirmed1',
        'auto_confirmed2'
    ],
    chooser_mode=ChooserModeEnum.KEYWORD,
    deferred=[
        'deferred7',
        'deferred8'
    ],
    flow_name='String3',
    form_result=GuideFormResult(
        item='item2',
        valid=False
    ),
    form_results=[
        GuideFieldResult(
            deferred=False,
            item='item6',
            valid=False
        )
    ],
    gap=GuideGap(
        conflicting=[
            'conflicting9',
            'conflicting8'
        ],
        missing=[
            'missing2',
            'missing3',
            'missing4'
        ],
        partial=[
            'partial4',
            'partial3',
            'partial2'
        ],
        present=[
            'present7',
            'present8'
        ]
    ),
    goods_type=GoodsTypeEnum.PHYSICAL,
    items=[
        GuideItem(
            chunk='String9',
            form=GuideForm(
                kind=Kind2Enum.CHOICE,
                options=[
                    GuideOption(
                        label='label2',
                        value='value4'
                    )
                ],
                placeholder='String9'
            ),
            id='id8',
            label='label8',
            source=Source8Enum.OFFICIAL,
            status=Status9Enum.MISSING
        )
    ],
    model_requested=False,
    prefill={
        'key0': 'prefill9'
    },
    reply=GuideReply(
        chooser=ChooserEnum.FORM,
        dropped=[
            GuideDropped(
                item='item2',
                reason=Reason6Enum.OTHER_PARTY
            )
        ],
        fallback_reason=FallbackReasonEnum.LATE,
        state_changed=False,
        template=TemplateEnum.REVIEW,
        text='text0'
    ),
    review=[
        GuideReviewRow(
            item='item4',
            source=Source9Enum.WORDS,
            value='value4'
        )
    ],
    rounds_used=100,
    scenario=Scenario1Enum.PREFLIGHT,
    stage=Stage3Enum.FUNNEL,
    started=False,
    subtraction=GuideSubtraction(
        left=64,
        needed=190,
        taken=178,
        text='text0'
    ),
    turns_limit=88,
    turns_used=242
)
```



