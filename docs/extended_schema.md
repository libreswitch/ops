# OpenSwitch Extended Schema

####**Category**
`OpenSwitch's` extended schema introduces category feature to differentiate between various types of data present in the database. To allow this each column in the table schema is assigned a category and `REST`, `Declarative Config` and `Config Persistence` features depend on it to allow read or write access to these fields in the database. These categories are,

 - **configuration**
   - `configuration` columns should contain information related to a feature that can be configured using `REST/DC`.
   - `configuration` columns are persistent upon reboot for config persistence feature.
 - **status**
   - `status` columns should contain information related to the feature which cannot be configured using `REST/DC`.
   - `status` columns are not persistent upon reboot for config persistence feature.
 - **statistics**
   - `statistics` columns contain various statistical data that is collected during normal running of a switch. `REST/DC` is only allowed to read this data.
   - `statistics` columns are not persistent upon reboot for config persistence feature.

`OpenSwitch` also introduces the concept of `dynamic` categories that determine the category of a column based on its content. To best describe this we shall use the example of `Route` table. The following is the schema for the `from` column of `Route` table without dynamic categories feature.

    "from":{
    "category":"configuration",
    }

As this column has a category of configuration `REST/DC` allow modification of this column. With the introduction of dyanmic category, the column schema is now,

    "from": {
      "category": {
        "per-value": [
          { "value": "connected", "category": "status" },
          { "value": "static", "category": "configuration" },
          { "value": "bgp", "category": "status" },
          { "value": "ospf", "category": "status" }
        ]
      },

What this syntax implies is that the category of `from` column is dependent upon the value it has in the DB. If `from` column has the value `static` then its category is `configuration` and hence a user is allowed to modify it using `REST/DC`. Whereas, if the value is `connected`, `bgp` or `ospf` the column has the category `status` and hence a user is restricted from modifying its content.

**Note: For this to work, the possible column values should belong to a predetermined set. In this case it is [connected, static, bgp, ospf].**

Dynamic category also allows restriction on other columns. The value of `from` can also decide the category of another column such as the `vrf` column of `Route` table. Without dynamic categories the `vrf` column schema is

      "vrf": {
      "category": "configuration",
      "relationship": "m:1",
      "type": {
        "key": {
          "type": "uuid",
          "refTable": "VRF"
        }
      },
      "mutable": false
    },

Before the introduction of dynamic categories this column's category was `configuration`. Hence, `REST/DC` were allowed to update this entry. With dynamic category the new schema is now
```
    "vrf": {
      "category": {
        "follows": "from"
      },
      "relationship": "m:1",
      "type": {
        "key": {
          "type": "uuid",
          "refTable": "VRF"
        }
      },
      "mutable": false
    },
```
This new representation of the `vrf` column's category means that it is now dependent upon the category of the column it `follows` and in this case, the `from` column.

Category of columns also determines if a row can be added, deleted or updated in a table.

* `CREATE` row is not allowed if `none` of the `index` columns have category `configuration`.
* `DELETE` row is not allowed if `none` of the `index` columns have category `configuration`.
* `UPDATE` row is not allowed if `none` of  the columns have category `configuration`.

####Relationships
`OpenSwitch's` extended schema introduces the concept of relationship to categorize references with respect to the resource that is referencing them. `REST/DC` depend on this categorization to allow `CRUD` operations. A reference can have one of these three relationships,

 - **1:m**
   - References in a column with `1:m` relationship signifies that the resources referenced here are considered `children` of the resource they are referenced from.
   - In a table, all columns with `1:m` relationship must have a unique `refTable`. For example, the following schema is not allowed.
```
    "System": {
      "columns": {
        "bridges": {
          "category": "configuration",
          "relationship": "1:m",
          "type": {
            "key": {
              "type": "uuid",
              "refTable": "Bridge"
            },
            "min": 0,
            "max": "unlimited"
          }
        },
        "bridges_two": {
          "category": "configuration",
          "relationship": "1:m",
          "type": {
            "key": {
              "type": "uuid",
              "refTable": "Bridge"
            },
            "min": 0,
            "max": "unlimited"
          }
        },
```
 - **m:1**
    - A reference in a column with `m:1` relationship signifies that the resource referenced here is considered a `parent` of the resource they are referenced from.
    - There can only be a maximum of one reference in the column with this relationship.
    - Only one column in the table can have an `m:1` relationship.
 - **reference**
   - A reference with this relationship signifies that the resource referenced here doesn't have a `parent` and can exist independently.

####**Index**
 - Always define 'indexes' field for the table schema. `REST/DC` uniquely identify a resource using these as `UUIDs` are not persistent and may change upon reboot.
 - A table may have implicit or explicit indices.
   - `Bridge` table has an explicit index and is clearly defined in its schema whereas `BGP_Routers` have an implicit index. The `asn` value that it is keyed against under `bgp_routers` column in `VRF` table acts as an implicit index.
   - `DHCP_Server` has an implicit index as only one `DHCP_Server` is allowed per `VRF`.
 - A resource `MUST` be uniquely identified within the same table using its indexes.
 - A resource with a missing index means trouble.  See [this](https://tree.taiga.io/project/openswitch/issue/1111)  for an example.

 ####**Naming Convention**
 - Table names are unique.
 - Table names are capitalized. e.g. `Bridge`
 - Column names should not contain table name prefixes as it is redundant. e.g. In `VLAN` table have a column `vlan_id` is discouraged but `id` is preferred.
