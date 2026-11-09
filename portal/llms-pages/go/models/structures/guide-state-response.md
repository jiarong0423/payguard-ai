# Guide State Response

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZQ

GuideStateResponse.


# Class Name

`GuideStateResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `Analysis` | [`models.GuideStateResponseAnalysis`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-state-response-analysis.md) | Required | This is a container for any-of cases. |
| `Asked` | `[]string` | Required | Asked.<br><br>**Constraints**: *Maximum Items*: `3` |
| `AutoConfirmed` | `[]string` | Required | Auto confirmed. |
| `ChooserMode` | [`models.ChooserModeEnum`](http://localhost:3000/llms-pages/go/models/enumerations/chooser-mode.md) | Required | Chooser mode. |
| `Deferred` | `[]string` | Required | Deferred. |
| `FlowName` | [`models.GuideStateResponseFlowName`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-state-response-flow-name.md) | Required | This is a container for any-of cases. |
| `FormResult` | [`models.GuideStateResponseFormResult`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-state-response-form-result.md) | Required | This is a container for any-of cases. |
| `FormResults` | [`[]models.GuideFieldResult`](http://localhost:3000/llms-pages/go/models/structures/guide-field-result.md) | Required | Form results. |
| `Gap` | [`models.GuideGap`](http://localhost:3000/llms-pages/go/models/structures/guide-gap.md) | Required | GuideGap. |
| `GoodsType` | [`models.GuideStateResponseGoodsType`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-state-response-goods-type.md) | Required | This is a container for any-of cases. |
| `Items` | [`[]models.GuideItem`](http://localhost:3000/llms-pages/go/models/structures/guide-item.md) | Required | Items. |
| `ModelRequested` | `bool` | Required | Model requested. |
| `ModelTextShown` | `string` | Required, Constant | Model text shown.<br><br>**Value**: `"False"` |
| `Prefill` | `map[string]string` | Required | Prefill. |
| `Reply` | [`models.GuideStateResponseReply`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-state-response-reply.md) | Required | This is a container for any-of cases. |
| `Review` | [`[]models.GuideReviewRow`](http://localhost:3000/llms-pages/go/models/structures/guide-review-row.md) | Required | Review. |
| `RoundsUsed` | `int` | Required | Rounds used. |
| `Scenario` | [`models.GuideStateResponseScenario`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-state-response-scenario.md) | Required | This is a container for any-of cases. |
| `SchemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `Stage` | [`models.GuideStateResponseStage`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-state-response-stage.md) | Required | This is a container for any-of cases. |
| `Started` | `bool` | Required | Started. |
| `Subtraction` | [`models.GuideStateResponseSubtraction`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-state-response-subtraction.md) | Required | This is a container for any-of cases. |
| `TurnsLimit` | `int` | Required | Turns limit. |
| `TurnsUsed` | `int` | Required | Turns used. |
| `ValuesStored` | `string` | Required, Constant | Values stored.<br><br>**Value**: `"False"` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideStateResponse := models.GuideStateResponse{
        AdvisoryOnly:   "True",
        Analysis:       models.GuideStateResponseAnalysisContainer.FromGuideAnalysis(models.GuideAnalysis{
            Reason: models.GuideAnalysisReasonContainer.FromReason5(models.Reason5Enum_INVALIDREPLY),
            Status: models.Status8Enum_REPLACED,
            Turn:   186,
        }),
        Asked:          []string{
            "asked6",
            "asked7",
        },
        AutoConfirmed:  []string{
            "auto_confirmed2",
            "auto_confirmed3",
        },
        ChooserMode:    models.ChooserModeEnum_KEYWORD,
        Deferred:       []string{
            "deferred9",
        },
        FlowName:       models.GuideStateResponseFlowNameContainer.FromString("String1"),
        FormResult:     models.GuideStateResponseFormResultContainer.FromGuideFormResult(models.GuideFormResult{
            Item:  "item2",
            Valid: false,
        }),
        FormResults:    []models.GuideFieldResult{
            models.GuideFieldResult{
                Deferred: false,
                Item:     "item6",
                Valid:    false,
            },
        },
        Gap:            models.GuideGap{
            Conflicting: []string{
                "conflicting9",
                "conflicting8",
            },
            Missing:     []string{
                "missing2",
                "missing3",
                "missing4",
            },
            Partial:     []string{
                "partial4",
                "partial3",
                "partial2",
            },
            Present:     []string{
                "present7",
                "present8",
            },
        },
        GoodsType:      models.GuideStateResponseGoodsTypeContainer.FromGoodsType(models.GoodsTypeEnum_PHYSICAL),
        Items:          []models.GuideItem{
            models.GuideItem{
                Chunk:  models.GuideItemChunkContainer.FromString("String9"),
                Form:   models.GuideItemFormContainer.FromGuideForm(models.GuideForm{
                    Kind:        models.Kind2Enum_CHOICE,
                    Options:     []models.GuideOption{
                        models.GuideOption{
                            Label: "label2",
                            Value: "value4",
                        },
                    },
                    Placeholder: models.GuideFormPlaceholderContainer.FromString("String9"),
                }),
                Id:     "id8",
                Label:  "label8",
                Source: models.Source8Enum_OFFICIAL,
                Status: models.Status9Enum_MISSING,
            },
        },
        ModelRequested: false,
        ModelTextShown: "False",
        Prefill:        map[string]string{
            "key0": "prefill7",
            "key1": "prefill8",
            "key2": "prefill9",
        },
        Reply:          models.GuideStateResponseReplyContainer.FromGuideReply(models.GuideReply{
            Chooser:        models.ChooserEnum_FORM,
            Dropped:        []models.GuideDropped{
                models.GuideDropped{
                    Item:   "item2",
                    Reason: models.Reason6Enum_OTHERPARTY,
                },
            },
            FallbackReason: models.GuideReplyFallbackReasonContainer.FromFallbackReason(models.FallbackReasonEnum_LATE),
            StateChanged:   false,
            Template:       models.TemplateEnum_REVIEW,
            Text:           "text0",
        }),
        Review:         []models.GuideReviewRow{
            models.GuideReviewRow{
                Item:   "item4",
                Source: models.Source9Enum_WORDS,
                Value:  "value4",
            },
        },
        RoundsUsed:     242,
        Scenario:       models.GuideStateResponseScenarioContainer.FromScenario1(models.Scenario1Enum_DISPUTE),
        SchemaVersion:  1,
        Stage:          models.GuideStateResponseStageContainer.FromStage3(models.Stage3Enum_REVIEW),
        Started:        false,
        Subtraction:    models.GuideStateResponseSubtractionContainer.FromGuideSubtraction(models.GuideSubtraction{
            Left:                 64,
            Needed:               190,
            Taken:                178,
            Text:                 "text0",
        }),
        TurnsLimit:     230,
        TurnsUsed:      128,
        ValuesStored:   "False",
    }

}
```



