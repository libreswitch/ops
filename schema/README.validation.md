# OpenSwitch Database Schema Validation

In order to verify whether the current OpenSwitch database schema (OPS DB schema)
is valid, a two step approach is taken:

1. A JSON Schema (the "metaschema") is used to validate the OPS DB schema, in
compliance with [JSON Schema Draft 4](http://json-schema.org/).
2. For those rules that the metaschema is unable to validate, a collection of
custom validators are used to verify such aspects. This document describes which
validations are performed using the metaschema and which ones are done with
custom validators.

The main goal is to provide early feedback about the changes on the schema instead
of waiting for the validation done by the `ops-openvswitch` module.


## 1. Metaschema validations

The following validations are performed using the a metaschema file
`ops.metaschema.json`:


### 1.1 Schema level validations

* The schema must have at least the following properties: `name`, `version`,
  `tables`.
* The schema could have the following optional properties: `$schema`, `id`,
  `cksum`, `doc`, `groups`.
* `name` property must be a string.
* `version` property must be a string.
* `tables` property must be an object, for which each property is a table.
* `$schema` property must be an URI string.
* `id` property must be an URI string.
* `cksum` property must be a string, which follows the pattern
  "XXXXXXXXXXXX YYYYYYY", i.e., twelve digits followed by space followed by
  seven more digits.
* `groups` property must be an object, for which each property is a group.
* A group must be an array of strings.
* All `doc` properties inside the schema must be an array of strings.
* All `group` properties inside the schema must be either a string or an array
  of strings.


### 1.2 Table level validations

* A table can be one of two types: a table reference or a proper table.
* A table reference must have one property: `$ref`.
* `$ref` property must be a string.
* A proper table must have at least the following property: `columns`.
* A proper table could have the following optional properties: `title`, `doc`,
  `isRoot`, `maxRows`, `indexes`, `group`.
* `columns` property must be an object, for which each property is a column.
* `title` property must be a string.
* `isRoot` property must be a boolean.
* `maxRows` property must be an integer, with minimum value of 1.
* `indexes` property must be an array of arrays of strings.


### 1.3 Column level validations

* A column must have at least the following properties: `type`.
* A column could have the following optional properties: `ephemeral`,
  `mutable`, `category`, `group`, `title`, `doc`, `relationship`, `emptyValue`,
  `keyname`.
* `type` must be one of the following:
  * Either `"integer"`, `"real"`, `"boolean"`, `"string"` or `"uuid"`.
  * An object with the property `key`, and the following optional properties:
    `value`, `valueMap`, `min`, `max`.
    * `key` and `value` must be a base type.
    * `valueMap` property must be an object, for which each property is a value
      association.
    * A value association is an object with the required property `type`, and
      optional properties `doc`, `group` and `emptyValue`.
      * `type` must be a base type object.
      * `emptyValue` must be of type `"integer"`, `"real"`, `"string"` or
        `"boolean"`.
    * `min` and `max` property must be positive integers or `"unlimited"`.
* A base type must be one of the following:
  * Either `"integer"`, `"real"`, `"boolean"`, `"string"` or `"uuid"`.
  * An object with the required property `type`, and the following optional
    properties: `enum`, `minInteger`, `maxInteger`, `minReal`, `maxReal`,
    `minLength`, `maxLength`, `refTable`, `refType`.
    * `type` must be one of `"integer"`, `"real"`, `"boolean"`,
      `"string"` or `"uuid"`.
    * `enum` property must be an array of values with the same type
      defined in `type`.
    * `minInteger` and `maxInteger` properties must be integers, and can
      be used only if `type` is `"integer"`.
    * `minReal` and `maxReal` properties must be integers, and can be
      used only if `type` is `"real"`.
    * `minLength` and `maxLength` properties must be positive integers,
      and can be used only if `type` is `"string"`.
    * `reftable` property must be an string.
    * `refType` property must be either `"strong"` or `"weak"`.
* `ephemeral` property must be boolean.
* `mutable` property must be boolean.
* `category` property must be one of:
  * Either `"configuration"`, `"status"` or `"statistics"`.
  * An object with the property `follows` of type string.
  * An object with the property `per-value`.
    * `per-value` property must be an array of objects, and such objects must
      have the following properties: `value` and `category`. `category`
      property must be of type string.
* `title` property must be a string.
* `relationship` property must be one of: `"reference"`, `"m:1"` or `"1:m"`.
* `emptyValue` must be integer, real, boolean or string.
* `keyname` must be a string.


## 2. Custom validators

A custom validator is a function inside the script `validators.py` that validates
some schema rules which are difficult or impossible to validate using the
metaschema approach. The following validations are performed using custom
validators:

* `follows` property must have the name of a valid column inside the
  corresponding table.
* `refTable` property must have the name of an existing table in the schema.
* `group` property must have strings that match group names in the `groups`
  property in the schema. If a string in `group` is not found in `groups`, a
  warning is printed.
* `per-value` property must have the same type as the column to which it
  belongs.
* `minLenght` is less than or equal to `maxLength`.
* `minInteger` is less than or equal to `maxInteger`.
* `min` is less than or equal to `max`.
* `min` can not be `"unlimited"`.
* `emptyValue` must have the same type as its parent column.
* All strings inside `indexes` must match a column in the corresponding table.
* All Markdown references inside `doc` must point to valid tables, columns or
  keys inside the schema.
