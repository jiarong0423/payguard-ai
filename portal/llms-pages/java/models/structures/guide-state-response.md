# Guide State Response

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZQ

GuideStateResponse.


# Class Name

`GuideStateResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AdvisoryOnly` | `String` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` | String getAdvisoryOnly() | setAdvisoryOnly(String advisoryOnly) |
| `Analysis` | [`GuideStateResponseAnalysis`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/guide-state-response-analysis.md) | Required | This is a container for any-of cases. | GuideStateResponseAnalysis getAnalysis() | setAnalysis(GuideStateResponseAnalysis analysis) |
| `Asked` | `List<String>` | Required | Asked.<br><br>**Constraints**: *Maximum Items*: `3` | List<String> getAsked() | setAsked(List<String> asked) |
| `AutoConfirmed` | `List<String>` | Required | Auto confirmed. | List<String> getAutoConfirmed() | setAutoConfirmed(List<String> autoConfirmed) |
| `ChooserMode` | [`ChooserModeEnum`](http://localhost:3000/llms-pages/java/models/enumerations/chooser-mode.md) | Required | Chooser mode. | ChooserModeEnum getChooserMode() | setChooserMode(ChooserModeEnum chooserMode) |
| `Deferred` | `List<String>` | Required | Deferred. | List<String> getDeferred() | setDeferred(List<String> deferred) |
| `FlowName` | [`GuideStateResponseFlowName`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/guide-state-response-flow-name.md) | Required | This is a container for any-of cases. | GuideStateResponseFlowName getFlowName() | setFlowName(GuideStateResponseFlowName flowName) |
| `FormResult` | [`GuideStateResponseFormResult`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/guide-state-response-form-result.md) | Required | This is a container for any-of cases. | GuideStateResponseFormResult getFormResult() | setFormResult(GuideStateResponseFormResult formResult) |
| `FormResults` | [`List<GuideFieldResult>`](http://localhost:3000/llms-pages/java/models/structures/guide-field-result.md) | Required | Form results. | List<GuideFieldResult> getFormResults() | setFormResults(List<GuideFieldResult> formResults) |
| `Gap` | [`GuideGap`](http://localhost:3000/llms-pages/java/models/structures/guide-gap.md) | Required | GuideGap. | GuideGap getGap() | setGap(GuideGap gap) |
| `GoodsType` | [`GuideStateResponseGoodsType`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/guide-state-response-goods-type.md) | Required | This is a container for any-of cases. | GuideStateResponseGoodsType getGoodsType() | setGoodsType(GuideStateResponseGoodsType goodsType) |
| `Items` | [`List<GuideItem>`](http://localhost:3000/llms-pages/java/models/structures/guide-item.md) | Required | Items. | List<GuideItem> getItems() | setItems(List<GuideItem> items) |
| `ModelRequested` | `boolean` | Required | Model requested. | boolean getModelRequested() | setModelRequested(boolean modelRequested) |
| `ModelTextShown` | `String` | Required, Constant | Model text shown.<br><br>**Value**: `"False"` | String getModelTextShown() | setModelTextShown(String modelTextShown) |
| `Prefill` | `Map<String, String>` | Required | Prefill. | Map<String, String> getPrefill() | setPrefill(Map<String, String> prefill) |
| `Reply` | [`GuideStateResponseReply`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/guide-state-response-reply.md) | Required | This is a container for any-of cases. | GuideStateResponseReply getReply() | setReply(GuideStateResponseReply reply) |
| `Review` | [`List<GuideReviewRow>`](http://localhost:3000/llms-pages/java/models/structures/guide-review-row.md) | Required | Review. | List<GuideReviewRow> getReview() | setReview(List<GuideReviewRow> review) |
| `RoundsUsed` | `int` | Required | Rounds used. | int getRoundsUsed() | setRoundsUsed(int roundsUsed) |
| `Scenario` | [`GuideStateResponseScenario`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/guide-state-response-scenario.md) | Required | This is a container for any-of cases. | GuideStateResponseScenario getScenario() | setScenario(GuideStateResponseScenario scenario) |
| `SchemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` | int getSchemaVersion() | setSchemaVersion(int schemaVersion) |
| `Stage` | [`GuideStateResponseStage`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/guide-state-response-stage.md) | Required | This is a container for any-of cases. | GuideStateResponseStage getStage() | setStage(GuideStateResponseStage stage) |
| `Started` | `boolean` | Required | Started. | boolean getStarted() | setStarted(boolean started) |
| `Subtraction` | [`GuideStateResponseSubtraction`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/guide-state-response-subtraction.md) | Required | This is a container for any-of cases. | GuideStateResponseSubtraction getSubtraction() | setSubtraction(GuideStateResponseSubtraction subtraction) |
| `TurnsLimit` | `int` | Required | Turns limit. | int getTurnsLimit() | setTurnsLimit(int turnsLimit) |
| `TurnsUsed` | `int` | Required | Turns used. | int getTurnsUsed() | setTurnsUsed(int turnsUsed) |
| `ValuesStored` | `String` | Required, Constant | Values stored.<br><br>**Value**: `"False"` | String getValuesStored() | setValuesStored(String valuesStored) |


# Example

```java
import java.util.Arrays;
import java.util.LinkedHashMap;
import m18000.m0.m0.m127.models.ChooserEnum;
import m18000.m0.m0.m127.models.ChooserModeEnum;
import m18000.m0.m0.m127.models.FallbackReasonEnum;
import m18000.m0.m0.m127.models.GoodsTypeEnum;
import m18000.m0.m0.m127.models.GuideAnalysis;
import m18000.m0.m0.m127.models.GuideDropped;
import m18000.m0.m0.m127.models.GuideFieldResult;
import m18000.m0.m0.m127.models.GuideForm;
import m18000.m0.m0.m127.models.GuideFormResult;
import m18000.m0.m0.m127.models.GuideGap;
import m18000.m0.m0.m127.models.GuideItem;
import m18000.m0.m0.m127.models.GuideOption;
import m18000.m0.m0.m127.models.GuideReply;
import m18000.m0.m0.m127.models.GuideReviewRow;
import m18000.m0.m0.m127.models.GuideStateResponse;
import m18000.m0.m0.m127.models.GuideSubtraction;
import m18000.m0.m0.m127.models.Kind2Enum;
import m18000.m0.m0.m127.models.Reason5Enum;
import m18000.m0.m0.m127.models.Reason6Enum;
import m18000.m0.m0.m127.models.Scenario1Enum;
import m18000.m0.m0.m127.models.Source8Enum;
import m18000.m0.m0.m127.models.Source9Enum;
import m18000.m0.m0.m127.models.Stage3Enum;
import m18000.m0.m0.m127.models.Status8Enum;
import m18000.m0.m0.m127.models.Status9Enum;
import m18000.m0.m0.m127.models.TemplateEnum;
import m18000.m0.m0.m127.models.containers.GuideAnalysisReason;
import m18000.m0.m0.m127.models.containers.GuideFormPlaceholder;
import m18000.m0.m0.m127.models.containers.GuideItemChunk;
import m18000.m0.m0.m127.models.containers.GuideItemForm;
import m18000.m0.m0.m127.models.containers.GuideReplyFallbackReason;
import m18000.m0.m0.m127.models.containers.GuideStateResponseAnalysis;
import m18000.m0.m0.m127.models.containers.GuideStateResponseFlowName;
import m18000.m0.m0.m127.models.containers.GuideStateResponseFormResult;
import m18000.m0.m0.m127.models.containers.GuideStateResponseGoodsType;
import m18000.m0.m0.m127.models.containers.GuideStateResponseReply;
import m18000.m0.m0.m127.models.containers.GuideStateResponseScenario;
import m18000.m0.m0.m127.models.containers.GuideStateResponseStage;
import m18000.m0.m0.m127.models.containers.GuideStateResponseSubtraction;

GuideStateResponse guideStateResponse = new GuideStateResponse.Builder(
    "True",
    GuideStateResponseAnalysis.fromGuideAnalysis(
        new GuideAnalysis.Builder(
            GuideAnalysisReason.fromReason5(
                Reason5Enum.INVALID_REPLY
            ),
            Status8Enum.REPLACED,
            186
        )
        .build()
    ),
    Arrays.asList(
        "asked6",
        "asked7"
    ),
    Arrays.asList(
        "auto_confirmed2",
        "auto_confirmed3"
    ),
    ChooserModeEnum.KEYWORD,
    Arrays.asList(
        "deferred9"
    ),
    GuideStateResponseFlowName.fromString(
        "String1"
    ),
    GuideStateResponseFormResult.fromGuideFormResult(
        new GuideFormResult.Builder(
            "item2",
            false
        )
        .build()
    ),
    Arrays.asList(
        new GuideFieldResult.Builder(
            false,
            "item6",
            false
        )
        .build()
    ),
    new GuideGap.Builder(
        Arrays.asList(
            "conflicting9",
            "conflicting8"
        ),
        Arrays.asList(
            "missing2",
            "missing3",
            "missing4"
        ),
        Arrays.asList(
            "partial4",
            "partial3",
            "partial2"
        ),
        Arrays.asList(
            "present7",
            "present8"
        )
    )
    .build(),
    GuideStateResponseGoodsType.fromGoodsType(
        GoodsTypeEnum.PHYSICAL
    ),
    Arrays.asList(
        new GuideItem.Builder(
            GuideItemChunk.fromString(
                "String9"
            ),
            GuideItemForm.fromGuideForm(
                new GuideForm.Builder(
                    Kind2Enum.CHOICE,
                    Arrays.asList(
                        new GuideOption.Builder(
                            "label2",
                            "value4"
                        )
                        .build()
                    ),
                    GuideFormPlaceholder.fromString(
                        "String9"
                    )
                )
                .build()
            ),
            "id8",
            "label8",
            Source8Enum.OFFICIAL,
            Status9Enum.MISSING
        )
        .build()
    ),
    false,
    "False",
    new LinkedHashMap<String, String>() {{
        put("key0", "prefill7");
        put("key1", "prefill8");
        put("key2", "prefill9");
    }},
    GuideStateResponseReply.fromGuideReply(
        new GuideReply.Builder(
            ChooserEnum.FORM,
            Arrays.asList(
                new GuideDropped.Builder(
                    "item2",
                    Reason6Enum.OTHER_PARTY
                )
                .build()
            ),
            GuideReplyFallbackReason.fromFallbackReason(
                FallbackReasonEnum.LATE
            ),
            false,
            TemplateEnum.REVIEW,
            "text0"
        )
        .build()
    ),
    Arrays.asList(
        new GuideReviewRow.Builder(
            "item4",
            Source9Enum.WORDS,
            "value4"
        )
        .build()
    ),
    242,
    GuideStateResponseScenario.fromScenario1(
        Scenario1Enum.DISPUTE
    ),
    1,
    GuideStateResponseStage.fromStage3(
        Stage3Enum.REVIEW
    ),
    false,
    GuideStateResponseSubtraction.fromGuideSubtraction(
        new GuideSubtraction.Builder(
            64,
            190,
            178,
            "text0"
        )
        .build()
    ),
    230,
    128,
    "False"
)
.build();
```



