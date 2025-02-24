# Overview

This is a set of Python tools for helping with the migration from FOLIO OKAPI platform to FOLIO Eureka platform. A lot of the scripts need to be ran in the order presented below as they build upon each other. I purposely did not combine them into a single function as to allow for the review of data at each step.

# Installation

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

# Scripts

## Get OKAPI Permissions

 !!! Run First !!!
 This script needs to be ran first to pull all the permission sets from an OKAPI instance of FOLIO. By Default Ramsons BugFest has been added to the .env file.

### Running the script:

```bash
python ./pullOkapiPermissions.py
```

## Get Eureka Permissions

 !!! Run First !!!

This script pulls the Capabilities and Capability Sets from the Eureka platform and saves them in JSON format to be used later.

- _At this time i can not log in via the API, so the JSON was pulled via the web interface and saved into a JSON file._

### Running the script:

```bash
python ./pullOkapiPermissions.py
```

## Get Production Permission Sets

This script pulls the current permission sets form your reference system and saves them in JSON format.

### Running the script:

```bash
python ./pullReferenceData.py
```

## Compare OKAPI to Eureka

This script pulls the Capability Sets and uses the published names to match them to a OKAPI permission set. It expands on the included capabilities and permissions to show the names and UUIDS.  Two files are generated:
`FILE_COMPARED_SETS_TO_PERMISSIONS`: JSON file with all the collected data
`FILE_COMPARED_SETS_TO_PERMISSIONS_CSV`: CV file that can be opened in Excel for easier viewing. the first row is are the headers. The data is formatted as:

**Eureka capability set**: _id	name	type	resource	description	action_

**Found OKAPI Permission Set**: _okapiDisplayName_

**Eureka linked Capabilities**: _subCapabilities.name	subCapabilities.type	subCapabilities.resource	subCapabilities.description	subCapabilities.action_

**OKAPI sub permissions (if a Matching permission set is found)**: _okapiSubPermissions.name	okapiSubPermissions.description	okapiSubPermissions.permissionName_

### Running the script:

```bash
python ./compareOkapiToEureka.py
```

## Expanded Capability Sets

This scripts takes the Capability set data and expands out the linked capabilities. 

### Files generated:

- `FILE_EUREKA_CAPABILITY_SETS_EXPANDED`: JSON file listing all the capability sets and the capabilities assigned to that set
- `FILE_EUREKA_CAPABILITY_SETS_EXPANDED_CSV`: CSV file of the same data set.
- `FILE_EUREKA_CAPABILITY_SETS_EXPANDED_HTML`: HTML Table view that can be opened directly in the browser or saved to Confluence.

### Running the script:

```bash
python ./expandCapabilitySets.py
```

## Compare Current Permissions to Capability Sets

This script takes current permission sets in the reference environment (visible, and mutable) expands the sub permissions. During this process it adds the supervision name, and description if they are included. it also looks to see if there is a matching capability, and lists that data. 
This should allow a user to re-create a permission set using just capabilities. 

### Files generated:

- `FILE_COMPARED_CURRENT_TO_CAPABILITIES`: JSON version of the expanded data
- `FILE_COMPARED_CURRENT_TO_CAPABILITIES_CSV`: CSV version of the same data set



### Running the script:

```bash
python ./compareCurrentToCapabilities.py
```

## Find possible compatibility sets

This script will look that the JSON generated from `compareCurrentToCapabilities.py` and compare the assigned Compatibility sets and rank what set may bes fit in a new role that will match the Permission Set. It does this by looking at the capability Sets individual capabilitys and then matches thos to the ones in the permission set. The fallowing data will be added:

**Total** - Total number of capabilities in the set

**Matching** - Number of matching Capabilities to the permission set

**Ranking** - based on the percentage of total number of capabilities that match

Items with a rank of 0 or lower then X will be ignored.

### Files generated:

- `FILE_COMPARED_CURRENT_TO_CAPABILITIES`: JSON version of the expanded data
- `FILE_COMPARED_CURRENT_TO_CAPABILITIES_CSV`: CSV version of the same data set

# Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please also fork as needed.

# .env File
FILE_OKAPI_PERMISSIONS: Location of the OKAPI permissions JSON file. This will be used fro reading and writing depending on the script ran.
FILE_EUREKA_CAPABILITY_SETS = Location of the Eureka Capability Sets JSON file. This will be used fro reading and writing depending on the script ran.
FILE_EUREKA_CAPABILITIES = Location of the Eureka Capabilities JSON file. This will be used fro reading and writing depending on the script ran.
FILE_COMPARED_SETS_TO_PERMISSIONS = Location of the OKAPI to Eureka Capability Set comparisons JSON file. This will be used fro reading and writing depending on the script ran.

# License

[MIT](https://choosealicense.com/licenses/mit/)