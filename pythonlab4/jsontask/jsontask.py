import json

with open('sample.json', 'r') as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)
print("{:<50} {:<20} {:<8} {:<6}".format("DN", "Description", "Speed", "MTU"))
print("-" * 50 + " " + "-" * 20 + "  " + "-" * 6 + "  " + "-" * 6)

for interface in data['imdata']:
    attributes = interface['l1PhysIf']['attributes']
    dn = attributes['dn']
    description = attributes.get('descr', '') 
    speed = attributes.get('speed', 'inherit')  
    mtu = attributes.get('mtu', '')  
    print("{:<50} {:<20} {:<8} {:<6}".format(dn, description, speed, mtu))