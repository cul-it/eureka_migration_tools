# Overview

This is a set of Python tools for helping with the migration from FOLIO OKAPI platform to FOLIO Eureka platform.

## Installation

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Scripts
### Get OKAPI Permissions
 !!! Run First !!!
 This script needs to be ran first to pull all the permission sets from an OKAPI instance of FOLIO. By Default Ramsons BugFest has been added to the .env file.

#### Running the script:

```bash
python ./pullOkapiPermissions.py
```

### Get Eureka Permissions
**_Not Functional_**

This script pulls the Capabilities and Capability Sets from the Eureka platform and saves them in JSON format to be used later.

- _At this time i can not log in via the API, so the JSON was pulled via the web interface and saved into a JSON file._

#### Running the script:

```bash
python ./pullEurekaCapabilities.py
```
### Compare

This script pulls the Capability Sets and uses the published names to match them to a OKAPI permission set. It expands on the included capabilities and permissions to show the names and UUIDS.  Two files are generated:
`FILE_COMPARED_SETS_TO_PERMISSIONS`: JSON file with all the collected data
`FILE_COMPARED_SETS_TO_PERMISSIONS_CSV`: CV file that can be opened in Excel for easier viewing. the first row is are the headers. The data is formatted as:

**Eureka capability set**: _id	name	type	resource	description	action_

**Found OKAPI Permission Set**: _okapiDisplayName_

**Eureka linked Capabilities**: _subCapabilities.name	subCapabilities.type	subCapabilities.resource	subCapabilities.description	subCapabilities.action_

**OKAPI sub permissions (if a Matching permission set is found)**: _okapiSubPermissions.name	okapiSubPermissions.description	okapiSubPermissions.permissionName_

#### Running the script:

```bash
python ./compare.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please also fork as needed.

## .env File
FILE_OKAPI_PERMISSIONS: Location of the OKAPI permissions JSON file. This will be used fro reading and writing depending on the script ran.
FILE_EUREKA_CAPABILITY_SETS = Location of the Eureka Capability Sets JSON file. This will be used fro reading and writing depending on the script ran.
FILE_EUREKA_CAPABILITIES = Location of the Eureka Capabilities JSON file. This will be used fro reading and writing depending on the script ran.
FILE_COMPARED_SETS_TO_PERMISSIONS = Location of the OKAPI to Eureka Capability Set comparisons JSON file. This will be used fro reading and writing depending on the script ran.

## License

[MIT](https://choosealicense.com/licenses/mit/)