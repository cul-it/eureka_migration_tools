# Overview

This repository contains a set of Python tools to assist with the migration from the FOLIO OKAPI platform to the FOLIO Eureka platform. Many of the scripts need to be run in the order presented below as they build upon each other. I purposely did not combine them into a single function to allow for the review of data at each step.


# Installation

Copy .env.example over to .env and populate with your local settings.

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

# Running

An interactive menu has been added to make it easier to run the included scripts. This menu can be accessed by running:


```bash
python ./main.py
```

## Menu options

### 1. Pull Reference Data:
This menu option runs four scripts:
-   Script one pulls all OKAPI permissions.
-   Script two pulls all Eureka capabilities.
-   Script three pulls all Eureka capability sets.
-   Script four pulls all OKAPI user permissions from your reference environment.

### 2. Build Comparisons:
This menu option runs three comparison scripts against the data pulled in the first menu option.

-   Script one adds all the sub-capability data to the capability sets; this option also generates a web page displaying the data in an easy-to-read format.
-   Script two compares permissions to capabilities.
-   Script three builds a comparison of current user permission sets to capabilities.

### 3. Build Working CSV and HTML File:   
This menu option runs two scripts that build upon the data generated in the second menu option.

-   Script one looks at the data generated from comparing the current user permissions to capabilities and identifies which capability sets could be used to fulfill the original permission sets. This file can be edited and resubmitted.
-   Script two creates the "FOLIO Roles Simulator" web interface. This uses the data collected in the previous steps to create a dynamic web interface to test creating roles. 


### 4. Reprocess the Capability Set Selection File (csv):
_(not implmented yet)_

This menu option takes the CSV file generated in menu option 3 and reprocesses it.

### 5. Run a Specific Script: 
Each of these menu options is outlined below.

- **Pull Reference Data - OKAPI Permissions**: 
- **Pull Reference Data - Capability Sets**: 
- **Pull Reference Data - Capabilities**: 
- **Pull Reference Data - OKAPI Permission Sets**: 
- **Expand Capability Sets**: 
- **Compare OKAPI Permissions to Eureka Capabilities**: 
- **Compare Current User Permission Sets to Eureka Capabilities**: 
- **Find Possible Capability Matches to OKAPI Permissions**: 
- **Build Web Interface - FOLIO Roles Simulator**: 
- **Build Web Interface - FOLIO Roles Simulator Without Comparisons**: 
- **Reprocess the Capability Set Selection File (csv)**:  _(not implmented yet)_
- **Main Menu**: 

### 6. Quit: 



# Individual Scripts

## Data Retrieval Functions

## Pull Reference Data - OKAPI Permissions
**Run First!** This script needs to be run first to pull all the permission sets from an OKAPI instance of FOLIO. By default, Ramsons BugFest has been added to the `.env` file.

## Pull Reference Data - Capability Sets

**Run First!** This script pulls the capability sets from the Eureka platform and saves them in JSON format to be used later.

## Pull Reference Data - Capabilities

**Run First!** This script pulls the capabilities from the Eureka platform and saves them in JSON format to be used later.

## Pull Reference Data - OKAPI Permission Sets

This script pulls the current permission sets from your reference system and saves them in JSON format. The reference system should be a production or test system with a current set of user permission sets.

---
## Data Formatting Functions

## Expanded Capability Sets

This script takes the capability set data and expands the linked capabilities.

### Files generated:
-   `FILE_EUREKA_CAPABILITY_SETS_EXPANDED`: JSON file listing all the capability sets and the capabilities assigned to that set.
-   `FILE_EUREKA_CAPABILITY_SETS_EXPANDED_CSV`: CSV file of the same data set.
-   `FILE_EUREKA_CAPABILITY_SETS_EXPANDED_HTML`: HTML table view that can be opened directly in the browser or saved to Confluence.

## Compare OKAPI Permissions to Eureka Capabilities

This script pulls the capability sets and uses the published names to match them to an OKAPI permission set. It expands on the included capabilities and permissions to show the names and UUIDs. Two files are generated:

-   `FILE_COMPARED_SETS_TO_PERMISSIONS`: JSON file with all the collected data.
-   `FILE_COMPARED_SETS_TO_PERMISSIONS_CSV`: CSV file that can be opened in Excel for easier viewing. The first row contains the headers. The data is formatted as:
    -   **Eureka capability set**: _id, name, type, resource, description, action_
    -   **Found OKAPI Permission Set**: _okapiDisplayName_
    -   **Eureka linked Capabilities**: _subCapabilities.name, subCapabilities.type, subCapabilities.resource, subCapabilities.description, subCapabilities.action_
    -   **OKAPI sub-permissions (if a matching permission set is found)**: _okapiSubPermissions.name, okapiSubPermissions.description, okapiSubPermissions.permissionName_


## Compare Current User Permission Sets to Eureka Capabilities

This script takes current permission sets in the reference environment (visible and mutable) and expands the sub-permissions. During this process, it adds the supervision name and description if they are included. It also looks to see if there is a matching capability and lists that data. This should allow a user to recreate a permission set using just capabilities.

### Files generated:
-   `FILE_COMPARED_CURRENT_TO_CAPABILITIES`: JSON version of the expanded data.
-   `FILE_COMPARED_CURRENT_TO_CAPABILITIES_CSV`: CSV version of the same data set.

---
## Create Working Documents

## Find Possible Capability Matches to OKAPI Permissions
This script will look at the JSON generated from `compareCurrentToCapabilities.py` and compare the assigned capability sets, ranking which set may best fit a new role that will match the permission set. It does this by looking at the capability sets' individual capabilities and then matching those to the ones in the permission set. The following data will be added:

-   **Total**: Total number of capabilities in the set.
-   **Matching**: Number of matching capabilities to the permission set.
-   **Ranking**: Based on the percentage of total number of capabilities that match. Items with a rank of 0 or lower than X will be ignored.

#### Files generated:

-   `FILE_COMPARED_CURRENT_TO_CAPABILITIES`: JSON version of the expanded data.
-   `FILE_COMPARED_CURRENT_TO_CAPABILITIES_CSV`: CSV version of the same data set.

## Build Web Interface - FOLIO Roles Simulator
This script will take the data produced in the previous scripts and generate a web interface that allows a user to pull up a current permission set and rebuild it using capability sets and capabilities. No server is required to run this page; it runs entirely in the user's browser.

### How to use 
-   Open the generated HTML in the browser of your choice (tested with Chrome).
-   Select a permission set from the drop-down on the left-hand side of the screen (red arrow).
-   Using the interface on the right side of the screen, start by selecting capability sets to fill in the majority of your missing capabilities for your permission set (blue arrow).
-   Use the capabilities section to fill any smaller gaps (blue arrow).

 ![Overview of the web interface](References/image.png)

In this image, you can see that the permission set "Acq Unopen Reopen" has been selected. The three sections under the selection box are:

-   **Missing Capabilities**: These are the capabilities that the scripts have identified as needed to recreate the permission set but are currently missing. In this example, since no capability sets or capabilities are selected, all sub-capabilities are displayed.
-   **Extra Capabilities**: These are capabilities that were added by selecting either capability sets or capabilities on the left.
-   **Assigned Capabilities**: These are the currently assigned capabilities based on what has been selected on the left.

 ![Overview of the web interface](References/image1.png)

This image depicts what happens after a user has selected a capability set on the left. The three areas are adjusted to show the most current information.

 ![Overview of the web interface](References/image2.png)

## Build Web Interface - FOLIO Roles Simulator Without Comparisons
This is the same interface as above but without the ability to select a current permission set in FOLIO Okapi and see missing extra capabilities. Instead this just lists the capabilities assigned by selected options form the table on the left. Results can be exported to a CSV file for later use.

## Reprocess the Capability Set Selection File (csv)

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please also fork as needed.

# .env File

## OKAPI Env
These environment variables are for your OKAPI reference environment. I suggest using BugFest as you want this data to be as up-to-date as possible.

`OKAPI_URL` =

`OKAPI_TENANT` =

`OKAPI_USER` =

`OKAPI_PASSWORD` =

## Eureka Env
These environment variables are for your Eureka reference environment. I suggest using Snapshot or BugFest as you want this data to be as up-to-date as possible.

`EUREKA_URL` =

`EUREKA_TENANT` =

`EUREKA_USER` =

`EUREKA_PASSWORD` =

## Reference OKAPI Env

These environment variables are for your production or test environment. The user account will need permissions to read permission data. This connection is used to pull your current permission sets.

`REF_OKAPI_URL` =

`REF_OKAPI_TENANT` =

`REF_OKAPI_USER` =

`REF_OKAPI_PASSWORD` =

## Reference server - Production or test server with real permission data in it.

These final settings are where files will be stored on your machine. to be safe it is suggested that you use absolute directory paths.

`BASE_DIR` = Base directory where all file will be stored.

`FILE_OKAPI_PERMISSIONS` = Location of the OKAPI permissions JSON file. This will be used fro reading and writing depending on the script ran.

`FILE_REF_OKAPI_PERMISSIONS` =

`FILE_EUREKA_CAPABILITY_SETS` = Location of the Eureka Capability Sets JSON file. This will be used fro reading and writing depending on the script ran.

`FILE_EUREKA_CAPABILITIES` = Location of the Eureka Capabilities JSON file. This will be used fro reading and writing depending on the script ran.

`FILE_EUREKA_CAPABILITY_SETS_EXPANDED` =

`FILE_COMPARED_SETS_TO_PERMISSIONS` = Location of the OKAPI to Eureka Capability Set comparisons JSON file. This will be used fro reading and writing depending on the script ran.

`FILE_COMPARED_CURRENT_TO_CAPABILITIES` =

`FILE_FIND_MY_CAPABILITIES` =

`FILE_NEW_ROLES` =

`FILE_WORKING_WEB_PAGE` =



# License

[MIT](https://choosealicense.com/licenses/mit/)