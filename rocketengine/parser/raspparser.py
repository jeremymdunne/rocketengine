def parseRaspFile(filepath):
    headerpassed = False

    data = {
        'motor name':None,
        'motor diameter':None,
        'motor length':None,
        'motor delay': None,
        'propellant weight': None,
        'total weight': None,
        'manufacturer': None,
        'thrust data': {'time':[],'thrust':[]}
    }

    with open(filepath) as enginefile:
        while True:
            line = enginefile.readline()
            if not line:
                break
            if not headerpassed:
                if line[0].isalpha():
                    headerpassed = True
                    name, diam, length, delay, prop_weight, total_weight, manufacturer = parseRaspHeader(line)
                    data['motor name'] = name
                    data['motor diameter'] = diam
                    data['motor length'] = length
                    data['motor delay'] = delay
                    data['propellant weight'] = prop_weight
                    data['total weight'] = total_weight
                    data['manufacturer'] = manufacturer
            else:
                try:
                    time, thrust = parseRaspDataLine(line)
                    data['thrust data']['time'].append(time)
                    data['thrust data']['thrust'].append(thrust)
                except:
                    break
    enginefile.close()
    return data

def parseRaspDataLine(line):
    # first float is the time
    # second is the thrust (N)
    contents = line.split()
    time = float(contents[0])
    thrust = float(contents[1])
    return time, thrust

def parseRaspHeader(header):
    # the content of the header is as follows:
    # 1. Motor Name
    # 2. Motor Diameter
    # 3. Motor Length
    # 4. Motor Delay
    # 5. Propellant Weight
    # 6. Total Weight
    # 7. Manufacturer

    # parse by spaces
    headercontents = header.split()
    motor_name = headercontents[0]
    motor_diameter = float(headercontents[1])
    motor_length = float(headercontents[2])
    motor_delay = float(headercontents[3])
    propellant_weight = float(headercontents[4])
    total_weight = float(headercontents[5])
    manufacturer = headercontents[6]

    return motor_name, motor_diameter, motor_length, motor_delay, propellant_weight, total_weight, manufacturer
