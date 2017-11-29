#import matplotlib.pyplot as PYPlot
import sys
import numpy as NUM_PY


# Uncomment for local machine
# def PlottingThePoints(Xaxis, Yaxis, weights):
#
#     for index in xrange(Xaxis.shape[0]):
#         if Yaxis[index] == 1:
#             PYPlot.plot(Xaxis[index, 0], Xaxis[index, 1], 'ro')
#         else:
#             PYPlot.plot(Xaxis[index, 0], Xaxis[index, 1], 'bx')
#
#     x_axis_min = Xaxis.min(axis=0)
#     x_axis_max = Xaxis.max(axis=0)
#
#     x_x = [x_axis_min[0] - 1, x_axis_max[0] + 1]
#     y_y = -(weights[2] + weights[0] * x_x) / weights[1]
#     PYPlot.plot(x_x, y_y, 'k')
#     PYPlot.axis([x_axis_min[0] - 1, x_axis_max[0] + 1, x_axis_min[1] - 1, x_axis_max[1] + 1])
#     PYPlot.show()


def checkAndReturn(x):
    return 1 if x > 0 else -1


def PPerceptronLearningAlgo(X_Sample, Y_label, output_file_result, graphics=False):
    data = X_Sample.shape[1]
    weights = NUM_PY.zeros((data + 1, 1))
    convergence = False

    open(output_file_result, 'w').close()
    while not convergence:
        convergence = True
        for index in xrange(X_Sample.shape[0]):
            if Y_label[index]*checkAndReturn(weights[-1] + NUM_PY.dot(X_Sample[[index], :], weights[:-1, [0]])) <= 0:
                weights[-1] = weights[-1] + Y_label[index]
                weights[:-1, [0]] = weights[:-1, [0]] + Y_label[index] * NUM_PY.transpose(X_Sample[[index], :])
                convergence = False

        # if graphics:
        #     PlottingThePoints(X_Sample, Y_label, weights)
    
        with open(output_file_result, "a") as output_text_file:
            for weightIdx in weights:
                if weightIdx[0].is_integer():
                    output_text_file.write(str(int(weightIdx[0])) + ",")
                else:
                    output_text_file.write(str(weightIdx[0]) + ",")
            output_text_file.write("\n")

    return weights

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python <input.csv> <output.csv> or python input1.csv output1.csv'
        sys.exit(0)

    sample_dataset = NUM_PY.genfromtxt(sys.argv[1], delimiter=',', skip_header=0, names=None)

    X_data = sample_dataset[:, [0, 1]]
    y_label = sample_dataset[:, [2]]

    # for debug set as True else False
    PPerceptronLearningAlgo(X_data, y_label, sys.argv[2], False)
