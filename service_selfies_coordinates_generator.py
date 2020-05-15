import os
from api import req


while 1:
    data = req('get_service_selfies_coordinates_generator')
    print(data)