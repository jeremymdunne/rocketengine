from os import path
import matplotlib.pyplot as plt
import rocketengine



if __name__ == '__main__':
    # test the parser
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "rocketengine", "resources", "enginefiles", "Cesaroni_9955M1450-P.eng"))
    enginedata = rocketengine.parser.parseEngineFile(filepath)
    print(enginedata)


    # test the interpolator
    enginedata = rocketengine.interpolate.interpolateEngineData(enginedata)

    plt.plot(enginedata['thrust data']['time'], enginedata['thrust data']['mass'])
    plt.show()
    print(enginedata)

    """
    time = []
    thrust = []
    for i in range(0, 700, 1):
        time.append(i/100)
        thrust.append(rocketengine.interpolate.getEngineThrust(i/100, enginedata))

    plt.plot(time, thrust)
    plt.show()
    """
    print('Total Impulse: ', rocketengine.interpolate.calcImpulse(enginedata))
