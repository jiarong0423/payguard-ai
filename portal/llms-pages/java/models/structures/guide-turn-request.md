# Guide Turn Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkd1aWRlVHVyblJlcXVlc3Q

GuideTurnRequest.


# Class Name

`GuideTurnRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Fields` | [`GuideTurnRequestFields`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/guide-turn-request-fields.md) | Optional | This is a container for any-of cases. | GuideTurnRequestFields getFields() | setFields(GuideTurnRequestFields fields) |
| `Scenario` | [`GuideTurnRequestScenario`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/guide-turn-request-scenario.md) | Optional | This is a container for any-of cases. | GuideTurnRequestScenario getScenario() | setScenario(GuideTurnRequestScenario scenario) |
| `Text` | `String` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1600` | String getText() | setText(String text) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.GuideField;
import m18000.m0.m0.m127.models.GuideTurnRequest;
import m18000.m0.m0.m127.models.Scenario1Enum;
import m18000.m0.m0.m127.models.containers.GuideTurnRequestFields;
import m18000.m0.m0.m127.models.containers.GuideTurnRequestScenario;

GuideTurnRequest guideTurnRequest = new GuideTurnRequest.Builder(
    "text2"
)
.fields(GuideTurnRequestFields.fromListOfGuideField(
        Arrays.asList(
            new GuideField.Builder(
                "item8",
                "value8"
            )
            .build()
        )
    ))
.scenario(GuideTurnRequestScenario.fromScenario1(
        Scenario1Enum.PREFLIGHT
    ))
.build();
```



