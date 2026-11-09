# Case Route Match

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkNhc2VSb3V0ZU1hdGNo

CaseRouteMatch.


# Class Name

`CaseRouteMatch`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Category` | [`CaseRouteMatchCategory`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/case-route-match-category.md) | Required | This is a container for any-of cases. | CaseRouteMatchCategory getCategory() | setCategory(CaseRouteMatchCategory category) |
| `ExactWords` | `List<String>` | Required | Exact words.<br><br>**Constraints**: *Maximum Items*: `8`, *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z0-9]+$` | List<String> getExactWords() | setExactWords(List<String> exactWords) |
| `MatchType` | [`MatchTypeEnum`](http://localhost:3000/llms-pages/java/models/enumerations/match-type.md) | Required | Match type. | MatchTypeEnum getMatchType() | setMatchType(MatchTypeEnum matchType) |
| `ProductId` | `String` | Required | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` | String getProductId() | setProductId(String productId) |
| `Score` | `double` | Required | Score.<br><br>**Constraints**: `>= 0`, `<= 1` | double getScore() | setScore(double score) |
| `Title` | `String` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` | String getTitle() | setTitle(String title) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.CaseRouteMatch;
import m18000.m0.m0.m127.models.MatchTypeEnum;
import m18000.m0.m0.m127.models.containers.CaseRouteMatchCategory;

CaseRouteMatch caseRouteMatch = new CaseRouteMatch.Builder(
    CaseRouteMatchCategory.fromString(
        "String7"
    ),
    Arrays.asList(
        "exact_words4",
        "exact_words3"
    ),
    MatchTypeEnum.EXACT,
    "product_id4",
    1D,
    "title4"
)
.build();
```



