import math

omega = {"K0":0,
         "M0":0.33,
         "R0":0,
         "L0":0.67}
H0 = 1

def hubbleRatio(z):
    """This is an example of a function."""
    return H0 *  math.sqrt(omega["K0"] * (1+z)**2 + 
                           omega["M0"] * (1+z)**3 + 
                           omega["R0"] * (1+z)**4 + 
                           omega["L0"])

if __name__=="__main__":
    def assertAlmostEqual(a, b, epsilon=1e-6):
        assert abs(a-b) < epsilon

    assert 1 == sum(omega.values())
    assertAlmostEqual(hubbleRatio(0), H0)
