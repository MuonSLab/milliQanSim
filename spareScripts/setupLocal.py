#!/usr/bin/env python

import subprocess
import os
import shutil
import sys

jobNumber = int(sys.argv[1])
proc = str(sys.argv[2]) # Sample, mCP_UFO, JPsi, Y1S, Y2S, Y3S, cosmicmuons, beammuons, Cs137gamma


#massDict = {
#    'mCP_UFO' : [0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7], #mCP masses
#    'cosmicmuons' : [0.105],
#    'beammuons' : [0.105]
#}

#charges = [0.01, 0.02, 0.05, 0.07, 0.1, 0.14, 0.2, 0.3] #mCP charges

configFile = 'particles'
nCores = 1

# Rescale the y or z position for the direction of the particle gun
yRescale = 1.
zRescale = 1.

########################################################################
# Define masses/charges based on chosen process
########################################################################

#masses = massDict[proc]

if proc == 'beammcp':
    nEv = 10000
    particle = 'monopole'
    mass = 0.01
    #masses[jobNumber / len(charges)]
    charge = 0.005
    #charges[jobNumber % len(charges)]
    sourcename = 'output_1.txt'
#    sourcename = 'mCP_UFO_v7/' + proc + '/' + str(mass) + '/' + str(charge) + '/hit_4_vecs.txt'
    macname = 'runMac/mcp_novis.mac' 
    outputname = proc + '.' + str(mass) + 'GeV.' + str(charge) + 'Q.' + str(jobNumber)

if proc == 'beammuons':
    mass = 0.105
    charge = 1.000
    nEv = 5
    particle = 'mu-'
    sourcename = 'muon_hit_4_vecs.txt'
    macname = 'runMac/mcp_novis.mac' 
    outputname = proc + '.' + str(jobNumber)

if proc == 'cosmicmuons':
    mass = 0.105
    charge = 1.000
    nEv = 100
    particle = 'mu-'
    macname = 'runMac/specmuon45_no_vis.mac'
    outputname = proc + '.' + str(jobNumber)

if proc == 'Cs137gamma':
    mass = 0
    charge = 0
    nEv = 1000
    particle = 'gamma'
    macname = 'runMac/Cs137gamma1C.mac'
    outputname = proc + '.' + str(jobNumber)


########################################################################
# Change values in configuration files
########################################################################

print outputname, nEv
#if   charge < 0.0030: nEv = 25000
#elif charge < 0.0050: nEv = 10000
#elif charge < 0.0090: nEv = 1000
#elif charge < 0.0200: nEv = 400
#elif charge < 0.0500: nEv = 100
#elif charge < 0.2000: nEv = 50
#else: nEv = 20

#if   charge < 0.0100: sourcecharge = 0.001
#elif charge < 0.1000: sourcecharge = 0.01
#else: sourcecharge = 0.1

#Define names
#os.mkdir('milliQanBuild')
#os.chdir('milliQanBuild')
#subprocess.call('tar -xvf ../mqDemoSim.tar', shell = True)

projectDir = os.getcwd() + '/'
#scratch directory for condor
#outputdir = projectDir + '../'
#outputdir = '/hadoop/cms/store/user/ryan/' + proc + '/'

os.chdir(projectDir + 'build')

if proc != 'cosmicmuons' and proc != 'Cs137gamma':
    subprocess.call('sed -i "s/^yParticleGunRescale.*/yParticleGunRescale = ' + str(yRescale) + '/g" config/particles.ini', shell = True)
    subprocess.call('sed -i "s/^zParticleGunRescale.*/zParticleGunRescale = ' + str(zRescale) + '/g" config/particles.ini', shell = True)
    subprocess.call('sed -i "s/^ElectricCharge.*/ElectricCharge = ' + str(charge) + '/g" config/particles.ini', shell = True)
    subprocess.call('sed -i "s/^MonopoleMass.*/MonopoleMass = ' + str(mass) + '/g" config/particles.ini', shell = True)
    subprocess.call('sed -i "s/^Particle.*/Particle = ' + particle + '/g" config/particles.ini', shell = True)
    subprocess.call('sed -i "s|FileName.*|FileName = ' + sourcename + '|g" config/particles.ini', shell = True)
    subprocess.call('sed -i "s|PathName.*|PathName = ' + projectDir + '|g" config/particles.ini', shell = True)
    subprocess.call('sed -i "s|.*new MilliQPrimaryGeneratorAction.*|   runManager->SetUserAction(new MilliQPrimaryGeneratorAction(pt,eventOffset));|g" ' + projectDir + 'MilliQan.cc', shell = True)
    subprocess.call('sed -i "s|.*new mqPrimaryGeneratorAction.*|   //runManager->SetUserAction(new mqPrimaryGeneratorAction(detector));|g" ' + projectDir + 'MilliQan.cc', shell = True)

if proc == 'beammcp':
    subprocess.call('sed -i "s|.*if(eventInformation->GetPMTHits.*| //if(eventInformation->GetPMTHits()->size()){ |g" ' + projectDir + 'src/mqEventAction.cc', shell = True)
    subprocess.call('sed -i "s|.*if(true).*| if(true){ |g" ' + projectDir + 'src/mqEventAction.cc', shell = True)
    mustring = "\\\"mu\\\""
    monopolestring = "\\\"monopole\\\""
    subprocess.call('sed -i "s|.*mumonopole.*|                 //if(particleName.contains('+mustring+') //mumonopole |g" ' + projectDir + 'src/mqSteppingAction.cc', shell = True)
    subprocess.call('sed -i "s|.*monopolemu.*|                 if(particleName.contains('+monopolestring+') //monopolemu |g" ' + projectDir + 'src/mqSteppingAction.cc', shell = True)
    
if proc == 'beammuons':
    subprocess.call('sed -i "s|.*if(eventInformation->GetPMTHits.*| //if(eventInformation->GetPMTHits()->size()){ |g" ' + projectDir + 'src/mqEventAction.cc', shell = True)
    subprocess.call('sed -i "s|.*if(true).*| if(true){ |g" ' + projectDir + 'src/mqEventAction.cc', shell = True)
    subprocess.call('sed -i "s|.*mumonopole.*|                 if(particleName.contains(\\"mu\\") //mumonopole |g" ' + projectDir + 'src/mqSteppingAction.cc', shell = True)
    subprocess.call('sed -i "s|.*monopolemu.*|                 //if(particleName.contains(\\"monopole\\") //monopolemu |g" ' + projectDir + 'src/mqSteppingAction.cc', shell = True)

if proc == 'cosmicmuons':
    subprocess.call('sed -i "s|.*new MilliQPrimaryGeneratorAction.*|   //runManager->SetUserAction(new MilliQPrimaryGeneratorAction(pt,eventOffset));|g" ' + projectDir + 'MilliQan.cc', shell = True)
    subprocess.call('sed -i "s|.*new mqPrimaryGeneratorAction.*|   runManager->SetUserAction(new mqPrimaryGeneratorAction(detector));|g" ' + projectDir + 'MilliQan.cc', shell = True)
    subprocess.call('sed -i "s|.*if(eventInformation->GetPMTHits.*| if(eventInformation->GetPMTHits()->size()){ |g" ' + projectDir + 'src/mqEventAction.cc', shell = True)
    subprocess.call('sed -i "s|.*if(true).*| //if(true){ |g" ' + projectDir + 'src/mqEventAction.cc', shell = True)
    subprocess.call('sed -i "s|.*mumonopole.*|                 if(particleName.contains(\\"mu\\") //mumonopole |g" ' + projectDir + 'src/mqSteppingAction.cc', shell = True)
    subprocess.call('sed -i "s|.*monopolemu.*|                 //if(particleName.contains(\\"monopole\\") //monopolemu |g" ' + projectDir + 'src/mqSteppingAction.cc', shell = True)

if proc == 'Cs137gamma':
    subprocess.call('sed -i "s|.*new MilliQPrimaryGeneratorAction.*|   //runManager->SetUserAction(new MilliQPrimaryGeneratorAction(pt,eventOffset));|g" ' + projectDir + 'MilliQan.cc', shell = True)
    subprocess.call('sed -i "s|.*new mqPrimaryGeneratorAction.*|   runManager->SetUserAction(new mqPrimaryGeneratorAction(detector));|g" ' + projectDir + 'MilliQan.cc', shell = True)
    subprocess.call('sed -i "s|.*if(eventInformation->GetPMTHits.*| if(eventInformation->GetPMTHits()->size()){ |g" ' + projectDir + 'src/mqEventAction.cc', shell = True)
    subprocess.call('sed -i "s|.*if(true).*| //if(true){ |g" ' + projectDir + 'src/mqEventAction.cc', shell = True)
    subprocess.call('sed -i "s|.*mumonopole.*|                 if(particleName.contains(\\"gamma\\") //mumonopole |g" ' + projectDir + 'src/mqSteppingAction.cc', shell = True)
    subprocess.call('sed -i "s|.*monopolemu.*|                 //if(particleName.contains(\\"monopole\\") //monopolemu |g" ' + projectDir + 'src/mqSteppingAction.cc', shell = True)
    
subprocess.call('sed -i "s/.*beamOn.*/\/run\/beamOn ' + str(nEv) + '/g" ' + projectDir + macname, shell = True)
subprocess.call('sed -i "s|.*fname.*|/run/fname ' + projectDir + 'data' + proc + '/tempdir' + str(jobNumber) + '/|g" ' + projectDir + macname, shell = True)


########################################################################
#Run Program
########################################################################
#useful if just running locally to rebuild automatically
subprocess.call('cmake ..', shell = True)
subprocess.call('make -j4', shell = True)
#subprocess.call('tar -cvf mqDemoSim.tar build/ runMac/ OpticalData/ datacosmicmuons/ databeammuons/ muon_hit_4_vecs.txt')
#shutil.move('mqDemoSim.tar','condor')
#subprocess.call('./MilliQan ' + projectDir + macname, shell = True)

#shutil.move(projectDir + 'data' + proc + '/tempdir' + str(jobNumber) + '/MilliQan.root', outputdir + outputname + '.root')
#subprocess.call('gfal-copy -pft 4200 --verbose file://' + projectDir + 'data' + proc + '/tempdir' + str(jobNumber) + '/MilliQan.root gsiftp://gftp.t2.ucsd.edu' + outputdir + outputname + '.root', shell = True)
#gfal-copy -pft 4200 --verbose file://${PROJECTDIR}/data$2/tempdir$1/MilliQan.root gsiftp://gftp.t2.ucsd.edu${OUTPUTDIR}$2"."$1".root"

#os.chdir('../../')
#subprocess.call('rm -r milliQanBuild', shell = True)
#subprocess.call('rm mqDemoSim.tar', shell = True)
