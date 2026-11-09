# Dispute Requirement

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkRpc3B1dGVSZXF1aXJlbWVudA

DisputeRequirement.


# Class Name

`DisputeRequirement`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `acceptedAttachmentCount` | `int` | Required | Accepted attachment count.<br><br>**Constraints**: `>= 0`, `<= 20` | getAcceptedAttachmentCount(): int | setAcceptedAttachmentCount(int acceptedAttachmentCount): void |
| `action` | string\|null | Optional | This is a container for any-of cases. | getAction(): ?string | setAction(?string action): void |
| `evidenceType` | string\|null | Optional | This is a container for any-of cases. | getEvidenceType(): ?string | setEvidenceType(?string evidenceType): void |
| `mandatory` | `bool` | Required | Mandatory. | getMandatory(): bool | setMandatory(bool mandatory): void |
| `proofCount` | `int` | Required | Proof count.<br><br>**Constraints**: `>= 0`, `<= 128` | getProofCount(): int | setProofCount(int proofCount): void |
| `providerEvidenceType` | `string` | Required | Provider evidence type.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z][A-Z0-9_]{0,127}$` | getProviderEvidenceType(): string | setProviderEvidenceType(string providerEvidenceType): void |
| `requestId` | `string` | Required | Request id.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$` | getRequestId(): string | setRequestId(string requestId): void |
| `requirementState` | [`string(RequirementStateEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/requirement-state.md) | Required | Requirement state. | getRequirementState(): string | setRequirementState(string requirementState): void |
| `source` | `string` | Required | Source.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z][A-Z0-9_]{0,127}$` | getSource(): string | setSource(string source): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\DisputeRequirementBuilder;
use TradeGlotLocalConsoleLib\Models\RequirementStateEnum;

$disputeRequirement = DisputeRequirementBuilder::init(
    8,
    false,
    128,
    'provider_evidence_type4',
    'request_id6',
    RequirementStateEnum::CONTEXT_ONLY,
    'source2'
)
    ->action(
        'String1'
    )
    ->evidenceType(
        'String3'
    )
    ->build();
```



