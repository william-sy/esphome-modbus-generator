# Desired output, its not complete or perfect, but saves a lot of typing :) :
#sensor:
#  - platform: modbus_controller
#    modbus_controller_id: 
#    name: ""
#    id: 
#    register_type: holding
#    address: 2032 
#    value_type: U_WORD
import yaml
input_yaml_file     = 'Registers.yaml'
output_yaml_file    = 'esphomeconfig.yaml'

with open(input_yaml_file, mode='r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

for register in data.get('registers', []):
    if 'Number' in register:
        register['address'] = int(register.pop('Number')) - 40001
    if 'Unit' in register and register['Unit'] == 'None':
        register.pop('Unit')
    elif 'Unit' in register:
        register['unit_of_measurement'] = register.pop('Unit')
    if 'DataType' in register:
        register['value_type'] = register.pop('DataType')
    if 'value_type' in register and register['value_type'] == "0X00":
        register['value_type'] = "U_WORD"
    elif 'value_type' in register and register['value_type'] == "0X91":
        register['value_type'] = "S_WORD"
    if 'value_type' in register and register['value_type'] == "0X10":
        register['value_type'] = "U_WORD"
    # New fields:
    register['register_type'] = "holding"
    register['state_class'] = "measurement"
    register['platform'] = "modbus_controller"
    register['modbus_controller_id'] = "wtw"

    if 'Max' in register:
        register.pop('Max')
    if 'Min' in register:
        register.pop('Min')
    if 'Step' in register:
        register.pop('Step')
    if 'Type' in register:
        register.pop('Type')
    
yaml_data = yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True, indent=2)

# Write the transformed YAML data to a new file
with open(output_yaml_file, mode='w', encoding='utf-8') as file:
    file.write(yaml_data)

print(f"Transformed YAML data has been written to {output_yaml_file}")