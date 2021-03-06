##############################################################################
##############################################################################
# Example code for Newton type maximum likelihood parameter inference
# in ninlinear state space models using particle methods.
#
# Please cite:
#
# M. Kok, J. Dahlin, T. B. Sch\"{o}n and A. Wills,
# "Newton-based maximum likelihood estimation in nonlinear state space models.
# Proceedings of the 17th IFAC Symposium on System Identification,
# Beijing, China, October 2015.
#
# (c) 2015 Johan Dahlin
# johan.dahlin (at) liu.se
#
# Distributed under the MIT license.
#
##############################################################################
##############################################################################


#=============================================================================
# Model structure
#=============================================================================
# xtt = atan( xt ) + self.par[3] * vt;
# yt  = self.par[0] * xt + self.par[1] + self.par[2] * et;
#
# vt  ~ N(0,1)
# et  ~ N(0,1)

import numpy          as     np
from   scipy.stats    import norm
from   models_helpers import *

class ssm(object):

    #=========================================================================
    # Define model settings
    #=========================================================================
    nPar         = 4;
    par          = np.zeros(nPar);
    modelName    = "Example 1 in SYSID-paper on Newton optimisation";
    filePrefix   = "newton_sysid2015_example1";
    supportsFA   = False;
    nParInfernce = None;
    nQInference  = None;

    #=========================================================================
    # Define the model
    #=========================================================================
    def generateInitialState( self, nPart ):
        return np.random.normal(size=(1,nPart));

    def generateState(self, xt, tt):
        return np.arctan( xt ) + self.par[3] * np.random.randn(1,len(xt));

    def evaluateState(self, xtt, xt, tt):
        return norm.pdf( xtt, np.arctan( xt ), self.par[3] );

    def generateObservation(self, xt, tt):
        return self.par[0] * xt + self.par[1] + self.par[2] * np.random.randn(1,len(xt));

    def evaluateObservation(self,  xt, tt):
        return norm.logpdf(self.y[tt], self.par[0] * xt + self.par[1], self.par[2] );

    #=========================================================================
    # Define gradients of logarithm of complete data-likelihood
    #=========================================================================
    def Dparm(self, xtt, xt, st, at, tt):

        nOut = len(xtt);
        gradient = np.zeros(( nOut, self.nParInference ));
	R2       = self.par[2]**(-2.0)
	py       = self.y[tt] - self.par[0]*xt - self.par[1];

        for v1 in range(0,self.nParInference):
            if v1 == 0:
                gradient[:,v1] = xt * py * R2;
            elif v1 == 1:
                gradient[:,v1] = py * R2;
            else:
                gradient[:,v1] = 0.0;
        return(gradient);

    #=========================================================================
    # Define Hessians of logarithm of complete data-likelihood
    #=========================================================================
    def DDparm(self, xtt, xt, st, at, tt):
        nOut = len(xtt);
        hessian = np.zeros( (nOut, self.nParInference,self.nParInference) );
        return(hessian);

    def priorUniform(self):
        return( 0.0 );

    #=========================================================================
    # Define standard methods for the model struct
    #=========================================================================

    # Standard operations on struct
    copyData                = template_copyData;
    storeParameters         = template_storeParameters;
    returnParameters        = template_returnParameters

    # Standard data generation for this model
    generateData            = template_generateData;

    # Simple priors for this model
    prior                   = empty_prior;
    dprior1                 = empty_dprior1
    ddprior1                = empty_ddprior1

##############################################################################
##############################################################################
# End of file
##############################################################################
##############################################################################