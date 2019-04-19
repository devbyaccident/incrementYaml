# Using ruamel yaml for the formatting options
# https://yaml.readthedocs.io/en/latest/overview
# pip install ryd

import ruamel.yaml
yaml = ruamel.yaml.YAML()

# Functions we will use
def yamlLoader(path):
    with open(path, "r") as fileObj:
        data = yaml.load(fileObj)
    return data

def yamlDump(path, data):
    with open(path, "w") as fileObj:
        yaml.dump(data, fileObj)

def versChanger(data, vers, appArr, firstLayer, secondLayer):
    for key, val in data.items():
        
        # Filter for apps passed in
        if key in appArr:
            
            # It is surprisingly hard to iterate over nested dicts without nesting for loops in python...
            versSplit = val[firstLayer][secondLayer]

            # Taking the 'v' off and breaking into Major Minor and Release
            versSplit = versSplit[1:].split('.')

            # Add one. Can parameterize to add more or negatives
            versSplit[vers] = int(versSplit[vers]) + 1

            # Because I'm joining ints in a str list, have to cast them as strings first
            versSplit = '.'.join(map(str,versSplit))

            # Putting the 'v' back on and overwriting the current value
            val[firstLayer][secondLayer] = 'v'+versSplit

    return data

# Now the work starts...
if __name__ == "__main__":

    # Asking for user unput. Could refactor this to take input from a pipeline    
    vers = input("Enter version to increment: \n1: Major\n2: Minor\n3: Release\n:")
    
    # Adjusting the user input to use as an index. This needs to be removed if user input is
    vers = int(vers) - 1
    
    # An array of items to increment. Again, can prompt or pass from CI loop
    appArr = ['adminApi', 'permissionsService']
 
    # These can be adjusted as the YAML file changes
    firstLayer = 'image'
    secondLayer = 'dockerTag'

    data = yamlLoader("example.yaml")
    versChanger(data, vers, appArr, firstLayer, secondLayer)
    yamlDump("output.yaml", data)

#end