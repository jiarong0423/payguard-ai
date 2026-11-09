# Guide Form Request

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkd1aWRlRm9ybVJlcXVlc3Q

One field ({item, value}) or one round of up to three fields ({fields: [...]}), never both.


# Class Name

`GuideFormRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `ConfirmReview` | `Boolean` | Optional | Confirm review.<br><br>**Default**: `false` | Boolean getConfirmReview() | setConfirmReview(Boolean confirmReview) |
| `Fields` | [`GuideFormRequestFields`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/guide-form-request-fields.md) | Optional | This is a container for any-of cases. | GuideFormRequestFields getFields() | setFields(GuideFormRequestFields fields) |
| `Item` | [`GuideFormRequestItem`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/guide-form-request-item.md) | Optional | This is a container for any-of cases. | GuideFormRequestItem getItem() | setItem(GuideFormRequestItem item) |
| `Scenario` | [`GuideFormRequestScenario`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/guide-form-request-scenario.md) | Optional | This is a container for any-of cases. | GuideFormRequestScenario getScenario() | setScenario(GuideFormRequestScenario scenario) |
| `Value` | [`GuideFormRequestValue`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/guide-form-request-value.md) | Optional | This is a container for any-of cases. | GuideFormRequestValue getValue() | setValue(GuideFormRequestValue value) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.GuideField;
import m18000.m0.m0.m127.models.GuideFormRequest;
import m18000.m0.m0.m127.models.Scenario1Enum;
import m18000.m0.m0.m127.models.containers.GuideFormRequestFields;
import m18000.m0.m0.m127.models.containers.GuideFormRequestItem;
import m18000.m0.m0.m127.models.containers.GuideFormRequestScenario;
import m18000.m0.m0.m127.models.containers.GuideFormRequestValue;

GuideFormRequest guideFormRequest = new GuideFormRequest.Builder()
    .confirmReview(false)
    .fields(GuideFormRequestFields.fromListOfGuideField(
        Arrays.asList(
            new GuideField.Builder(
                "item8",
                "value8"
            )
            .build()
        )
    ))
    .item(GuideFormRequestItem.fromString(
        "String1"
    ))
    .scenario(GuideFormRequestScenario.fromScenario1(
        Scenario1Enum.PREFLIGHT
    ))
    .value(GuideFormRequestValue.fromString(
        "String1"
    ))
    .build();
```



