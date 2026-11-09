# Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkV2aWRlbmNl

Evidence.


# Class Name

`Evidence`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CarrierStatus` | [`EvidenceCarrierStatus`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/evidence-carrier-status.md) | Optional | This is a container for any-of cases. | EvidenceCarrierStatus getCarrierStatus() | setCarrierStatus(EvidenceCarrierStatus carrierStatus) |
| `DeliveredAt` | [`EvidenceDeliveredAt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/evidence-delivered-at.md) | Optional | This is a container for any-of cases. | EvidenceDeliveredAt getDeliveredAt() | setDeliveredAt(EvidenceDeliveredAt deliveredAt) |
| `EvidenceSource` | `String` | Required, Constant | Evidence source.<br><br>**Value**: `"synthetic"` | String getEvidenceSource() | setEvidenceSource(String evidenceSource) |
| `OpenedAt` | [`EvidenceOpenedAt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/evidence-opened-at.md) | Optional | This is a container for any-of cases. | EvidenceOpenedAt getOpenedAt() | setOpenedAt(EvidenceOpenedAt openedAt) |
| `OrderCreatedAt` | [`EvidenceOrderCreatedAt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/evidence-order-created-at.md) | Optional | This is a container for any-of cases. | EvidenceOrderCreatedAt getOrderCreatedAt() | setOrderCreatedAt(EvidenceOrderCreatedAt orderCreatedAt) |
| `Reason` | [`EvidenceReason`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/evidence-reason.md) | Optional | This is a container for any-of cases. | EvidenceReason getReason() | setReason(EvidenceReason reason) |


# Example

```java
import m18000.m0.m0.m127.models.Evidence;
import m18000.m0.m0.m127.models.containers.EvidenceCarrierStatus;
import m18000.m0.m0.m127.models.containers.EvidenceDeliveredAt;
import m18000.m0.m0.m127.models.containers.EvidenceOpenedAt;
import m18000.m0.m0.m127.models.containers.EvidenceOrderCreatedAt;
import m18000.m0.m0.m127.models.containers.EvidenceReason;

Evidence evidence = new Evidence.Builder(
    "synthetic"
)
.carrierStatus(EvidenceCarrierStatus.fromString(
        "String5"
    ))
.deliveredAt(EvidenceDeliveredAt.fromString(
        "String1"
    ))
.openedAt(EvidenceOpenedAt.fromString(
        "String1"
    ))
.orderCreatedAt(EvidenceOrderCreatedAt.fromString(
        "String3"
    ))
.reason(EvidenceReason.fromString(
        "String3"
    ))
.build();
```



