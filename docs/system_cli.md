# System commands


## Contents

- [System configuration commands](#system-configuration-commands)
  - [Setting the fan speed](#setting-the-fan-speed)
  - [Unsetting the fan speed](#unsetting-the-fan-speed)
  - [Setting an LED state](#setting-an-led-state)
  - [Unsetting an LED state](#unsetting-an-led-state)
  - [Setting timezone on the switch](#setting-timezone-on-the-switch)
  - [Unsetting timezone on the switch](#unsetting-timezone-on-the-switch)
- [System Display Commands](#system-display-commands)
  - [Showing version information](#showing-version-information)
  - [Showing package information](#showing-package-information)
  - [Showing system information](#showing-system-information)
  - [System fan information](#system-fan-information)
  - [Showing system temperature information](#showing-system-temperature-information)
  - [Showing system LED information](#showing-system-led-information)
  - [Showing system power-supply information](#showing-system-power-supply-information)
  - [Showing system date information](#showing-system-date-information)
  - [Showing system cpu information using top](#showing-system-cpu-information-using-top)
  - [Showing system memory information using top](#showing-system-memory-information-using-top)
  - [Showing timezone information](#showing-timezone-information)


## System configuration commands
### Setting the fan speed
#### Syntax
`fan-speed < normal | slow | medium | fast | maximum >`

#### Description
This command globally sets the fan speed to the value indicated by the command parameter. This command overrides the fan speed set internally by the platform. The fan speed value set by the user takes affect depending on platform cooling requirements.

#### Authority
All users.

#### Parameters
This command takes one of the following values:
- slow
- normal
- medium
- fast

By default fans operate at normal speed.

| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------------|
| *slow* | choose one| Literal | Slow is 25% of maximum speed. |
| *normal* | choose one| Literal | Normal is 40% of maximum speed. |
| *medium* | choose one| Literal | Medium is 65% of maximum speed. |
| *fast* | choose one| Literal | Fast is 80% of maximum speed. |
| *max* | choose one| Literal | Fan speed is at maximum speed. |

#### Examples

```
switch(config)#fan-speed slow
```

### Unsetting the fan speed
#### Syntax
`no fan-speed [< normal | slow | medium | fast | maximum >]`

#### Description
This command removes the configured fan speed, and sets it to the default speed.

#### Authority
All users.

#### Parameters

| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------------|
| *slow* | optional(choose one)| Literal | Slow is 25% of maximum speed. |
| *normal* |optional(choose one)| Literal | Normal is 40% of maximum speed. |
| *medium* | optional(choose one)| Literal | Medium is 65% of maximum speed. |
| *fast* | optional(choose one)| Literal | Fast is 80% of maximum speed. |
| *max* | optional(choose one)| Literal | Fan speed is at maximum speed. |

#### Examples
```
switch(config)#no fan-speed
```

### Setting an LED state
#### Syntax
`led < led-name > < on | flashing | off >`

#### Description
This command sets the LED state to **on**, **off**, or **flashing**. By default, the LED state is off.

#### Authority
All users.

#### Parameters
| Parameter 1| Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *led-name* | Required | Literal |LED name of whose state is to be set |


| Parameter 2| Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *off* | choose one| Literal |Select this to switch off LED |
| *on* | choose one| Literal  | Select this to switch on LED |
| *flashing*| choose one|Literal | Select this to blink/flash the LED|

#### Examples
```
switch(config)#led base-loc on
```

### Unsetting an LED state
#### Syntax
`no led <led-name> [< on | flashing | off >]`

#### Description
This command turns off the LED.

#### Authority
All users.

#### Parameters
| Parameter 1| Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *led-name* | Required | Literal | The LED name whose state is to be set. |


| Parameter 2| Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *off* | Optional(choose one)| Literal | Select this to switch the LED off. |
| *on* | Optional (choose one)| Literal  | Select this to switch the LED on. |
| *flashing*| Optional (choose one)|Literal | Select this to blink/flash the LED. |


#### Examples
```
switch(config)#no led base-loc
```

## System display commands
### Showing version information
#### Syntax
`show version`

#### Description
This command shows the current switch version information. The format of the `show version` output:
```
<name> <version> (Build: <platform>-ops-<X.Y.Z-string>-<branch-name>[-<build-time>][-<meta-string>]
```

| Field Name  | Explanation                                                                                                                          | Example                       |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| name        | Name of the project.                                                                                                                 | OpenSwitch                    |
| version     | Version of the software.                                                                                                             | 0.4.0 or 0.3.0-rc0 etc.       |
| platform    | Platform for which the image is built.                                                                                               | genericx86-64, AS5712, AS6712 |
| ops         | Abbreviation for OpenSwitch.                                                                                                         |                               |
| X.Y.Z-string| The release version tag.                                                                                                             | 0.4.0 or 0.3.0-rc0 etc.       |
| branch-name | Branch where the image is built.                                                                                                     | master, feature, release      |
| build-time  | For periodic builds, the build time-stamp in YYYYMMDDNN format. For developer builds, the build time-stamp in YYYYMMDDHHmmss format. | 2016042606, 20160419204046    |
| meta-string | “dev” is appended to image names when a developer builds an image using “make”.                                                      |                               |

#### Authority
All users.

#### Parameters
No parameters.

#### Examples
```
| Switch Image Build Type                                                 | Show version                                                                |
|-------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| Developer build of OpenSwitch from the master branch for genericx86-64. | OpenSwitch 0.4.0 (Build: genericx86-64-ops-0.4.0-master-20160419204046-dev) |
| Periodic build of OpenSwitch from the master branch for genericx86-64.  | OpenSwitch 0.4.0 (Build: genericx86-64-ops-0.4.0-master+2016042606          |
| Developer build of OpenSwitch from the master branch for AS5712.        | OpenSwitch 0.4.0 (Build: as5712-ops-0.4.0-master-20160419204046-dev)        |
| Periodic build of OpenSwitch from the master branch for AS5712.         | OpenSwitch 0.4.0 (Build: as5712-ops-0.4.0-master+2016042606)                |
| Periodic build of OpenSwitch from the release branch for AS5712.        | OpenSwitch 0.3.0-rc0 (Build: as5712-ops-0.3.0-rc0-release+2016042606)                |
```


### Showing package information
#### Syntax
`show version detail [ops]`

#### Description
This command lists every package present in the switch image under the PACKAGE column. The VERSION column displays the git hash value if the SOURCE URL is a git repository. If not, the VERSION column displays the version string of the package. SOURCE TYPE displays the type of source pointed to by SOURCE URL. SOURCE URL displays the download location for the source-code of the corresponding package in the SOURCE URI column. If version information and/or Source URL is not available during build-time, `show version detail` displays 'NA' (Not Available).

#### Authority
All users.

#### Parameters
No parameters.

| Parameter  | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
|  *ops*   | Optional | Literal | Displays git-hashes for OpenSwitch repos (ops-*) alone. |

#### Examples
```
switch#show version detail
PACKAGE     : kernel-module-gspca-spca1528
VERSION     : 3.14.36+gitAUTOINC+a996d95104_dbe5b52e93
SOURCE TYPE : git
SOURCE URL  : https://git.yoctoproject.org/linux-yocto-3.14.git;bareclone=1;branch=standard/common-pc-64/base,meta;name=machine,meta

PACKAGE     : python-jsonpatch
VERSION     : 1.11
SOURCE TYPE : http
SOURCE URL  : http://pypi.python.org/packages/source/j/jsonpatch/jsonpatch-1.11.tar.gz

PACKAGE     : ops-cli
VERSION     : a70df32190755dabf3fb404c3cde04a03aa6be40~DIRTY
SOURCE TYPE : other
SOURCE URL  : NA

PACKAGE     : dbus-1
VERSION     : NA
SOURCE TYPE : other
SOURCE URL  : NA
```
### Setting timezone on the switch
#### Syntax
`timezone set *TIMEZONE*`

#### Description
This command sets the time zone on the switch. By default the time zone is set to UTC (Coordinated Universal Time).

#### Authority
All users.

#### Parameters
The *TIMEZONE* parameter takes one of the following values as per the posix timezone database:

| Parameter                          | Status    | Syntax  | Description                                      |
|:-----------------------------------|:----------|:-------:|:-------------------------------------------------|
| africa/abidjan                     | Mandatory | Literal | Africa/Abidjan Zone                              |
| africa/accra                       | Mandatory | Literal | Africa/Accra Zone                                |
| africa/addis_ababa                 | Mandatory | Literal | Africa/Addis_Ababa Zone                          |
| africa/algiers                     | Mandatory | Literal | Africa/Algiers Zone                              |
| africa/asmara                      | Mandatory | Literal | Africa/Asmara Zone                               |
| africa/asmera                      | Mandatory | Literal | Africa/Asmera Zone                               |
| africa/bamako                      | Mandatory | Literal | Africa/Bamako Zone                               |
| africa/bangui                      | Mandatory | Literal | Africa/Bangui Zone                               |
| africa/banjul                      | Mandatory | Literal | Africa/Banjul Zone                               |
| africa/bissau                      | Mandatory | Literal | Africa/Bissau Zone                               |
| africa/blantyre                    | Mandatory | Literal | Africa/Blantyre Zone                             |
| africa/brazzaville                 | Mandatory | Literal | Africa/Brazzaville Zone                          |
| africa/bujumbura                   | Mandatory | Literal | Africa/Bujumbura Zone                            |
| africa/cairo                       | Mandatory | Literal | Africa/Cairo Zone                                |
| africa/casablanca                  | Mandatory | Literal | Africa/Casablanca Zone                           |
| africa/ceuta                       | Mandatory | Literal | Africa/Ceuta Zone                                |
| africa/conakry                     | Mandatory | Literal | Africa/Conakry Zone                              |
| africa/dakar                       | Mandatory | Literal | Africa/Dakar Zone                                |
| africa/dar_es_salaam               | Mandatory | Literal | Africa/Dar_es_Salaam Zone                        |
| africa/djibouti                    | Mandatory | Literal | Africa/Djibouti Zone                             |
| africa/douala                      | Mandatory | Literal | Africa/Douala Zone                               |
| africa/el_aaiun                    | Mandatory | Literal | Africa/El_Aaiun Zone                             |
| africa/freetown                    | Mandatory | Literal | Africa/Freetown Zone                             |
| africa/gaborone                    | Mandatory | Literal | Africa/Gaborone Zone                             |
| africa/harare                      | Mandatory | Literal | Africa/Harare Zone                               |
| africa/johannesburg                | Mandatory | Literal | Africa/Johannesburg Zone                         |
| africa/juba                        | Mandatory | Literal | Africa/Juba Zone                                 |
| africa/kampala                     | Mandatory | Literal | Africa/Kampala Zone                              |
| africa/khartoum                    | Mandatory | Literal | Africa/Khartoum Zone                             |
| africa/kigali                      | Mandatory | Literal | Africa/Kigali Zone                               |
| africa/kinshasa                    | Mandatory | Literal | Africa/Kinshasa Zone                             |
| africa/lagos                       | Mandatory | Literal | Africa/Lagos Zone                                |
| africa/libreville                  | Mandatory | Literal | Africa/Libreville Zone                           |
| africa/lome                        | Mandatory | Literal | Africa/Lome Zone                                 |
| africa/luanda                      | Mandatory | Literal | Africa/Luanda Zone                               |
| africa/lubumbashi                  | Mandatory | Literal | Africa/Lubumbashi Zone                           |
| africa/lusaka                      | Mandatory | Literal | Africa/Lusaka Zone                               |
| africa/malabo                      | Mandatory | Literal | Africa/Malabo Zone                               |
| africa/maputo                      | Mandatory | Literal | Africa/Maputo Zone                               |
| africa/maseru                      | Mandatory | Literal | Africa/Maseru Zone                               |
| africa/mbabane                     | Mandatory | Literal | Africa/Mbabane Zone                              |
| africa/mogadishu                   | Mandatory | Literal | Africa/Mogadishu Zone                            |
| africa/monrovia                    | Mandatory | Literal | Africa/Monrovia Zone                             |
| africa/nairobi                     | Mandatory | Literal | Africa/Nairobi Zone                              |
| africa/ndjamena                    | Mandatory | Literal | Africa/Ndjamena Zone                             |
| africa/niamey                      | Mandatory | Literal | Africa/Niamey Zone                               |
| africa/nouakchott                  | Mandatory | Literal | Africa/Nouakchott Zone                           |
| africa/ouagadougou                 | Mandatory | Literal | Africa/Ouagadougou Zone                          |
| africa/porto-novo                  | Mandatory | Literal | Africa/Porto-Novo Zone                           |
| africa/sao_tome                    | Mandatory | Literal | Africa/Sao_Tome Zone                             |
| africa/timbuktu                    | Mandatory | Literal | Africa/Timbuktu Zone                             |
| africa/tripoli                     | Mandatory | Literal | Africa/Tripoli Zone                              |
| africa/tunis                       | Mandatory | Literal | Africa/Tunis Zone                                |
| africa/windhoek                    | Mandatory | Literal | Africa/Windhoek Zone                             |
| america/adak                       | Mandatory | Literal | America/Adak Zone                                |
| america/anchorage                  | Mandatory | Literal | America/Anchorage Zone                           |
| america/anguilla                   | Mandatory | Literal | America/Anguilla Zone                            |
| america/antigua                    | Mandatory | Literal | America/Antigua Zone                             |
| america/araguaina                  | Mandatory | Literal | America/Araguaina Zone                           |
| america/argentina/buenos_aires     | Mandatory | Literal | America/Argentina/Buenos_Aires Zone              |
| america/argentina/catamarca        | Mandatory | Literal | America/Argentina/Catamarca Zone                 |
| america/argentina/comodrivadavia   | Mandatory | Literal | America/Argentina/ComodRivadavia Zone            |
| america/argentina/cordoba          | Mandatory | Literal | America/Argentina/Cordoba Zone                   |
| america/argentina/jujuy            | Mandatory | Literal | America/Argentina/Jujuy Zone                     |
| america/argentina/la_rioja         | Mandatory | Literal | America/Argentina/La_Rioja Zone                  |
| america/argentina/mendoza          | Mandatory | Literal | America/Argentina/Mendoza Zone                   |
| america/argentina/rio_gallegos     | Mandatory | Literal | America/Argentina/Rio_Gallegos Zone              |
| america/argentina/salta            | Mandatory | Literal | America/Argentina/Salta Zone                     |
| america/argentina/san_juan         | Mandatory | Literal | America/Argentina/San_Juan Zone                  |
| america/argentina/san_luis         | Mandatory | Literal | America/Argentina/San_Luis Zone                  |
| america/argentina/tucuman          | Mandatory | Literal | America/Argentina/Tucuman Zone                   |
| america/argentina/ushuaia          | Mandatory | Literal | America/Argentina/Ushuaia Zone                   |
| america/aruba                      | Mandatory | Literal | America/Aruba Zone                               |
| america/asuncion                   | Mandatory | Literal | America/Asuncion Zone                            |
| america/atikokan                   | Mandatory | Literal | America/Atikokan Zone                            |
| america/atka                       | Mandatory | Literal | America/Atka Zone                                |
| america/bahia                      | Mandatory | Literal | America/Bahia Zone                               |
| america/bahia_banderas             | Mandatory | Literal | America/Bahia_Banderas Zone                      |
| america/barbados                   | Mandatory | Literal | America/Barbados Zone                            |
| america/belem                      | Mandatory | Literal | America/Belem Zone                               |
| america/belize                     | Mandatory | Literal | America/Belize Zone                              |
| america/blanc-sablon               | Mandatory | Literal | America/Blanc-Sablon Zone                        |
| america/boa_vista                  | Mandatory | Literal | America/Boa_Vista Zone                           |
| america/bogota                     | Mandatory | Literal | America/Bogota Zone                              |
| america/boise                      | Mandatory | Literal | America/Boise Zone                               |
| america/buenos_aires               | Mandatory | Literal | America/Buenos_Aires Zone                        |
| america/cambridge_bay              | Mandatory | Literal | America/Cambridge_Bay Zone                       |
| america/campo_grande               | Mandatory | Literal | America/Campo_Grande Zone                        |
| america/cancun                     | Mandatory | Literal | America/Cancun Zone                              |
| america/caracas                    | Mandatory | Literal | America/Caracas Zone                             |
| america/catamarca                  | Mandatory | Literal | America/Catamarca Zone                           |
| america/cayenne                    | Mandatory | Literal | America/Cayenne Zone                             |
| america/cayman                     | Mandatory | Literal | America/Cayman Zone                              |
| america/chicago                    | Mandatory | Literal | America/Chicago Zone                             |
| america/chihuahua                  | Mandatory | Literal | America/Chihuahua Zone                           |
| america/coral_harbour              | Mandatory | Literal | America/Coral_Harbour Zone                       |
| america/cordoba                    | Mandatory | Literal | America/Cordoba Zone                             |
| america/costa_rica                 | Mandatory | Literal | America/Costa_Rica Zone                          |
| america/creston                    | Mandatory | Literal | America/Creston Zone                             |
| america/cuiaba                     | Mandatory | Literal | America/Cuiaba Zone                              |
| america/curacao                    | Mandatory | Literal | America/Curacao Zone                             |
| america/danmarkshavn               | Mandatory | Literal | America/Danmarkshavn Zone                        |
| america/dawson                     | Mandatory | Literal | America/Dawson Zone                              |
| america/dawson_creek               | Mandatory | Literal | America/Dawson_Creek Zone                        |
| america/denver                     | Mandatory | Literal | America/Denver Zone                              |
| america/detroit                    | Mandatory | Literal | America/Detroit Zone                             |
| america/dominica                   | Mandatory | Literal | America/Dominica Zone                            |
| america/edmonton                   | Mandatory | Literal | America/Edmonton Zone                            |
| america/eirunepe                   | Mandatory | Literal | America/Eirunepe Zone                            |
| america/el_salvador                | Mandatory | Literal | America/El_Salvador Zone                         |
| america/ensenada                   | Mandatory | Literal | America/Ensenada Zone                            |
| america/fort_wayne                 | Mandatory | Literal | America/Fort_Wayne Zone                          |
| america/fortaleza                  | Mandatory | Literal | America/Fortaleza Zone                           |
| america/glace_bay                  | Mandatory | Literal | America/Glace_Bay Zone                           |
| america/godthab                    | Mandatory | Literal | America/Godthab Zone                             |
| america/goose_bay                  | Mandatory | Literal | America/Goose_Bay Zone                           |
| america/grand_turk                 | Mandatory | Literal | America/Grand_Turk Zone                          |
| america/grenada                    | Mandatory | Literal | America/Grenada Zone                             |
| america/guadeloupe                 | Mandatory | Literal | America/Guadeloupe Zone                          |
| america/guatemala                  | Mandatory | Literal | America/Guatemala Zone                           |
| america/guayaquil                  | Mandatory | Literal | America/Guayaquil Zone                           |
| america/guyana                     | Mandatory | Literal | America/Guyana Zone                              |
| america/halifax                    | Mandatory | Literal | America/Halifax Zone                             |
| america/havana                     | Mandatory | Literal | America/Havana Zone                              |
| america/hermosillo                 | Mandatory | Literal | America/Hermosillo Zone                          |
| america/indiana/indianapolis       | Mandatory | Literal | America/Indiana/Indianapolis Zone                |
| america/indiana/knox               | Mandatory | Literal | America/Indiana/Knox Zone                        |
| america/indiana/marengo            | Mandatory | Literal | America/Indiana/Marengo Zone                     |
| america/indiana/petersburg         | Mandatory | Literal | America/Indiana/Petersburg Zone                  |
| america/indiana/tell_city          | Mandatory | Literal | America/Indiana/Tell_City Zone                   |
| america/indiana/vevay              | Mandatory | Literal | America/Indiana/Vevay Zone                       |
| america/indiana/vincennes          | Mandatory | Literal | America/Indiana/Vincennes Zone                   |
| america/indiana/winamac            | Mandatory | Literal | America/Indiana/Winamac Zone                     |
| america/indianapolis               | Mandatory | Literal | America/Indianapolis Zone                        |
| america/inuvik                     | Mandatory | Literal | America/Inuvik Zone                              |
| america/iqaluit                    | Mandatory | Literal | America/Iqaluit Zone                             |
| america/jamaica                    | Mandatory | Literal | America/Jamaica Zone                             |
| america/jujuy                      | Mandatory | Literal | America/Jujuy Zone                               |
| america/juneau                     | Mandatory | Literal | America/Juneau Zone                              |
| america/kentucky/louisville        | Mandatory | Literal | America/Kentucky/Louisville Zone                 |
| america/kentucky/monticello        | Mandatory | Literal | America/Kentucky/Monticello Zone                 |
| america/knox_in                    | Mandatory | Literal | America/Knox_IN Zone                             |
| america/kralendijk                 | Mandatory | Literal | America/Kralendijk Zone                          |
| america/la_paz                     | Mandatory | Literal | America/La_Paz Zone                              |
| america/lima                       | Mandatory | Literal | America/Lima Zone                                |
| america/los_angeles                | Mandatory | Literal | America/Los_Angeles Zone                         |
| america/louisville                 | Mandatory | Literal | America/Louisville Zone                          |
| america/lower_princes              | Mandatory | Literal | America/Lower_Princes Zone                       |
| america/maceio                     | Mandatory | Literal | America/Maceio Zone                              |
| america/managua                    | Mandatory | Literal | America/Managua Zone                             |
| america/manaus                     | Mandatory | Literal | America/Manaus Zone                              |
| america/marigot                    | Mandatory | Literal | America/Marigot Zone                             |
| america/martinique                 | Mandatory | Literal | America/Martinique Zone                          |
| america/matamoros                  | Mandatory | Literal | America/Matamoros Zone                           |
| america/mazatlan                   | Mandatory | Literal | America/Mazatlan Zone                            |
| america/mendoza                    | Mandatory | Literal | America/Mendoza Zone                             |
| america/menominee                  | Mandatory | Literal | America/Menominee Zone                           |
| america/merida                     | Mandatory | Literal | America/Merida Zone                              |
| america/metlakatla                 | Mandatory | Literal | America/Metlakatla Zone                          |
| america/mexico_city                | Mandatory | Literal | America/Mexico_City Zone                         |
| america/miquelon                   | Mandatory | Literal | America/Miquelon Zone                            |
| america/moncton                    | Mandatory | Literal | America/Moncton Zone                             |
| america/monterrey                  | Mandatory | Literal | America/Monterrey Zone                           |
| america/montevideo                 | Mandatory | Literal | America/Montevideo Zone                          |
| america/montreal                   | Mandatory | Literal | America/Montreal Zone                            |
| america/montserrat                 | Mandatory | Literal | America/Montserrat Zone                          |
| america/nassau                     | Mandatory | Literal | America/Nassau Zone                              |
| america/new_york                   | Mandatory | Literal | America/New_York Zone                            |
| america/nipigon                    | Mandatory | Literal | America/Nipigon Zone                             |
| america/nome                       | Mandatory | Literal | America/Nome Zone                                |
| america/noronha                    | Mandatory | Literal | America/Noronha Zone                             |
| america/north_dakota/beulah        | Mandatory | Literal | America/North_Dakota/Beulah Zone                 |
| america/north_dakota/center        | Mandatory | Literal | America/North_Dakota/Center Zone                 |
| america/north_dakota/new_salem     | Mandatory | Literal | America/North_Dakota/New_Salem Zone              |
| america/ojinaga                    | Mandatory | Literal | America/Ojinaga Zone                             |
| america/panama                     | Mandatory | Literal | America/Panama Zone                              |
| america/pangnirtung                | Mandatory | Literal | America/Pangnirtung Zone                         |
| america/paramaribo                 | Mandatory | Literal | America/Paramaribo Zone                          |
| america/phoenix                    | Mandatory | Literal | America/Phoenix Zone                             |
| america/port-au-prince             | Mandatory | Literal | America/Port-au-Prince Zone                      |
| america/port_of_spain              | Mandatory | Literal | America/Port_of_Spain Zone                       |
| america/porto_acre                 | Mandatory | Literal | America/Porto_Acre Zone                          |
| america/porto_velho                | Mandatory | Literal | America/Porto_Velho Zone                         |
| america/puerto_rico                | Mandatory | Literal | America/Puerto_Rico Zone                         |
| america/rainy_river                | Mandatory | Literal | America/Rainy_River Zone                         |
| america/rankin_inlet               | Mandatory | Literal | America/Rankin_Inlet Zone                        |
| america/recife                     | Mandatory | Literal | America/Recife Zone                              |
| america/regina                     | Mandatory | Literal | America/Regina Zone                              |
| america/resolute                   | Mandatory | Literal | America/Resolute Zone                            |
| america/rio_branco                 | Mandatory | Literal | America/Rio_Branco Zone                          |
| america/rosario                    | Mandatory | Literal | America/Rosario Zone                             |
| america/santa_isabel               | Mandatory | Literal | America/Santa_Isabel Zone                        |
| america/santarem                   | Mandatory | Literal | America/Santarem Zone                            |
| america/santiago                   | Mandatory | Literal | America/Santiago Zone                            |
| america/santo_domingo              | Mandatory | Literal | America/Santo_Domingo Zone                       |
| america/sao_paulo                  | Mandatory | Literal | America/Sao_Paulo Zone                           |
| america/scoresbysund               | Mandatory | Literal | America/Scoresbysund Zone                        |
| america/shiprock                   | Mandatory | Literal | America/Shiprock Zone                            |
| america/sitka                      | Mandatory | Literal | America/Sitka Zone                               |
| america/st_barthelemy              | Mandatory | Literal | America/St_Barthelemy Zone                       |
| america/st_johns                   | Mandatory | Literal | America/St_Johns Zone                            |
| america/st_kitts                   | Mandatory | Literal | America/St_Kitts Zone                            |
| america/st_lucia                   | Mandatory | Literal | America/St_Lucia Zone                            |
| america/st_thomas                  | Mandatory | Literal | America/St_Thomas Zone                           |
| america/st_vincent                 | Mandatory | Literal | America/St_Vincent Zone                          |
| america/swift_current              | Mandatory | Literal | America/Swift_Current Zone                       |
| america/tegucigalpa                | Mandatory | Literal | America/Tegucigalpa Zone                         |
| america/thule                      | Mandatory | Literal | America/Thule Zone                               |
| america/thunder_bay                | Mandatory | Literal | America/Thunder_Bay Zone                         |
| america/tijuana                    | Mandatory | Literal | America/Tijuana Zone                             |
| america/toronto                    | Mandatory | Literal | America/Toronto Zone                             |
| america/tortola                    | Mandatory | Literal | America/Tortola Zone                             |
| america/vancouver                  | Mandatory | Literal | America/Vancouver Zone                           |
| america/virgin                     | Mandatory | Literal | America/Virgin Zone                              |
| america/whitehorse                 | Mandatory | Literal | America/Whitehorse Zone                          |
| america/winnipeg                   | Mandatory | Literal | America/Winnipeg Zone                            |
| america/yakutat                    | Mandatory | Literal | America/Yakutat Zone                             |
| america/yellowknife                | Mandatory | Literal | America/Yellowknife Zone                         |
| antarctica/casey                   | Mandatory | Literal | Antarctica/Casey Zone                            |
| antarctica/davis                   | Mandatory | Literal | Antarctica/Davis Zone                            |
| antarctica/dumontdurville          | Mandatory | Literal | Antarctica/DumontDUrville Zone                   |
| antarctica/macquarie               | Mandatory | Literal | Antarctica/Macquarie Zone                        |
| antarctica/mawson                  | Mandatory | Literal | Antarctica/Mawson Zone                           |
| antarctica/mcmurdo                 | Mandatory | Literal | Antarctica/McMurdo Zone                          |
| antarctica/palmer                  | Mandatory | Literal | Antarctica/Palmer Zone                           |
| antarctica/rothera                 | Mandatory | Literal | Antarctica/Rothera Zone                          |
| antarctica/south_pole              | Mandatory | Literal | Antarctica/South_Pole Zone                       |
| antarctica/syowa                   | Mandatory | Literal | Antarctica/Syowa Zone                            |
| antarctica/troll                   | Mandatory | Literal | Antarctica/Troll Zone                            |
| antarctica/vostok                  | Mandatory | Literal | Antarctica/Vostok Zone                           |
| arctic/longyearbyen                | Mandatory | Literal | Arctic/Longyearbyen Zone                         |
| asia/aden                          | Mandatory | Literal | Asia/Aden Zone                                   |
| asia/almaty                        | Mandatory | Literal | Asia/Almaty Zone                                 |
| asia/amman                         | Mandatory | Literal | Asia/Amman Zone                                  |
| asia/anadyr                        | Mandatory | Literal | Asia/Anadyr Zone                                 |
| asia/aqtau                         | Mandatory | Literal | Asia/Aqtau Zone                                  |
| asia/aqtobe                        | Mandatory | Literal | Asia/Aqtobe Zone                                 |
| asia/ashgabat                      | Mandatory | Literal | Asia/Ashgabat Zone                               |
| asia/ashkhabad                     | Mandatory | Literal | Asia/Ashkhabad Zone                              |
| asia/baghdad                       | Mandatory | Literal | Asia/Baghdad Zone                                |
| asia/bahrain                       | Mandatory | Literal | Asia/Bahrain Zone                                |
| asia/baku                          | Mandatory | Literal | Asia/Baku Zone                                   |
| asia/bangkok                       | Mandatory | Literal | Asia/Bangkok Zone                                |
| asia/beirut                        | Mandatory | Literal | Asia/Beirut Zone                                 |
| asia/bishkek                       | Mandatory | Literal | Asia/Bishkek Zone                                |
| asia/brunei                        | Mandatory | Literal | Asia/Brunei Zone                                 |
| asia/calcutta                      | Mandatory | Literal | Asia/Calcutta Zone                               |
| asia/chita                         | Mandatory | Literal | Asia/Chita Zone                                  |
| asia/choibalsan                    | Mandatory | Literal | Asia/Choibalsan Zone                             |
| asia/chongqing                     | Mandatory | Literal | Asia/Chongqing Zone                              |
| asia/chungking                     | Mandatory | Literal | Asia/Chungking Zone                              |
| asia/colombo                       | Mandatory | Literal | Asia/Colombo Zone                                |
| asia/dacca                         | Mandatory | Literal | Asia/Dacca Zone                                  |
| asia/damascus                      | Mandatory | Literal | Asia/Damascus Zone                               |
| asia/dhaka                         | Mandatory | Literal | Asia/Dhaka Zone                                  |
| asia/dili                          | Mandatory | Literal | Asia/Dili Zone                                   |
| asia/dubai                         | Mandatory | Literal | Asia/Dubai Zone                                  |
| asia/dushanbe                      | Mandatory | Literal | Asia/Dushanbe Zone                               |
| asia/gaza                          | Mandatory | Literal | Asia/Gaza Zone                                   |
| asia/harbin                        | Mandatory | Literal | Asia/Harbin Zone                                 |
| asia/hebron                        | Mandatory | Literal | Asia/Hebron Zone                                 |
| asia/ho_chi_minh                   | Mandatory | Literal | Asia/Ho_Chi_Minh Zone                            |
| asia/hong_kong                     | Mandatory | Literal | Asia/Hong_Kong Zone                              |
| asia/hovd                          | Mandatory | Literal | Asia/Hovd Zone                                   |
| asia/irkutsk                       | Mandatory | Literal | Asia/Irkutsk Zone                                |
| asia/istanbul                      | Mandatory | Literal | Asia/Istanbul Zone                               |
| asia/jakarta                       | Mandatory | Literal | Asia/Jakarta Zone                                |
| asia/jayapura                      | Mandatory | Literal | Asia/Jayapura Zone                               |
| asia/jerusalem                     | Mandatory | Literal | Asia/Jerusalem Zone                              |
| asia/kabul                         | Mandatory | Literal | Asia/Kabul Zone                                  |
| asia/kamchatka                     | Mandatory | Literal | Asia/Kamchatka Zone                              |
| asia/karachi                       | Mandatory | Literal | Asia/Karachi Zone                                |
| asia/kashgar                       | Mandatory | Literal | Asia/Kashgar Zone                                |
| asia/kathmandu                     | Mandatory | Literal | Asia/Kathmandu Zone                              |
| asia/katmandu                      | Mandatory | Literal | Asia/Katmandu Zone                               |
| asia/khandyga                      | Mandatory | Literal | Asia/Khandyga Zone                               |
| asia/kolkata                       | Mandatory | Literal | Asia/Kolkata Zone                                |
| asia/krasnoyarsk                   | Mandatory | Literal | Asia/Krasnoyarsk Zone                            |
| asia/kuala_lumpur                  | Mandatory | Literal | Asia/Kuala_Lumpur Zone                           |
| asia/kuching                       | Mandatory | Literal | Asia/Kuching Zone                                |
| asia/kuwait                        | Mandatory | Literal | Asia/Kuwait Zone                                 |
| asia/macao                         | Mandatory | Literal | Asia/Macao Zone                                  |
| asia/macau                         | Mandatory | Literal | Asia/Macau Zone                                  |
| asia/magadan                       | Mandatory | Literal | Asia/Magadan Zone                                |
| asia/makassar                      | Mandatory | Literal | Asia/Makassar Zone                               |
| asia/manila                        | Mandatory | Literal | Asia/Manila Zone                                 |
| asia/muscat                        | Mandatory | Literal | Asia/Muscat Zone                                 |
| asia/nicosia                       | Mandatory | Literal | Asia/Nicosia Zone                                |
| asia/novokuznetsk                  | Mandatory | Literal | Asia/Novokuznetsk Zone                           |
| asia/novosibirsk                   | Mandatory | Literal | Asia/Novosibirsk Zone                            |
| asia/omsk                          | Mandatory | Literal | Asia/Omsk Zone                                   |
| asia/oral                          | Mandatory | Literal | Asia/Oral Zone                                   |
| asia/phnom_penh                    | Mandatory | Literal | Asia/Phnom_Penh Zone                             |
| asia/pontianak                     | Mandatory | Literal | Asia/Pontianak Zone                              |
| asia/pyongyang                     | Mandatory | Literal | Asia/Pyongyang Zone                              |
| asia/qatar                         | Mandatory | Literal | Asia/Qatar Zone                                  |
| asia/qyzylorda                     | Mandatory | Literal | Asia/Qyzylorda Zone                              |
| asia/rangoon                       | Mandatory | Literal | Asia/Rangoon Zone                                |
| asia/riyadh                        | Mandatory | Literal | Asia/Riyadh Zone                                 |
| asia/saigon                        | Mandatory | Literal | Asia/Saigon Zone                                 |
| asia/sakhalin                      | Mandatory | Literal | Asia/Sakhalin Zone                               |
| asia/samarkand                     | Mandatory | Literal | Asia/Samarkand Zone                              |
| asia/seoul                         | Mandatory | Literal | Asia/Seoul Zone                                  |
| asia/shanghai                      | Mandatory | Literal | Asia/Shanghai Zone                               |
| asia/singapore                     | Mandatory | Literal | Asia/Singapore Zone                              |
| asia/srednekolymsk                 | Mandatory | Literal | Asia/Srednekolymsk Zone                          |
| asia/taipei                        | Mandatory | Literal | Asia/Taipei Zone                                 |
| asia/tashkent                      | Mandatory | Literal | Asia/Tashkent Zone                               |
| asia/tbilisi                       | Mandatory | Literal | Asia/Tbilisi Zone                                |
| asia/tehran                        | Mandatory | Literal | Asia/Tehran Zone                                 |
| asia/tel_aviv                      | Mandatory | Literal | Asia/Tel_Aviv Zone                               |
| asia/thimbu                        | Mandatory | Literal | Asia/Thimbu Zone                                 |
| asia/thimphu                       | Mandatory | Literal | Asia/Thimphu Zone                                |
| asia/tokyo                         | Mandatory | Literal | Asia/Tokyo Zone                                  |
| asia/ujung_pandang                 | Mandatory | Literal | Asia/Ujung_Pandang Zone                          |
| asia/ulaanbaatar                   | Mandatory | Literal | Asia/Ulaanbaatar Zone                            |
| asia/ulan_bator                    | Mandatory | Literal | Asia/Ulan_Bator Zone                             |
| asia/urumqi                        | Mandatory | Literal | Asia/Urumqi Zone                                 |
| asia/ust-nera                      | Mandatory | Literal | Asia/Ust-Nera Zone                               |
| asia/vientiane                     | Mandatory | Literal | Asia/Vientiane Zone                              |
| asia/vladivostok                   | Mandatory | Literal | Asia/Vladivostok Zone                            |
| asia/yakutsk                       | Mandatory | Literal | Asia/Yakutsk Zone                                |
| asia/yekaterinburg                 | Mandatory | Literal | Asia/Yekaterinburg Zone                          |
| asia/yerevan                       | Mandatory | Literal | Asia/Yerevan Zone                                |
| atlantic/azores                    | Mandatory | Literal | Atlantic/Azores Zone                             |
| atlantic/bermuda                   | Mandatory | Literal | Atlantic/Bermuda Zone                            |
| atlantic/canary                    | Mandatory | Literal | Atlantic/Canary Zone                             |
| atlantic/cape_verde                | Mandatory | Literal | Atlantic/Cape_Verde Zone                         |
| atlantic/faeroe                    | Mandatory | Literal | Atlantic/Faeroe Zone                             |
| atlantic/faroe                     | Mandatory | Literal | Atlantic/Faroe Zone                              |
| atlantic/jan_mayen                 | Mandatory | Literal | Atlantic/Jan_Mayen Zone                          |
| atlantic/madeira                   | Mandatory | Literal | Atlantic/Madeira Zone                            |
| atlantic/reykjavik                 | Mandatory | Literal | Atlantic/Reykjavik Zone                          |
| atlantic/south_georgia             | Mandatory | Literal | Atlantic/South_Georgia Zone                      |
| atlantic/st_helena                 | Mandatory | Literal | Atlantic/St_Helena Zone                          |
| atlantic/stanley                   | Mandatory | Literal | Atlantic/Stanley Zone                            |
| australia/act                      | Mandatory | Literal | Australia/ACT Zone                               |
| australia/adelaide                 | Mandatory | Literal | Australia/Adelaide Zone                          |
| australia/brisbane                 | Mandatory | Literal | Australia/Brisbane Zone                          |
| australia/broken_hill              | Mandatory | Literal | Australia/Broken_Hill Zone                       |
| australia/canberra                 | Mandatory | Literal | Australia/Canberra Zone                          |
| australia/currie                   | Mandatory | Literal | Australia/Currie Zone                            |
| australia/darwin                   | Mandatory | Literal | Australia/Darwin Zone                            |
| australia/eucla                    | Mandatory | Literal | Australia/Eucla Zone                             |
| australia/hobart                   | Mandatory | Literal | Australia/Hobart Zone                            |
| australia/lhi                      | Mandatory | Literal | Australia/LHI Zone                               |
| australia/lindeman                 | Mandatory | Literal | Australia/Lindeman Zone                          |
| australia/lord_howe                | Mandatory | Literal | Australia/Lord_Howe Zone                         |
| australia/melbourne                | Mandatory | Literal | Australia/Melbourne Zone                         |
| australia/nsw                      | Mandatory | Literal | Australia/NSW Zone                               |
| australia/north                    | Mandatory | Literal | Australia/North Zone                             |
| australia/perth                    | Mandatory | Literal | Australia/Perth Zone                             |
| australia/queensland               | Mandatory | Literal | Australia/Queensland Zone                        |
| australia/south                    | Mandatory | Literal | Australia/South Zone                             |
| australia/sydney                   | Mandatory | Literal | Australia/Sydney Zone                            |
| australia/tasmania                 | Mandatory | Literal | Australia/Tasmania Zone                          |
| australia/victoria                 | Mandatory | Literal | Australia/Victoria Zone                          |
| australia/west                     | Mandatory | Literal | Australia/West Zone                              |
| australia/yancowinna               | Mandatory | Literal | Australia/Yancowinna Zone                        |
| brazil/acre                        | Mandatory | Literal | Brazil/Acre Zone                                 |
| brazil/denoronha                   | Mandatory | Literal | Brazil/DeNoronha Zone                            |
| brazil/east                        | Mandatory | Literal | Brazil/East Zone                                 |
| brazil/west                        | Mandatory | Literal | Brazil/West Zone                                 |
| cet                                | Mandatory | Literal | CET Zone                                         |
| cst6cdt                            | Mandatory | Literal | CST6CDT Zone                                     |
| canada/atlantic                    | Mandatory | Literal | Canada/Atlantic Zone                             |
| canada/central                     | Mandatory | Literal | Canada/Central Zone                              |
| canada/east-saskatchewan           | Mandatory | Literal | Canada/East-Saskatchewan Zone                    |
| canada/eastern                     | Mandatory | Literal | Canada/Eastern Zone                              |
| canada/mountain                    | Mandatory | Literal | Canada/Mountain Zone                             |
| canada/newfoundland                | Mandatory | Literal | Canada/Newfoundland Zone                         |
| canada/pacific                     | Mandatory | Literal | Canada/Pacific Zone                              |
| canada/saskatchewan                | Mandatory | Literal | Canada/Saskatchewan Zone                         |
| canada/yukon                       | Mandatory | Literal | Canada/Yukon Zone                                |
| chile/continental                  | Mandatory | Literal | Chile/Continental Zone                           |
| chile/easterisland                 | Mandatory | Literal | Chile/EasterIsland Zone                          |
| cuba                               | Mandatory | Literal | Cuba Zone                                        |
| eet                                | Mandatory | Literal | EET Zone                                         |
| est                                | Mandatory | Literal | EST Zone                                         |
| est5edt                            | Mandatory | Literal | EST5EDT Zone                                     |
| egypt                              | Mandatory | Literal | Egypt Zone                                       |
| eire                               | Mandatory | Literal | Eire Zone                                        |
| etc/gmt                            | Mandatory | Literal | Etc/GMT Zone                                     |
| etc/gmt+0                          | Mandatory | Literal | Etc/GMT+0 Zone                                   |
| etc/gmt+1                          | Mandatory | Literal | Etc/GMT+1 Zone                                   |
| etc/gmt+10                         | Mandatory | Literal | Etc/GMT+10 Zone                                  |
| etc/gmt+11                         | Mandatory | Literal | Etc/GMT+11 Zone                                  |
| etc/gmt+12                         | Mandatory | Literal | Etc/GMT+12 Zone                                  |
| etc/gmt+2                          | Mandatory | Literal | Etc/GMT+2 Zone                                   |
| etc/gmt+3                          | Mandatory | Literal | Etc/GMT+3 Zone                                   |
| etc/gmt+4                          | Mandatory | Literal | Etc/GMT+4 Zone                                   |
| etc/gmt+5                          | Mandatory | Literal | Etc/GMT+5 Zone                                   |
| etc/gmt+6                          | Mandatory | Literal | Etc/GMT+6 Zone                                   |
| etc/gmt+7                          | Mandatory | Literal | Etc/GMT+7 Zone                                   |
| etc/gmt+8                          | Mandatory | Literal | Etc/GMT+8 Zone                                   |
| etc/gmt+9                          | Mandatory | Literal | Etc/GMT+9 Zone                                   |
| etc/gmt-0                          | Mandatory | Literal | Etc/GMT-0 Zone                                   |
| etc/gmt-1                          | Mandatory | Literal | Etc/GMT-1 Zone                                   |
| etc/gmt-10                         | Mandatory | Literal | Etc/GMT-10 Zone                                  |
| etc/gmt-11                         | Mandatory | Literal | Etc/GMT-11 Zone                                  |
| etc/gmt-12                         | Mandatory | Literal | Etc/GMT-12 Zone                                  |
| etc/gmt-13                         | Mandatory | Literal | Etc/GMT-13 Zone                                  |
| etc/gmt-14                         | Mandatory | Literal | Etc/GMT-14 Zone                                  |
| etc/gmt-2                          | Mandatory | Literal | Etc/GMT-2 Zone                                   |
| etc/gmt-3                          | Mandatory | Literal | Etc/GMT-3 Zone                                   |
| etc/gmt-4                          | Mandatory | Literal | Etc/GMT-4 Zone                                   |
| etc/gmt-5                          | Mandatory | Literal | Etc/GMT-5 Zone                                   |
| etc/gmt-6                          | Mandatory | Literal | Etc/GMT-6 Zone                                   |
| etc/gmt-7                          | Mandatory | Literal | Etc/GMT-7 Zone                                   |
| etc/gmt-8                          | Mandatory | Literal | Etc/GMT-8 Zone                                   |
| etc/gmt-9                          | Mandatory | Literal | Etc/GMT-9 Zone                                   |
| etc/gmt0                           | Mandatory | Literal | Etc/GMT0 Zone                                    |
| etc/greenwich                      | Mandatory | Literal | Etc/Greenwich Zone                               |
| etc/uct                            | Mandatory | Literal | Etc/UCT Zone                                     |
| etc/utc                            | Mandatory | Literal | Etc/UTC Zone                                     |
| etc/universal                      | Mandatory | Literal | Etc/Universal Zone                               |
| etc/zulu                           | Mandatory | Literal | Etc/Zulu Zone                                    |
| europe/amsterdam                   | Mandatory | Literal | Europe/Amsterdam Zone                            |
| europe/andorra                     | Mandatory | Literal | Europe/Andorra Zone                              |
| europe/athens                      | Mandatory | Literal | Europe/Athens Zone                               |
| europe/belfast                     | Mandatory | Literal | Europe/Belfast Zone                              |
| europe/belgrade                    | Mandatory | Literal | Europe/Belgrade Zone                             |
| europe/berlin                      | Mandatory | Literal | Europe/Berlin Zone                               |
| europe/bratislava                  | Mandatory | Literal | Europe/Bratislava Zone                           |
| europe/brussels                    | Mandatory | Literal | Europe/Brussels Zone                             |
| europe/bucharest                   | Mandatory | Literal | Europe/Bucharest Zone                            |
| europe/budapest                    | Mandatory | Literal | Europe/Budapest Zone                             |
| europe/busingen                    | Mandatory | Literal | Europe/Busingen Zone                             |
| europe/chisinau                    | Mandatory | Literal | Europe/Chisinau Zone                             |
| europe/copenhagen                  | Mandatory | Literal | Europe/Copenhagen Zone                           |
| europe/dublin                      | Mandatory | Literal | Europe/Dublin Zone                               |
| europe/gibraltar                   | Mandatory | Literal | Europe/Gibraltar Zone                            |
| europe/guernsey                    | Mandatory | Literal | Europe/Guernsey Zone                             |
| europe/helsinki                    | Mandatory | Literal | Europe/Helsinki Zone                             |
| europe/isle_of_man                 | Mandatory | Literal | Europe/Isle_of_Man Zone                          |
| europe/istanbul                    | Mandatory | Literal | Europe/Istanbul Zone                             |
| europe/jersey                      | Mandatory | Literal | Europe/Jersey Zone                               |
| europe/kaliningrad                 | Mandatory | Literal | Europe/Kaliningrad Zone                          |
| europe/kiev                        | Mandatory | Literal | Europe/Kiev Zone                                 |
| europe/lisbon                      | Mandatory | Literal | Europe/Lisbon Zone                               |
| europe/ljubljana                   | Mandatory | Literal | Europe/Ljubljana Zone                            |
| europe/london                      | Mandatory | Literal | Europe/London Zone                               |
| europe/luxembourg                  | Mandatory | Literal | Europe/Luxembourg Zone                           |
| europe/madrid                      | Mandatory | Literal | Europe/Madrid Zone                               |
| europe/malta                       | Mandatory | Literal | Europe/Malta Zone                                |
| europe/mariehamn                   | Mandatory | Literal | Europe/Mariehamn Zone                            |
| europe/minsk                       | Mandatory | Literal | Europe/Minsk Zone                                |
| europe/monaco                      | Mandatory | Literal | Europe/Monaco Zone                               |
| europe/moscow                      | Mandatory | Literal | Europe/Moscow Zone                               |
| europe/nicosia                     | Mandatory | Literal | Europe/Nicosia Zone                              |
| europe/oslo                        | Mandatory | Literal | Europe/Oslo Zone                                 |
| europe/paris                       | Mandatory | Literal | Europe/Paris Zone                                |
| europe/podgorica                   | Mandatory | Literal | Europe/Podgorica Zone                            |
| europe/prague                      | Mandatory | Literal | Europe/Prague Zone                               |
| europe/riga                        | Mandatory | Literal | Europe/Riga Zone                                 |
| europe/rome                        | Mandatory | Literal | Europe/Rome Zone                                 |
| europe/samara                      | Mandatory | Literal | Europe/Samara Zone                               |
| europe/san_marino                  | Mandatory | Literal | Europe/San_Marino Zone                           |
| europe/sarajevo                    | Mandatory | Literal | Europe/Sarajevo Zone                             |
| europe/simferopol                  | Mandatory | Literal | Europe/Simferopol Zone                           |
| europe/skopje                      | Mandatory | Literal | Europe/Skopje Zone                               |
| europe/sofia                       | Mandatory | Literal | Europe/Sofia Zone                                |
| europe/stockholm                   | Mandatory | Literal | Europe/Stockholm Zone                            |
| europe/tallinn                     | Mandatory | Literal | Europe/Tallinn Zone                              |
| europe/tirane                      | Mandatory | Literal | Europe/Tirane Zone                               |
| europe/tiraspol                    | Mandatory | Literal | Europe/Tiraspol Zone                             |
| europe/uzhgorod                    | Mandatory | Literal | Europe/Uzhgorod Zone                             |
| europe/vaduz                       | Mandatory | Literal | Europe/Vaduz Zone                                |
| europe/vatican                     | Mandatory | Literal | Europe/Vatican Zone                              |
| europe/vienna                      | Mandatory | Literal | Europe/Vienna Zone                               |
| europe/vilnius                     | Mandatory | Literal | Europe/Vilnius Zone                              |
| europe/volgograd                   | Mandatory | Literal | Europe/Volgograd Zone                            |
| europe/warsaw                      | Mandatory | Literal | Europe/Warsaw Zone                               |
| europe/zagreb                      | Mandatory | Literal | Europe/Zagreb Zone                               |
| europe/zaporozhye                  | Mandatory | Literal | Europe/Zaporozhye Zone                           |
| europe/zurich                      | Mandatory | Literal | Europe/Zurich Zone                               |
| factory                            | Mandatory | Literal | Factory Zone                                     |
| gb                                 | Mandatory | Literal | GB Zone                                          |
| gb-eire                            | Mandatory | Literal | GB-Eire Zone                                     |
| gmt                                | Mandatory | Literal | GMT Zone                                         |
| gmt+0                              | Mandatory | Literal | GMT+0 Zone                                       |
| gmt-0                              | Mandatory | Literal | GMT-0 Zone                                       |
| gmt0                               | Mandatory | Literal | GMT0 Zone                                        |
| greenwich                          | Mandatory | Literal | Greenwich Zone                                   |
| hst                                | Mandatory | Literal | HST Zone                                         |
| hongkong                           | Mandatory | Literal | Hongkong Zone                                    |
| iceland                            | Mandatory | Literal | Iceland Zone                                     |
| indian/antananarivo                | Mandatory | Literal | Indian/Antananarivo Zone                         |
| indian/chagos                      | Mandatory | Literal | Indian/Chagos Zone                               |
| indian/christmas                   | Mandatory | Literal | Indian/Christmas Zone                            |
| indian/cocos                       | Mandatory | Literal | Indian/Cocos Zone                                |
| indian/comoro                      | Mandatory | Literal | Indian/Comoro Zone                               |
| indian/kerguelen                   | Mandatory | Literal | Indian/Kerguelen Zone                            |
| indian/mahe                        | Mandatory | Literal | Indian/Mahe Zone                                 |
| indian/maldives                    | Mandatory | Literal | Indian/Maldives Zone                             |
| indian/mauritius                   | Mandatory | Literal | Indian/Mauritius Zone                            |
| indian/mayotte                     | Mandatory | Literal | Indian/Mayotte Zone                              |
| indian/reunion                     | Mandatory | Literal | Indian/Reunion Zone                              |
| iran                               | Mandatory | Literal | Iran Zone                                        |
| israel                             | Mandatory | Literal | Israel Zone                                      |
| jamaica                            | Mandatory | Literal | Jamaica Zone                                     |
| japan                              | Mandatory | Literal | Japan Zone                                       |
| kwajalein                          | Mandatory | Literal | Kwajalein Zone                                   |
| libya                              | Mandatory | Literal | Libya Zone                                       |
| met                                | Mandatory | Literal | MET Zone                                         |
| mst                                | Mandatory | Literal | MST Zone                                         |
| mst7mdt                            | Mandatory | Literal | MST7MDT Zone                                     |
| mexico/bajanorte                   | Mandatory | Literal | Mexico/BajaNorte Zone                            |
| mexico/bajasur                     | Mandatory | Literal | Mexico/BajaSur Zone                              |
| mexico/general                     | Mandatory | Literal | Mexico/General Zone                              |
| nz                                 | Mandatory | Literal | NZ Zone                                          |
| nz-chat                            | Mandatory | Literal | NZ-CHAT Zone                                     |
| navajo                             | Mandatory | Literal | Navajo Zone                                      |
| prc                                | Mandatory | Literal | PRC Zone                                         |
| pst8pdt                            | Mandatory | Literal | PST8PDT Zone                                     |
| pacific/apia                       | Mandatory | Literal | Pacific/Apia Zone                                |
| pacific/auckland                   | Mandatory | Literal | Pacific/Auckland Zone                            |
| pacific/bougainville               | Mandatory | Literal | Pacific/Bougainville Zone                        |
| pacific/chatham                    | Mandatory | Literal | Pacific/Chatham Zone                             |
| pacific/chuuk                      | Mandatory | Literal | Pacific/Chuuk Zone                               |
| pacific/easter                     | Mandatory | Literal | Pacific/Easter Zone                              |
| pacific/efate                      | Mandatory | Literal | Pacific/Efate Zone                               |
| pacific/enderbury                  | Mandatory | Literal | Pacific/Enderbury Zone                           |
| pacific/fakaofo                    | Mandatory | Literal | Pacific/Fakaofo Zone                             |
| pacific/fiji                       | Mandatory | Literal | Pacific/Fiji Zone                                |
| pacific/funafuti                   | Mandatory | Literal | Pacific/Funafuti Zone                            |
| pacific/galapagos                  | Mandatory | Literal | Pacific/Galapagos Zone                           |
| pacific/gambier                    | Mandatory | Literal | Pacific/Gambier Zone                             |
| pacific/guadalcanal                | Mandatory | Literal | Pacific/Guadalcanal Zone                         |
| pacific/guam                       | Mandatory | Literal | Pacific/Guam Zone                                |
| pacific/honolulu                   | Mandatory | Literal | Pacific/Honolulu Zone                            |
| pacific/johnston                   | Mandatory | Literal | Pacific/Johnston Zone                            |
| pacific/kiritimati                 | Mandatory | Literal | Pacific/Kiritimati Zone                          |
| pacific/kosrae                     | Mandatory | Literal | Pacific/Kosrae Zone                              |
| pacific/kwajalein                  | Mandatory | Literal | Pacific/Kwajalein Zone                           |
| pacific/majuro                     | Mandatory | Literal | Pacific/Majuro Zone                              |
| pacific/marquesas                  | Mandatory | Literal | Pacific/Marquesas Zone                           |
| pacific/midway                     | Mandatory | Literal | Pacific/Midway Zone                              |
| pacific/nauru                      | Mandatory | Literal | Pacific/Nauru Zone                               |
| pacific/niue                       | Mandatory | Literal | Pacific/Niue Zone                                |
| pacific/norfolk                    | Mandatory | Literal | Pacific/Norfolk Zone                             |
| pacific/noumea                     | Mandatory | Literal | Pacific/Noumea Zone                              |
| pacific/pago_pago                  | Mandatory | Literal | Pacific/Pago_Pago Zone                           |
| pacific/palau                      | Mandatory | Literal | Pacific/Palau Zone                               |
| pacific/pitcairn                   | Mandatory | Literal | Pacific/Pitcairn Zone                            |
| pacific/pohnpei                    | Mandatory | Literal | Pacific/Pohnpei Zone                             |
| pacific/ponape                     | Mandatory | Literal | Pacific/Ponape Zone                              |
| pacific/port_moresby               | Mandatory | Literal | Pacific/Port_Moresby Zone                        |
| pacific/rarotonga                  | Mandatory | Literal | Pacific/Rarotonga Zone                           |
| pacific/saipan                     | Mandatory | Literal | Pacific/Saipan Zone                              |
| pacific/samoa                      | Mandatory | Literal | Pacific/Samoa Zone                               |
| pacific/tahiti                     | Mandatory | Literal | Pacific/Tahiti Zone                              |
| pacific/tarawa                     | Mandatory | Literal | Pacific/Tarawa Zone                              |
| pacific/tongatapu                  | Mandatory | Literal | Pacific/Tongatapu Zone                           |
| pacific/truk                       | Mandatory | Literal | Pacific/Truk Zone                                |
| pacific/wake                       | Mandatory | Literal | Pacific/Wake Zone                                |
| pacific/wallis                     | Mandatory | Literal | Pacific/Wallis Zone                              |
| pacific/yap                        | Mandatory | Literal | Pacific/Yap Zone                                 |
| poland                             | Mandatory | Literal | Poland Zone                                      |
| portugal                           | Mandatory | Literal | Portugal Zone                                    |
| roc                                | Mandatory | Literal | ROC Zone                                         |
| rok                                | Mandatory | Literal | ROK Zone                                         |
| singapore                          | Mandatory | Literal | Singapore Zone                                   |
| turkey                             | Mandatory | Literal | Turkey Zone                                      |
| uct                                | Mandatory | Literal | UCT Zone                                         |
| us/alaska                          | Mandatory | Literal | US/Alaska Zone                                   |
| us/aleutian                        | Mandatory | Literal | US/Aleutian Zone                                 |
| us/arizona                         | Mandatory | Literal | US/Arizona Zone                                  |
| us/central                         | Mandatory | Literal | US/Central Zone                                  |
| us/east-indiana                    | Mandatory | Literal | US/East-Indiana Zone                             |
| us/eastern                         | Mandatory | Literal | US/Eastern Zone                                  |
| us/hawaii                          | Mandatory | Literal | US/Hawaii Zone                                   |
| us/indiana-starke                  | Mandatory | Literal | US/Indiana-Starke Zone                           |
| us/michigan                        | Mandatory | Literal | US/Michigan Zone                                 |
| us/mountain                        | Mandatory | Literal | US/Mountain Zone                                 |
| us/pacific                         | Mandatory | Literal | US/Pacific Zone                                  |
| us/samoa                           | Mandatory | Literal | US/Samoa Zone                                    |
| utc                                | Mandatory | Literal | UTC Zone                                         |
| universal                          | Mandatory | Literal | Universal Zone                                   |
| w-su                               | Mandatory | Literal | W-SU Zone                                        |
| wet                                | Mandatory | Literal | WET Zone                                         |
| zulu                               | Mandatory | Literal | Zulu Zone                                        |

#### Examples

```
switch(config)# timezone set us/alaska
```

### Unsetting timezone on the switch
#### Syntax
`no timezone set *TIMEZONE*`

#### Description
This command removes the configured time zone, and sets it to the default UTC time zone.

#### Authority
All users.

#### Parameters
This command takes in the same parameters as the `timezone set` command. Refer to "Setting timezone on the switch".

#### Examples
```
switch(config)#no timezone set us/alaska
```


### Showing system information
#### Syntax
`show system [ < fan | temperature [ detail ] | led | power-supply >]`

#### Description
Using no parameters, this command shows the overall system details, including information about physical components such as the fan, temperature sensor, LED, and power supply. Using a parameter, this command gives detailed information of various physical components.

#### Authority
All users.

#### Parameters
| Parameter 1 | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *fan* | choose one| Literal | Displays fan information. |
| *temperature * | choose one| Literal | Displays temperature-sensor information. |
| *led* | choose one| Literal | Displays LED information. |
| *power-supply* | choose one| Literal | Displays power-supply information. |

| Parameter 2 | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *detail* | Optional | Literal | Displays detailed temperature-sensor information. |

#### Examples
```
switch#show system
OpenSwitch Version  :
Product Name        : 5712-54X-O-AC-F
Vendor              : Edgecore
Platform            : x86_64-accton_as5712_54x-r0
Manufacturer        : Accton
Manufacturer Date   : 03/24/2015 02:05:30
Serial Number       : 571254X1512035      Label Revision      : R01H
ONIE Version        : 2014.08.00.05       DIAG Version        : 2.0.1.0
Base MAC Address    : 70:72:cf:fd:e9:b9   Number of MACs      : 74
Interface Count     : 78                  Max Interface Speed : 40000 Mbps

Fan details:
Name           Speed     Status
--------------------------------
base-1L        normal    ok
base-1R        normal    ok
base-2L        normal    ok
base-2R        normal    ok
base-3L        normal    ok
base-3R        normal    ok
base-4L        normal    ok
base-4R        normal    ok
base-5L        normal    ok
base-5R        normal    ok

LED details:

Name      State     Status
-------------------------
base-loc  on        ok
Power supply details:
Name      Status
-----------------------

base-1    ok
base-2    Input Fault
Temperature Sensors:
Location                                          Name      Reading(celsius)
---------------------------------------------------------------------------
front                                             base-1    21.00
side                                              base-3    18.00
back                                              base-2    20.00
```

### System fan information
#### Syntax
`show system fan`
#### Description
This command displays detailed fan information.
#### Authority
All users
#### Parameters
This command does not require a parameter
#### Example
```
switch#show system fan

Fan information
------------------------------------------------------
Name         Speed  Direction      Status        RPM
------------------------------------------------------
base-2L      normal front-to-back  ok            9600
base-5R      normal front-to-back  ok            8100
base-3R      normal front-to-back  ok            8100
base-4R      normal front-to-back  ok            8100
base-3L      normal front-to-back  ok            9600
base-5L      normal front-to-back  ok            9600
base-1R      normal front-to-back  ok            8100
base-1L      normal front-to-back  ok            9600
base-2R      normal front-to-back  ok            7950
base-4L      normal front-to-back  ok            9600
------------------------------------------------------
Fan speed override is not configured
------------------------------------------------------
```
### Showing system temperature information
#### Syntax
`
show system temperature [detail]
`
#### Description
This command displays detailed temperature sensor information. If a parameter is not used, the command displays minimal temperature information.

#### Authority
All users.

#### Parameters
| Parameter  | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *detail* | Optional | Literal | Displays detailed temperature-sensor information. |

#### Example
```
switch#show system temperature

Temperature information
---------------------------------------------------
            Current
Name      temperature    Status         Fan state
            (in C)
---------------------------------------------------
base-1    21.50          normal         normal
base-3    18.50          normal         normal
base-2    20.50          normal         normal
```

```
switch#show system temperature detail

Detailed temperature information
---------------------------------------------------
Name                      :base-1
Location                  :front
Status                    :normal
Fan-state                 :normal
Current temperature(in C) :21.50
Minimum temperature(in C) :19.50
Maximum temperature(in C) :22.00

Name                      :base-3
Location                  :side
Status                    :normal
Fan-state                 :normal
Current temperature(in C) :18.50
Minimum temperature(in C) :17.50
Maximum temperature(in C) :19.50

Name                      :base-2
Location                  :back
Status                    :normal
Fan-state                 :normal
Current temperature(in C) :20.50
Minimum temperature(in C) :18.50
Maximum temperature(in C) :21.00

```

### Showing system LED information
#### Syntax
`show system led`

#### Description
This command displays detailed LED information.

#### Authority
All users

#### Parameters
This command does not require a parameter.

#### Example
```
switch#show system led

Name           State     Status
-----------------------------------
base-loc       on        ok
```

### Showing system power-supply information

#### Syntax
`show system power-supply`

#### Description
This command displays detailed power-supply information.

#### Authority
All users.

#### Parameters
This command does not require a parameter.

#### Examples
```
switch#show system power-supply
Name           Status
-----------------------------
base-1         ok
base-2         Input Fault
```

### Showing system date information

#### Syntax
`show date`

#### Description
This command displays system date information. It shows system time in <<para>Day> <<para>Mon> <<para>Date> <<para>hh:mm:ss> <<para>timezone> <<para>year> format.

#### Authority
All users.

#### Parameters
No parameters.

#### Examples
```
switch# show date
  Wed Jun 22 18:39:48 UTC 2016
switch#
```

### Showing system CPU information using top

#### Syntax
`top cpu`

#### Description
This command displays detailed CPU information sorted by CPU usage.

#### Authority
All users.

#### Parameters
No parameters.

#### Examples
```
switch# top cpu
top - 23:06:26 up 16:21,  0 users,  load average: 0.85, 0.56, 0.67
Tasks:  45 total,   1 running,  42 sleeping,   0 stopped,   2 zombie
%Cpu(s):  5.7 us,  1.2 sy,  0.0 ni, 93.0 id,  0.0 wa,  0.0 hi,  0.1 si,  0.0 st
KiB Mem : 10221884 total,  1566952 free,   853212 used,  7801720 buff/cache
KiB Swap:  8385532 total,  8368236 free,    17296 used.  9044772 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
    1 root      20   0   29996   4644   3488 S   0.0  0.0   0:00.19 /sbin/init
   16 root      20   0   23352   5796   5524 S   0.0  0.1   0:00.34 /lib/systemd/systemd-journald
   65 root      20   0   32452   2924   2492 S   0.0  0.0   0:00.02 /lib/systemd/systemd-udevd
  138 systemd+  20   0   18276   2688   2484 S   0.0  0.0   0:00.00 /lib/systemd/systemd-resolved
  142 root      20   0  259676   2936   2588 S   0.0  0.0   0:00.06 /usr/sbin/rsyslogd -n
  150 message+  20   0   13180   2496   2272 S   0.0  0.0   0:00.00 /usr/bin/dbus-daemon --system +
  151 root      20   0   13108   2352   2144 S   0.0  0.0   0:00.00 /lib/systemd/systemd-logind
  153 root      20   0   15712   2216   1652 S   0.0  0.0   0:00.00 /usr/sbin/crond -n
```

### Showing system memory information using top

#### Syntax
`top memory`

#### Description
This command displays detailed memory information sorted by memory usage.

#### Authority
All users.

#### Parameters
No parameters.

#### Examples
```
switch# top memory
top - 23:08:08 up 16:23,  0 users,  load average: 0.32, 0.45, 0.62
Tasks:  45 total,   1 running,  42 sleeping,   0 stopped,   2 zombie
%Cpu(s):  5.7 us,  1.2 sy,  0.0 ni, 93.1 id,  0.0 wa,  0.0 hi,  0.1 si,  0.0 st
KiB Mem : 10221884 total,  1546164 free,   873572 used,  7802148 buff/cache
KiB Swap:  8385532 total,  8368236 free,    17296 used.  9024352 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
  321 root      20   0  161984  38516   8848 S   0.0  0.4   0:02.75 python /usr/bin/restd
  236 root      20   0  182212  18520   7176 S   0.0  0.2   0:00.81 python /usr/bin/ops_ntpd
  253 root      20   0  101828  18052   7108 S   0.0  0.2   0:00.29 python /usr/bin/ops_dhcp_tftp
  312 root      20   0  112496  17312   3992 S   0.0  0.2   0:00.07 python /usr/bin/ops_mgmtintfcf+
  405 root      20   0  109908  16208   3344 S   0.0  0.2   0:00.66 python /usr/bin/ops_ntpd
  313 root      20   0  101564  14008   3244 S   0.0  0.1   0:00.00 python /usr/bin/ops_aaautilspa+
  188 root      20   0   40288  13300   4636 S   0.0  0.1   0:00.35 /usr/sbin/ovsdb-server --remot+
```
### Showing time zone information

#### Syntax
`show system timezone`

#### Description
This command displays detailed information for the time zone configured on the system.

#### Authority
All users.

#### Parameters
No parameters.

#### Example
By default the time zone configured is UTC:
```
switch# show system timezone
System is configured for timezone : UTC
      DST active: n/a
```
If the time zone is configured for "US/Alaska", then it may be verified using the `show system timezone` command:
```
switch# show system timezone
System is configured for timezone : US/Alaska
      DST active: yes
 Last DST change: DST began at
                  Sun 2016-03-13 01:59:59 AKST
                  Sun 2016-03-13 03:00:00 AKDT
 Next DST change: DST ends (the clock jumps one hour backwards) at
                  Sun 2016-11-06 01:59:59 AKDT
                  Sun 2016-11-06 01:00:00 AKST
```
