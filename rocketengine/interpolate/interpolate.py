import copy


def interpolateEngineData(enginedata):
    # open and interpolate estimated mass data at varying times
    # return a dict with all data
    enginedata['thrust data']['mass'] = []
    # add a 0,0 time place
    if enginedata['thrust data']['time'][0] != 0:
        enginedata['thrust data']['thrust'].insert(0,0)
        enginedata['thrust data']['time'].insert(0,0)
    for i in enginedata['thrust data']['time']:
        enginedata['thrust data']['mass'].append(getEngineMass(i,enginedata))
    return enginedata

def getEngineData(time, enginedata):
    # return thrust, mass at the time
    thrust = getEngineThrust(enginedata)
    mass = getEngineMass(enginedata)
    return thrust, mass

def getEngineThrust(time, enginedata):
    # return thrust at the time
    if time <= 0:
        return 0
    if time > enginedata['thrust data']['time'][-1]:
        return 0
    thrust = interpolate(time, enginedata['thrust data']['time'], enginedata['thrust data']['thrust'])
    return thrust

def getEngineMass(time, enginedata):
    # return mass at the time
    # get the total impulse
    total_impulse = calcImpulse(enginedata)
    print('total impulse ', total_impulse)
    # get the impulse so far
    spent_impulse = calcImpulse(enginedata, endtime = time)
    print('spent impulse ', spent_impulse)
    mass = enginedata['total weight'] - enginedata['propellant weight'] + (enginedata['propellant weight'] / total_impulse) * (total_impulse - spent_impulse)
    return mass 

def calcImpulse(enginedata, endtime = None, starttime = None):
    print('endtime ', endtime)
    print('starttime ',starttime)
    # return impulse between the time steps
    thrust_data = copy.deepcopy(enginedata['thrust data'])
    if starttime is not None and starttime > 0:
        # add in new starting point and delete the rest
        for i in range(0,len(thrust_data['time'])):
            if starttime <= thrust_data['time'][i]:
                # delete up to the data before
                thrust_data['time'] = thrust_data['time'][i:]
                thrust_data['thrust'] = thrust_data['thrust'][i:]
                # add in new point
                thrust_data['time'].insert(0,starttime)
                thrust_data['thrust'].insert(0,getEngineThrust(starttime,enginedata))
                break
    # remove after
    if endtime is not None and endtime < thrust_data['time'][-1]:
        for i in range(len(thrust_data['time'])-1,-1,-1):
            if endtime >= thrust_data['time'][i]:
                # insert new point
                thrust_data['time'].insert(i,endtime)
                thrust_data['thrust'].insert(i,getEngineThrust(endtime,enginedata))
                # delete the excess
                thrust_data['time'] = thrust_data['time'][:(i+1)]
                thrust_data['thrust'] = thrust_data['thrust'][:(i+1)]
                break
    print(thrust_data)

    # trapezoidal integration
    impulse = 0
    if len(thrust_data['time']) > 1:
        for i in range(0,len(thrust_data['time'])-1):
            impulse += (thrust_data['thrust'][i+1] + thrust_data['thrust'][i]) / 2 * (thrust_data['time'][i+1] - thrust_data['time'][i])
    return impulse

def interpolate(x, xdata, ydata):
    # perform simple linear interpolation for now
    n = 0
    for i in range(0, len(xdata) - 1):
        if x <= xdata[i+1]:
            n = i
            break
    if x > xdata[-1]:
        n = len(xdata) - 2

    # print('n ',n)
    # print('x ',x)
    # print('x data', xdata)

    interp = (ydata[n] * (xdata[n+1] - x) + ydata[n+1]*(x - xdata[n])) / (xdata[n+1] - xdata[n])
    return interp
