import time
from simple_term_menu import TerminalMenu
from src.pull_scripts.pullOkapiPermissions import get_permissions
from src.pull_scripts.pullEurekaCapabilities import get_capabilities, get_capability_sets
from src.pull_scripts.pullReferenceData import get_permission_sets
from src.format_scripts.expandCapabilitySets import expand_and_save_capability_sets
from src.format_scripts.compareOkapiToEureka import compare_permissions_to_capability_sets
from src.format_scripts.compareCurrentToCapabilities import compare_current_permissions
from src.working_scripts.findMyCapabilitySets import find_possible_compatibility_sets
from src.working_scripts.generateWorkingWebPage import generate_web_page
from src.working_scripts.processNewPermissions import reprocess_cap_sets
from src.working_scripts.generateSelectWebPage import generate_mock_web_page

def main():
    main_menu_title = """  
    -------------------------------------------------
                Eureka Role helper Scripts
    -------------------------------------------------

    Please be sure to copy over .env.sample to .env and populate it with your local variables.
    Main Menu.
    Press Q or Esc to quit.
    """
    main_menu_items = ["Pull Reference Data", "Build Comparisons", "Build Working CSV and HTML File", "Reprocess the Capability Set Selection File (csv)", "Run a Specific Script", "Quit"]
    main_menu_exit = False

    main_menu = TerminalMenu(
        menu_entries=main_menu_items,
        title=main_menu_title,
        cycle_cursor=True,
        clear_screen=True,
    )

    sub_menu_title = """
    -------------------------------------------------
                Run Individual Scripts
    -------------------------------------------------
    This sub menu allows you to run the scripts individual if required.
    Individual Scripts Menu.
    Press Q or Esc to quit.
    """
    sub_menu_items = [
        "Pull Reference Data - OKAPI Permissions", "Pull Reference Data - Capability Sets", "Pull Reference Data - Capabilities", "Pull Reference Data - OKAPI Permission Sets"
        "Expand Capability Sets", "Compare OKAPI Permissions to Eureka Capabilities", "Compare Current User Permission Sets to Eureka Capabilities",
        "Find Possible Capability Matches to OKAPI Permissions", "Build Web Interface - FOLIO Roles Simulator", "Build Web Interface 2 - FOLIO Roles Simulator w/o comparison", "Reprocess the Capability Set Selection File (csv)", "Main Menu"
    ]
    sub_menu_back = False
    sub_menu = TerminalMenu(
        sub_menu_items,
        title=sub_menu_title,
        cycle_cursor=True,
        clear_screen=True,
    )

    while not main_menu_exit:
        main_sel = main_menu.show()

        if main_sel == 0:
            print("Pulling Reference Data >>>>>>>")
            get_permissions()
            get_capabilities()
            get_capability_sets()
            get_permission_sets()
            print("<<<<<<< Process Complete >>>>>>>")
            time.sleep(5)
        elif main_sel == 1:
            print("Building Comparisons >>>>>>>")
            expand_and_save_capability_sets()
            compare_permissions_to_capability_sets()
            compare_current_permissions()
            print("<<<<<<< Process Complete >>>>>>>")
            time.sleep(5)
        elif main_sel == 2:
            print("Building Working CSV and HTML File")
            find_possible_compatibility_sets()
            generate_web_page()
            generate_mock_web_page()
            print("<<<<<<< Process Complete >>>>>>>")
            time.sleep(5)
        elif main_sel == 3:
            print("Reprocessing the Capability Set Selection File (csv)")
            reprocess_cap_sets()
            print("<<<<<<< Process Complete >>>>>>>")
            time.sleep(5)
        elif main_sel == 4:
            while not sub_menu_back:
                sub_sel = sub_menu.show()
                if sub_sel == 0:
                    print("Pulling Reference Data - OKAPI Permissions >>>>>>>")
                    get_permissions()
                    time.sleep(5)
                elif sub_sel == 1:
                    print("Pulling Reference Data - Capability Sets >>>>>>>")
                    get_capability_sets()
                    time.sleep(5)
                elif sub_sel == 2:
                    print("Pulling Reference Data - Capabilities >>>>>>>")
                    get_capabilities()
                    time.sleep(5)
                elif sub_sel == 3:
                    print("Pulling Reference Data - OKAPI Permission Sets >>>>>>>")
                    get_permission_sets()
                    time.sleep(5)
                elif sub_sel == 4:
                    print("Expanding Capability Sets >>>>>>>")
                    expand_and_save_capability_sets()
                    time.sleep(5)
                elif sub_sel == 5:
                    print("Comparing OKAPI User Permission Sets to Eureka Capabilities >>>>>>>")
                    compare_permissions_to_capability_sets()
                    time.sleep(5)
                elif sub_sel == 6:
                    print("Comparing OKAPI Permissions to Eureka Capabilities >>>>>>>")
                    compare_current_permissions()
                    time.sleep(5)
                elif sub_sel == 7:
                    print("Find Possible Capability Matches to OKAPI Permissions >>>>>>>")
                    find_possible_compatibility_sets()
                    time.sleep(5)
                elif sub_sel == 8:
                    print("Build Web Interface - FOLIO Roles Simulator >>>>>>>")
                    generate_web_page()
                    time.sleep(5)
                elif sub_sel == 9:
                    print("Build Web Interface - FOLIO Roles Simulator with out comparison >>>>>>>")
                    generate_mock_web_page()
                    time.sleep(5)
                elif sub_sel == 10:
                    print("Reprocessing the CSV file to find more capability sets >>>>>>>")
                    reprocess_cap_sets()
                    time.sleep(5)
                elif sub_sel == 11 or sub_sel == None:
                    sub_menu_back = True
                    print("Back Selected")
        elif main_sel == 5 or main_sel == None:
            main_menu_exit = True
            print("Quit Selected")


if __name__ == "__main__":
    main()