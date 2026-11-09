# Evidence Input

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXQ

EvidenceInput.


# Class Name

`EvidenceInput`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Evidences` | [`List<EvidenceInputItem>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/evidence-input-item.md) | Required | Evidences.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` | List<EvidenceInputItem> getEvidences() | setEvidences(List<EvidenceInputItem> evidences) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.CarrierNameEnum;
import m18000.m0.m0.m127.models.EvidenceInfo;
import m18000.m0.m0.m127.models.EvidenceInput;
import m18000.m0.m0.m127.models.EvidenceInputItem;
import m18000.m0.m0.m127.models.TrackingInfo;
import m18000.m0.m0.m127.models.containers.TrackingInfoCarrierNameOther;

EvidenceInput evidenceInput = new EvidenceInput.Builder(
    Arrays.asList(
        new EvidenceInputItem.Builder(
            new EvidenceInfo.Builder(
                Arrays.asList(
                    new TrackingInfo.Builder(
                        CarrierNameEnum.DHL,
                        "tracking_number6"
                    )
                    .carrierNameOther(TrackingInfoCarrierNameOther.fromString(
                            "String1"
                        ))
                    .build()
                )
            )
            .build(),
            "evidence_type2",
            "notes2"
        )
        .build()
    )
)
.build();
```



