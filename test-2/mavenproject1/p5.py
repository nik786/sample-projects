#python p9.py -api debitcardsetup-iapi -id sysTIAGGDHGSDK -v1 1.3-1.11 -v2 3-1.13
import argparse
import yaml

def add_data_to_yaml(input_file, api, id, v1, v2):
    # New data to add under clientVersionRules
    new_data = {
        id: {
            "defaultMajorMinorVersion": v1,
            "versionRules": {
                "1": {
                    "defaultMinorVersion": v2
                }
            }
        }
    }

    # Load the YAML file
    with open(input_file, "r") as yaml_file:
        data = yaml.safe_load(yaml_file)

    # Locate the position to add the new data
    if "eurekazuul" not in data:
        data["eurekazuul"] = {}
    if "serviceClientVersionMap" not in data["eurekazuul"]:
        data["eurekazuul"]["serviceClientVersionMap"] = {}
    if api not in data["eurekazuul"]["serviceClientVersionMap"]:
        data["eurekazuul"]["serviceClientVersionMap"][api] = {}
    if "allowableConsumers" not in data["eurekazuul"]["serviceClientVersionMap"][api]:
        data["eurekazuul"]["serviceClientVersionMap"][api]["allowableConsumers"] = []
    if "clientVersionRules" not in data["eurekazuul"]["serviceClientVersionMap"][api]:
        data["eurekazuul"]["serviceClientVersionMap"][api]["clientVersionRules"] = {}
    data["eurekazuul"]["serviceClientVersionMap"][api]["clientVersionRules"].update(new_data)

    # Rearrange the data to match the desired format
    default_version = data["eurekazuul"]["serviceClientVersionMap"][api].pop("defaultVersion")
    data["eurekazuul"]["serviceClientVersionMap"][api]["clientVersionRules"]["default"] = default_version

    # Write the updated data back to the YAML file without using sort_keys
    with open(input_file, "w") as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

    print(f"New data added under clientVersionRules in {input_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add data to a YAML file")
    parser.add_argument("-api", help="API name", required=True)
    parser.add_argument("-id", help="ID", required=True)
    parser.add_argument("-v1", help="Version 1", required=True)
    parser.add_argument("-v2", help="Version 2", required=True)

    args = parser.parse_args()
    file = "test.yml"
    add_data_to_yaml(file, args.api, args.id, args.v1, args.v2)
