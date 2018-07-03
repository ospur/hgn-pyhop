import hgn_pyhop, logistics_domain

print('')
hgn_pyhop.print_operators()
print('')
hgn_pyhop.print_methods()

state1 = hgn_pyhop.State('state1')
state1.packages = {'package1', 'package2'}
state1.trucks = {'truck1', 'truck6'}
state1.airplanes = {'plane2'}
state1.locations = {'location1', 'location2', 'location3', 'airport1', 'location10', 'airport2'}
state1.airports = {'airport1', 'airport2'}
state1.cities = {'city1', 'city2'}

state1.at = {'package1': 'location1',
             'package2': 'location2',
             'truck1': 'location3',
             'truck6': 'location10',
             'plane2': 'airport2'}
state1.in_city = {'location1': 'city1',
                  'location2': 'city1',
                  'location3': 'city1',
                  'airport1': 'city1',
                  'location10': 'city2',
                  'airport2': 'city2'}

print("""
----------
Goal 1: package1 is at location2; package2 is at location3 (transport within the same city)
----------
""")
hgn_pyhop.pyhop(state1, [('at', 'package1', 'location2'), ('at', 'package2', 'location3')], verbose=3)

print("""
----------
Goal 2: package1 is at location10 (transport to a different city)
----------
""")
hgn_pyhop.pyhop(state1, [('at', 'package1', 'location10')], verbose=3)

print("""
----------
Goal 3: package1 is at location1 (no actions needed)
----------
""")
hgn_pyhop.pyhop(state1, [('at', 'package1', 'location1')], verbose=3)
