#import matplotlib.pyplot as PYPlot
import numpy as NUM_PY
import sys
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


def load_sample_data(input_file_for_processing):
    loadedDataSet = NUM_PY.genfromtxt(input_file_for_processing, delimiter=',', skip_header=0, names=None)
    X_axis = loadedDataSet[:, :-1]
    Y_axis = loadedDataSet[:, [-1]]
    return (X_axis, Y_axis)


def pre_process_data_samples(X_data_samples):

    XTempData = NUM_PY.copy(X_data_samples)

    mutual = NUM_PY.mean(XTempData, axis=0)
    StdEnv = NUM_PY.std(XTempData, axis=0)

    XTempData = (XTempData - mutual) / StdEnv

    XCalculatedNewValue = NUM_PY.ones((XTempData.shape[0], XTempData.shape[1] + 1))

    XCalculatedNewValue[:, 1:X_data_samples.shape[1] + 1] = XTempData

    return XCalculatedNewValue


def calculationOfRisk(X_Data, y_label, beta_value):
    return NUM_PY.linalg.norm(NUM_PY.dot(X_Data, beta_value) - y_label) ** 2

def AlgorithumGradientDescent(X_Data, Y_label, alpha_value, verbose_track=False, iterations_maximum=100):

    totalNumber = X_Data.shape[0]
    beta_value = NUM_PY.zeros((X_Data.shape[1], 1))

    for index in xrange(iterations_maximum):
        beta_value = beta_value - alpha_value / float(totalNumber) * NUM_PY.dot(NUM_PY.transpose(X_Data), NUM_PY.dot(X_Data, beta_value) - Y_label)

        risk = calculationOfRisk(X_Data, Y_label, beta_value)
        if verbose_track:
            print "Looping total num: %d, with the risk : %.6f" % (index + 1, risk)


    return (beta_value, index + 1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python <input.csv> <output.csv> or pythong input2.csv output2.csv '
        sys.exit(0)
    X_value, y_lable = load_sample_data(sys.argv[1])
    XData_Sample = pre_process_data_samples(X_value)


    open(sys.argv[2], 'w').close()

    for alphaIndex in [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]:
        with open(sys.argv[2], "a") as readFromText_file:
            betaData, iterationsOnloop = AlgorithumGradientDescent(XData_Sample, y_lable, alphaIndex)
            readFromText_file.write(str(alphaIndex) + "," + str(iterationsOnloop) + ",")

            readFromText_file.write(','.join(['%.5f' % num for num in betaData]))

            readFromText_file.write('\n')

    alphaIndex = 0.08
    with open(sys.argv[2], "a") as readFromText_file:
        betaData, iterationsOnloop = AlgorithumGradientDescent(XData_Sample, y_lable, alphaIndex, False, 1000)
        readFromText_file.write(str(alphaIndex) + "," + str(iterationsOnloop) + ",")
        readFromText_file.write(','.join(['%.5f' % num for num in betaData]))
        readFromText_file.write('\n')

    #figureOnPyplot = PYPlot.figure()
    #axes3Dmagic = Axes3D(figureOnPyplot)

  #  X_axis1, X_axis2 = NUM_PY.meshgrid(X_value[:, 0], X_value[:, 1])
    #axes3Dmagic.scatter(X_value[:, 0], X_value[:, 1], y_lable)

   # X_axis1_paralel, X_axis2_parallel = NUM_PY.meshgrid(XData_Sample[:, 1], XData_Sample[:, 2])

   # axes3Dmagic.plot_surface(X_axis1, X_axis2, betaData[0] + betaData[1] * X_axis1_paralel + betaData[2] * X_axis2_parallel, rstride=4, cstride=4, alpha=0.4, cmap=cm.jet)
   # axes3Dmagic.set_zlabel('Height (Meters)')
   # axes3Dmagic.set_ylabel('Weight (Kilograms)')
   # axes3Dmagic.set_xlabel('Age (Years)')

   # PYPlot.show()

