
    
def calcPSD(t1, accelA, speedA, speedB, carLengthA, carLengthB, clearanceAB, clearanceBA, verbose = False):
    dist1 = t1*speedB+(pow(speedA,2)-pow(speedB,2))/(2*accelA)
    if verbose: print 'dist1:\t%0.2f meters\t(%0.2f feet)' % (dist1, dist1*METERtoFEET)

    t2 = float(carLengthA + carLengthB + clearanceAB + clearanceBA) / (speedA - speedB)
    dist2 = t2 * speedA
    if verbose: print 'dist2:\t%0.2f meters\t(%0.2f feet)' % (dist2, dist2*METERtoFEET)

    dist3 = 2.5*carLengthA  # 70 meters
    if verbose: print 'dist3:\t%0.2f meters\t(%0.2f feet)' % (dist3, dist3*METERtoFEET)

    dist4 = 2./3 * speedA * t2
    if verbose: print 'dist4:\t%0.2f meters\t(%0.2f feet)' % (dist4, dist4*METERtoFEET)    

    psd = dist1 + dist2 + dist3 + dist4
    if verbose: print 'psd:\t%0.2f meters\t(%0.2f feet)' % (psd, psd*METERtoFEET)

    return psd
    

# http://www.webpages.uidaho.edu/niatt_labmanual/chapters/geometricdesign/exampleproblems/PassingSightDistance.htm
MPHtoMPS    = 0.44704   # miles per hour to meters per second
METERtoFEET = 3.28084
t1 = 2.5; accelA = 1.47*MPHtoMPS
speedA = 60.*MPHtoMPS; speedB = 50.*MPHtoMPS
carLengthA = 22./METERtoFEET; carLengthB = carLengthA
clearanceAB = 20./METERtoFEET; clearanceBA = clearanceAB

calcPSD(t1, accelA, speedA, speedB, carLengthA, carLengthB, clearanceAB, clearanceBA, verbose = True)

# car
t1 = 0.; accelA = 10.
speedA = 16.; speedB = 15.
carLengthA = 30.; carLengthB = carLengthA
clearanceAB = 10.; clearanceBA = clearanceAB

calcPSD(t1, accelA, speedA, speedB, carLengthA, carLengthB, clearanceAB, clearanceBA, verbose = True)

