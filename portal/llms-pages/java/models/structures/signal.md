# Signal

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlNpZ25hbA

Signal.


# Class Name

`Signal`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Category` | [`SignalCategory`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/signal-category.md) | Optional | This is a container for any-of cases. | SignalCategory getCategory() | setCategory(SignalCategory category) |
| `Confidence` | [`SignalConfidence`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/signal-confidence.md) | Optional | This is a container for any-of cases. | SignalConfidence getConfidence() | setConfidence(SignalConfidence confidence) |
| `Source` | [`Source2Enum`](http://localhost:3000/llms-pages/java/models/enumerations/source-2.md) | Optional | Source. | Source2Enum getSource() | setSource(Source2Enum source) |


# Example

```java
import m18000.m0.m0.m127.models.ConfidenceEnum;
import m18000.m0.m0.m127.models.Signal;
import m18000.m0.m0.m127.models.Source2Enum;
import m18000.m0.m0.m127.models.containers.SignalCategory;
import m18000.m0.m0.m127.models.containers.SignalConfidence;

Signal signal = new Signal.Builder()
    .category(SignalCategory.fromString(
        "String1"
    ))
    .confidence(SignalConfidence.fromConfidence(
        ConfidenceEnum.HIGH
    ))
    .source(Source2Enum.CHANNEL3)
    .build();
```



