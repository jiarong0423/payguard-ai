# Guide State Response

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZQ

GuideStateResponse.


# Class Name

`GuideStateResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `Analysis` | [`GuideStateResponseAnalysis`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-state-response-analysis.md) | Required | This is a container for any-of cases. |
| `Asked` | `List<string>` | Required | Asked.<br><br>**Constraints**: *Maximum Items*: `3` |
| `AutoConfirmed` | `List<string>` | Required | Auto confirmed. |
| `ChooserMode` | [`ChooserModeEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/chooser-mode.md) | Required | Chooser mode. |
| `Deferred` | `List<string>` | Required | Deferred. |
| `FlowName` | [`GuideStateResponseFlowName`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-state-response-flow-name.md) | Required | This is a container for any-of cases. |
| `FormResult` | [`GuideStateResponseFormResult`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-state-response-form-result.md) | Required | This is a container for any-of cases. |
| `FormResults` | [`List<GuideFieldResult>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-field-result.md) | Required | Form results. |
| `Gap` | [`GuideGap`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-gap.md) | Required | GuideGap. |
| `GoodsType` | [`GuideStateResponseGoodsType`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-state-response-goods-type.md) | Required | This is a container for any-of cases. |
| `Items` | [`List<GuideItem>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-item.md) | Required | Items. |
| `ModelRequested` | `bool` | Required | Model requested. |
| `ModelTextShown` | `string` | Required, Constant | Model text shown.<br><br>**Value**: `"False"` |
| `Prefill` | `Dictionary<string, string>` | Required | Prefill. |
| `Reply` | [`GuideStateResponseReply`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-state-response-reply.md) | Required | This is a container for any-of cases. |
| `Review` | [`List<GuideReviewRow>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-review-row.md) | Required | Review. |
| `RoundsUsed` | `int` | Required | Rounds used. |
| `Scenario` | [`GuideStateResponseScenario`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-state-response-scenario.md) | Required | This is a container for any-of cases. |
| `SchemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `Stage` | [`GuideStateResponseStage`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-state-response-stage.md) | Required | This is a container for any-of cases. |
| `Started` | `bool` | Required | Started. |
| `Subtraction` | [`GuideStateResponseSubtraction`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-state-response-subtraction.md) | Required | This is a container for any-of cases. |
| `TurnsLimit` | `int` | Required | Turns limit. |
| `TurnsUsed` | `int` | Required | Turns used. |
| `ValuesStored` | `string` | Required, Constant | Values stored.<br><br>**Value**: `"False"` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

GuideStateResponse guideStateResponse = new GuideStateResponse
{
    AdvisoryOnly = "True",
    Analysis = GuideStateResponseAnalysis.FromGuideAnalysis(
        new GuideAnalysis
        {
            Reason = GuideAnalysisReason.FromReason5(Reason5Enum.InvalidReply),
            Status = Status8Enum.Replaced,
            Turn = 186,
        }
    ),
    Asked = new List<string>
    {
        "asked6",
        "asked7",
    },
    AutoConfirmed = new List<string>
    {
        "auto_confirmed2",
        "auto_confirmed3",
    },
    ChooserMode = ChooserModeEnum.Keyword,
    Deferred = new List<string>
    {
        "deferred9",
    },
    FlowName = GuideStateResponseFlowName.FromString("String1"),
    FormResult = GuideStateResponseFormResult.FromGuideFormResult(
        new GuideFormResult
        {
            Item = "item2",
            Valid = false,
        }
    ),
    FormResults = new List<GuideFieldResult>
    {
        new GuideFieldResult
        {
            Deferred = false,
            Item = "item6",
            Valid = false,
        },
    },
    Gap = new GuideGap
    {
        Conflicting = new List<string>
        {
            "conflicting9",
            "conflicting8",
        },
        Missing = new List<string>
        {
            "missing2",
            "missing3",
            "missing4",
        },
        MPartial = new List<string>
        {
            "partial4",
            "partial3",
            "partial2",
        },
        Present = new List<string>
        {
            "present7",
            "present8",
        },
    },
    GoodsType = GuideStateResponseGoodsType.FromGoodsType(GoodsTypeEnum.Physical),
    Items = new List<GuideItem>
    {
        new GuideItem
        {
            Chunk = GuideItemChunk.FromString("String9"),
            Form = GuideItemForm.FromGuideForm(
                new GuideForm
                {
                    Kind = Kind2Enum.Choice,
                    Options = new List<GuideOption>
                    {
                        new GuideOption
                        {
                            Label = "label2",
                            MValue = "value4",
                        },
                    },
                    Placeholder = GuideFormPlaceholder.FromString("String9"),
                }
            ),
            Id = "id8",
            Label = "label8",
            Source = Source8Enum.OFFICIAL,
            Status = Status9Enum.MISSING,
        },
    },
    ModelRequested = false,
    ModelTextShown = "False",
    Prefill = new Dictionary<string, string>
    {
        ["key0"] = "prefill7",
        ["key1"] = "prefill8",
        ["key2"] = "prefill9",
    },
    Reply = GuideStateResponseReply.FromGuideReply(
        new GuideReply
        {
            Chooser = ChooserEnum.Form,
            Dropped = new List<GuideDropped>
            {
                new GuideDropped
                {
                    Item = "item2",
                    Reason = Reason6Enum.OtherParty,
                },
            },
            FallbackReason = GuideReplyFallbackReason.FromFallbackReason(FallbackReasonEnum.Late),
            StateChanged = false,
            Template = TemplateEnum.REVIEW,
            Text = "text0",
        }
    ),
    Review = new List<GuideReviewRow>
    {
        new GuideReviewRow
        {
            Item = "item4",
            Source = Source9Enum.Words,
            MValue = "value4",
        },
    },
    RoundsUsed = 242,
    Scenario = GuideStateResponseScenario.FromScenario1(Scenario1Enum.Dispute),
    SchemaVersion = 1,
    Stage = GuideStateResponseStage.FromStage3(Stage3Enum.Review),
    Started = false,
    Subtraction = GuideStateResponseSubtraction.FromGuideSubtraction(
        new GuideSubtraction
        {
            Left = 64,
            Needed = 190,
            Taken = 178,
            Text = "text0",
        }
    ),
    TurnsLimit = 230,
    TurnsUsed = 128,
    ValuesStored = "False",
};
```



