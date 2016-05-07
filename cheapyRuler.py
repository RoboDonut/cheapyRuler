#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Daniel Smith --<>
  Purpose: Python Port of Mapbox Cheap Ruler (https://github.com/mapbox/cheap-ruler)
  Credits: @mourner,@anandthakker
  Created: 5/5/2016
"""

import math

factors = {'kilometers': 1,
        'miles': 1000 / 1609.344,
        'nauticalmiles': 1000 / 1852,
        'meters': 1000,
        'metres': 1000,
        'yards': 1000 / 0.9144,
        'feet': 1000 / 0.3048,
        'inches': 1000 / 0.0254}

########################################################################
class cheapyRuler():
    """python port of mapbox cheap ruler. not all functions are available"""

    #----------------------------------------------------------------------
        
    def __init__(self,lat=None,units=None):
        """Constructor"""
        m = factors[units]
        _cos = math.cos(lat * math.pi / 180);
        cos2 = 2 * _cos * _cos - 1;
        cos3 = 2 * _cos * cos2 - cos;
        cos4 = 2 * _cos * cos3 - cos2;
        cos5 = 2 * _cos * cos4 - cos3;
        #multipliers for converting longitude and latitude degrees into distance (http://1.usa.gov/1Wb1bv7)
        self.kx = m * (111.41513 * _cos - 0.09455 * cos3 + 0.00012 * cos5);
        self.ky = m * (111.13209 - 0.56605 * cos2 + 0.0012 * cos4);
        
    
    def distance(self,first_point=None,second_point=None):
        ''' Distance between points'''
        dx = (first_point[0] - second_point[0]) * self.kx
        dy = (first_point[1] - second_point[1]) * self.ky
        return math.sqrt(dx * dx + dy * dy)
    
    def destination(self,p,distance=None,bearing=None):
        '''new point from point distance and bearing'''
        a = (90 - bearing) * math.pi / 180
        return [p[0] + math.cos(a) * distance / self.kx,
            p[1] + math.sin(a) * distance / self.ky]
    
    def bearing(self,first_point=None,second_point=None):
        '''bearing to from point to point'''
        dx = (second_point[0] - first_point[0]) * self.kx
        dy = (second_point[1] - first_point[1]) * self.ky
        if dx == 0 and dy == 0:
            return 0
        bearing = math.atan2(-dy, dx) * 180 / math.pi + 90
        if bearing > 180:
            bearing -= 360
        return bearing
    
    def lineDistance(self,points=None):
        '''length of a line'''
        total = 0
        i = 0
        while i < len(points) - 1:
            total += self.distance(points[i], points[i + 1])
            i+=1        
        return total
    
    
    
    
    #helper functions
    def equals(self,first_point=None,second_point=None):
        '''Check equality of a point'''
        if first_point[0]==second_point[0] and first_point[1]==second_point[1]:
            return True
        else:
            return False
        
    def interpolate(self,first_point=None,second_point=None,t=None):
        '''interpolate a new point'''
        dx = second_point[0]-first_point[0]
        dy = second_point[1]-first_point[1]
        return [first_point[0]+dx*t, first_point[1]+dy*t]