from copy import deepcopy
from CSP_algo import *

class Queue:
    def __init__(self):
        self.queue = []

    def isEmpty(self):
        return len(self.queue) == 0

    def enqueue(self, e):
        self.queue.append(e)

    def dequeue(self):
        return self.queue.pop(0)

    def __len__(self):
        return len(self.queue)

class CSP_Algo:
    def __init__(self, domain, binary_constraints, unassigned_vars):
        self.customDomain = domain
        self.binary_constraintsRules = binary_constraints
        self.unassigned_variables
        self.empty

    def getNeighbors__(self):
        raise NotImplementedError

    def getUnassignedNotCompletedVariables(self):
        raise NotImplementedError

    def assignVariable_SetTheCell(self, var, value):
        raise NotImplementedError

    def checkTheConstraints(self):
        raise NotImplementedError

def AC3_Algo(CSP_Algo):
    queues_loc = Queue()
    queues_loc.queue = list(CSP_Algo.binary_constraintsRules)

    while not queues_loc.isEmpty():
        (__i, __j) = queues_loc.dequeue()
        if ReOrderTheCspAlgo(CSP_Algo, __i, __j):
            if len(CSP_Algo.customDomain[__i]) == 0:
                return False
            for __ij in CSP_Algo.getNeighbors__(__i, __j):
                queues_loc.enqueue((__ij, __i))
           
    return True

def ReOrderTheCspAlgo(csp_algo, __i, __j):
    revisedStatus = False
    for __eachdoamin in csp_algo.customDomain[__i]:
        isSatisfy = False
        for __jcostom in csp_algo.customDomain[__j]:
            if __eachdoamin != __jcostom:
                isSatisfy = True
                break
        if not isSatisfy:
            csp_algo.customDomain[__i].remove(__eachdoamin)
            revisedStatus = True
    return revisedStatus

def frontCheck(csp_algo, vari__, tempValue):
    variables__loc = list(csp_algo.getUnassignedNotCompletedVariables())
    if vari__ in variables__loc:
        variables__loc.remove(vari__)

    for eachVariable in variables__loc:
        for eachValue in list(csp_algo.customDomain[eachVariable]):
            csp_algo.assignVariable_SetTheCell(eachVariable, eachValue)
            if not csp_algo.checkTheConstraints():
                csp_algo.customDomain[eachVariable].remove(eachValue)
            if len(csp_algo.customDomain[eachVariable]) == 0:
                return False
        if len(csp_algo.customDomain[eachVariable]) == 1:
            csp_algo.assignVariable_SetTheCell(eachVariable, csp_algo.customDomain[eachVariable][0])
        else:
            csp_algo.assignVariable_SetTheCell(eachVariable, csp_algo.emptyFor)

    return True

def BackCheckS(csp_algo):
    return BackCheckTracking({}, csp_algo)

def BackCheckTracking(inputValueAssignment, csp_algo, inference=frontCheck):

    variables_local = list(csp_algo.getUnassignedNotCompletedVariables())
    for eachKey in inputValueAssignment.keys():
        if eachKey in variables_local:
            variables_local.remove(eachKey)

    if len(variables_local) == 0:
        return inputValueAssignment

    infinityMax = float('Inf')
    vari__ = None
    for eachLockVar in variables_local:
        if len(csp_algo.customDomain[eachLockVar]) < infinityMax:
            infinityMax = len(csp_algo.customDomain[eachLockVar])
            vari__ = eachLockVar

    for eachCustomDoVar in csp_algo.customDomain[vari__]:
        tempCspAlgo = deepcopy(csp_algo)
        tempCspAlgo.assignVariable_SetTheCell(vari__, eachCustomDoVar)
        tempCspAlgo.unassigned_variables.remove(vari__)
        if tempCspAlgo.checkTheConstraints():
            inputValueAssignment[vari__] = eachCustomDoVar
            inferencesLocal = []
            if inference(tempCspAlgo, vari__, eachCustomDoVar):
                for eachLockVar in list(tempCspAlgo.getUnassignedNotCompletedVariables()):
                    if len(tempCspAlgo.customDomain[eachLockVar]) == 1:
                        inputValueAssignment[eachLockVar] = tempCspAlgo.customDomain[eachLockVar][0]
                        inferencesLocal.append(eachLockVar)

                resultFinalCheck = BackCheckTracking(inputValueAssignment, tempCspAlgo)
                if resultFinalCheck != False:
                    return resultFinalCheck

            inputValueAssignment.pop(vari__, None)
            for eachLockVar in inferencesLocal:
                inputValueAssignment.pop(eachLockVar, None)

    return False

