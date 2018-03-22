#!/usr/bin/python
# -*- coding: utf-8 -*-

## Modified version of the BVH importer borrowed from the makehuman project
## some parts borrowed from bvhplay


"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers, Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2012

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

BVH importer
"""

# Libraries from makehuman
from aljabr import vadd, makeUnit, degree2rad, makeTranslation, mmul, euler2matrix

# Standard libraries
from math import radians, cos, sin, pi
import math

# Numpy
from numpy import array, dot

from joint import Joint

class Skeleton:
    
    def __init__(self, filename, scale):
        
        self.file = open(filename, 'r')

        # Read hierarchy
        self.__expectKeyword('HIERARCHY')
            
        items = self.__expectKeyword('ROOT')
        
        self.root = Joint(items[1])
        
        self.__readJoint(self.root, scale)
            
        # Read motion
        self.__expectKeyword('MOTION')
        
        items = self.__expectKeyword('Frames:')
        self.frames = int(items[1])
        items = self.__expectKeyword('Frame') # Time:
        self.frameTime = float(items[2])

        for i in range(self.frames):
            line = self.file.readline()
            items = line.split()
            data = [float(item) for item in items]
            data = self.__getChannelData(self.root, data)
                
    def getJoint(self, name):
        
        return self.__getJoint(self.root, name)
        
    def __getJoint(self, joint, name):
        
        if joint.name == name:
            return joint
            
        for child in joint.children:
            j = self.__getJoint(child, name)
            if j:
                return j
                
        return None

    def __calcPosition(self, joint, scale):
        # Get OFFSET
        items = self.__expectKeyword('OFFSET')
        joint.offset = [scale*float(x) for x in items[1:]]
        joint.strans = joint.offset[:]
        joint.stransmat[0,3] = joint.strans[0]
        joint.stransmat[1,3] = joint.strans[1]
        joint.stransmat[2,3] = joint.strans[2]
        
        if joint.parent:
            joint.position = vadd(joint.parent.position, joint.offset)
        else:
            joint.position = joint.offset[:]

        # Calculate static transformation matrix
        joint.stransmat = array([ [1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.] ])
        joint.stransmat[0,3] = joint.offset[0]
        joint.stransmat[1,3] = joint.offset[1]
        joint.stransmat[2,3] = joint.offset[2]
                
    def __readJoint(self, joint, scale=0.25):
        
        self.__expectKeyword('{')

        self.__calcPosition(joint, scale)
        
        items = self.__expectKeyword('CHANNELS')
        joint.channels = items[2:]
        joint.parseChannels(items[2:])

        if int(items[1]) != len(joint.channels):
            RuntimeError('Expected %d channels found %d' % (items[1], len(joint.channels)))
        
        # Read child joints
        while 1:
            line = self.file.readline()
            items = line.split()
            
            if items[0] == 'JOINT':
                
                child = Joint(items[1])
                joint.children.append(child)
                child.parent = joint
                self.__readJoint(child, scale)
                
            elif items[0] == 'End': # Site
                
                child = Joint('End effector')
                joint.children.append(child)
                child.channels = []
                child.parent = joint
                
                self.__expectKeyword('{')

                self.__calcPosition(child, scale)
                
                self.__expectKeyword('}')
                
            elif items[0] == '}':
                
                break
                
            else:
                
                raise RuntimeError('Expected %s found %s' % ('JOINT, End Site or }', items[0]))
                    
    def __expectKeyword(self, keyword):
        
        line = self.file.readline()
        items = line.split()
        
        if items[0] != keyword:
            raise RuntimeError('Expected %s found %s' % (keyword, items[0]))
                
        return items


    def __getChannelData(self, joint, data):
        
        channels = len(joint.channels)
        joint.frames.append(data[0:channels])
        data = data[channels:]
        
        for child in joint.children:
            data = self.__getChannelData(child, data)
        
        return data
        
    def updateFrame(self, frame, scale = 1):
        self.root.updateFrame(frame, scale)
