import hgn_pyhop, satellite_domain


print('')
hgn_pyhop.print_operators()
print('')
hgn_pyhop.print_methods()


# Problem 1
state1 = hgn_pyhop.State('state1')
state1.satellites = {'satellite0'}
state1.instruments = {'instrument0'}
state1.modes = {'image1', 'spectrograph2', 'thermograph0'}
state1.directions = {'Star0', 'GroundStation1', 'GroundStation2', 'Phenomenon3', 'Phenomenon4', 'Star5', 'Phenomenon6'}

state1.power_avail = {'satellite0': True}
state1.pointing = {'satellite0': 'Phenomenon6'}
state1.on_board = {'instrument0': 'satellite0'}
state1.supports = {'instrument0': 'thermograph0'}
state1.calibration_target = {'instrument0': 'GroundStation2'}
state1.power_on = {'instrument0': False}
state1.calibrated = {'instrument0': False}
state1.have_image = {'Star0': '',
                     'Phenomenon3': '',
                     'Phenomenon4': '',
                     'Star5': '',
                     'Phenomenon6': ''}

hgn_pyhop.pyhop(state1, [('have_image', 'Phenomenon4', 'thermograph0'),
                         ('have_image', 'Star5', 'thermograph0'),
                         ('have_image', 'Phenomenon6', 'thermograph0')], verbose=1)


# Problem 10
state2 = hgn_pyhop.State('state2')
state2.satellites = {'satellite0', 'satellite1', 'satellite2', 'satellite3', 'satellite4'}
state2.instruments = {'instrument0', 'instrument1', 'instrument2', 'instrument3', 'instrument4', 'instrument5',
                      'instrument6', 'instrument7', 'instrument8', 'instrument9', 'instrument10'}
state2.modes = {'infrared0', 'spectrograph1', 'image2', 'infrared3', 'image4'}
state2.directions = {'Star0', 'Star1', 'Star2', 'GroundStation3', 'Star4', 'Planet5', 'Star6', 'Star7', 'Phenomenon8',
                     'Planet9', 'Planet10', 'Star11', 'Star12', 'Phenomenon13', 'Phenomenon14', 'Star15', 'Star16'}

state2.power_avail = {'satellite0': True,
                      'satellite1': True,
                      'satellite2': True,
                      'satellite3': True,
                      'satellite4': True}
state2.pointing = {'satellite0': 'Star0',
                   'satellite1': 'Star4',
                   'satellite2': 'Star1',
                   'satellite3': 'GroundStation3',
                   'satellite4': 'Planet10'}
state2.on_board = {'instrument0': 'satellite0',
                   'instrument1': 'satellite0',
                   'instrument2': 'satellite1',
                   'instrument3': 'satellite1',
                   'instrument4': 'satellite2',
                   'instrument5': 'satellite2',
                   'instrument6': 'satellite3',
                   'instrument7': 'satellite3',
                   'instrument8': 'satellite4',
                   'instrument9': 'satellite4',
                   'instrument10': 'satellite4'}
state2.supports = {'instrument0': {'image4'},
                   'instrument1': {'infrared0', 'spectrograph1'},
                   'instrument2': {'infrared0', 'image2'},
                   'instrument3': {'infrared3', 'infrared0'},
                   'instrument4': {'spectrograph1', 'image4', 'infrared0'},
                   'instrument5': {'image2', 'infrared0', 'infrared3'},
                   'instrument6': {'infrared0', 'infrared3'},
                   'instrument7': {'image4', 'spectrograph1', 'infrared3'},
                   'instrument8': {'spectrograph1', 'image4'},
                   'instrument9': {'infrared3'},
                   'instrument10': {'image2', 'image4'}}
state2.calibration_target = {'instrument0': 'Star1',
                             'instrument1': 'GroundStation3',
                             'instrument2': 'GroundStation3',
                             'instrument3': 'Star4',
                             'instrument4': 'Star2',
                             'instrument5': 'Star0',
                             'instrument6': 'GroundStation3',
                             'instrument7': 'Star4',
                             'instrument8': 'Star4',
                             'instrument9': 'Star2',
                             'instrument10': 'Star0',
                             }
state2.power_on = {'instrument0': False,
                   'instrument1': False,
                   'instrument2': False,
                   'instrument3': False,
                   'instrument4': False,
                   'instrument5': False,
                   'instrument6': False,
                   'instrument7': False,
                   'instrument8': False,
                   'instrument9': False,
                   'instrument10': False}
state2.calibrated = {'instrument0': False,
                     'instrument1': False,
                     'instrument2': False,
                     'instrument3': False,
                     'instrument4': False,
                     'instrument5': False,
                     'instrument6': False,
                     'instrument7': False,
                     'instrument8': False,
                     'instrument9': False,
                     'instrument10': False}
state2.have_image = {'Star0': '',
                     'Star1': '',
                     'Star2': '',
                     'Star4': '',
                     'Planet5': '',
                     'Star6': '',
                     'Star7': '',
                     'Phenomenon8': '',
                     'Planet9': '',
                     'Planet10': '',
                     'Star11': '',
                     'Star12': '',
                     'Phenomenon13': '',
                     'Phenomenon14': '',
                     'Star15': '',
                     'Star16': ''}

hgn_pyhop.pyhop(state2, [('pointing', 'satellite4', 'Planet9'),
                         ('have_image', 'Planet5', 'image4'),
                         ('have_image', 'Star6', 'infrared3'),
                         ('have_image', 'Star7', 'image4'),
                         ('have_image', 'Phenomenon8', 'image4'),
                         ('have_image', 'Planet9', 'infrared0'),
                         ('have_image', 'Planet10', 'infrared3'),
                         ('have_image', 'Star12', 'image4'),
                         ('have_image', 'Phenomenon13', 'image4'),
                         ('have_image', 'Phenomenon14', 'spectrograph1'),
                         ('have_image', 'Star15', 'spectrograph1'),
                         ('have_image', 'Star16', 'image2')], verbose=1)
