# Evidence Input Item

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXRJdGVt

EvidenceInputItem.


# Class Name

`EvidenceInputItem`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `EvidenceInfo` | [`EvidenceInfo`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/evidence-info.md) | Required | EvidenceInfo. | EvidenceInfo getEvidenceInfo() | setEvidenceInfo(EvidenceInfo evidenceInfo) |
| `EvidenceType` | `String` | Required | Evidence type.<br><br>**Constraints**: *Pattern*: `^[A-Z][A-Z0-9_]{0,63}$` | String getEvidenceType() | setEvidenceType(String evidenceType) |
| `Notes` | `String` | Required | Notes.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` | String getNotes() | setNotes(String notes) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.CarrierNameEnum;
import m18000.m0.m0.m127.models.EvidenceInfo;
import m18000.m0.m0.m127.models.EvidenceInputItem;
import m18000.m0.m0.m127.models.TrackingInfo;
import m18000.m0.m0.m127.models.containers.TrackingInfoCarrierNameOther;

EvidenceInputItem evidenceInputItem = new EvidenceInputItem.Builder(
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
.build();
```



