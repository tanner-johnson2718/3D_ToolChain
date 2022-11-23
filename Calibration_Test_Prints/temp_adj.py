file_name = "TOWER.GCO"
temps  = [215, 210, 205, 200, 195, 190, 185, 180]
layers = [40,  75,  105, 140, 175, 205, 240, 275]
layer_string_base = ";LAYER:"
layer_string_curr = ""
layer_index = 0
line_index = 0
data = []

with open(file_name, 'r') as my_file_handle:
    data = my_file_handle.readlines()

layer_string_curr = layer_string_base + str(layers[layer_index])

for line in data:
    if line.find(layer_string_curr) == 0:
        data.insert(line_index+1, "M104 S" + str(temps[layer_index]) + '\n')
        layer_index += 1
        if layer_index == len(temps):
            break
        layer_string_curr = layer_string_base + str(layers[layer_index])
    
    line_index += 1

with open(file_name, 'w') as my_file:
    my_file.writelines(data)