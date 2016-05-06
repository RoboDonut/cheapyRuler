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
        
    def __init__(self,lat,units):
        """Constructor"""
        m = factors[units]
        cos = math.cos(lat * math.pi / 180);
        cos2 = 2 * cos * cos - 1;
        cos3 = 2 * cos * cos2 - cos;
        cos4 = 2 * cos * cos3 - cos2;
        cos5 = 2 * cos * cos4 - cos3;
        #multipliers for converting longitude and latitude degrees into distance (http://1.usa.gov/1Wb1bv7)
        self.kx = m * (111.41513 * cos - 0.09455 * cos3 + 0.00012 * cos5);
        self.ky = m * (111.13209 - 0.56605 * cos2 + 0.0012 * cos4);
        
    
    def distance(self,a,b):
        ''' Distance between points'''
        dx = (a[0] - b[0]) * self.kx
        dy = (a[1] - b[1]) * self.ky
        return math.sqrt(dx * dx + dy * dy)
    
    def destination(self,p,dist,bearing):
        '''new point from point distance and bearing'''
        a = (90 - bearing) * math.pi / 180
        return [p[0] + math.cos(a) * dist / self.kx,
            p[1] + math.sin(a) * dist / self.ky]
    
    def bearing(self,a,b):
        '''bearing to from point to point'''
        dx = (b[0] - a[0]) * self.kx
        dy = (b[1] - a[1]) * self.ky
        if dx == 0 and dy == 0:
            return 0
        bearing = math.atan2(-dy, dx) * 180 / math.pi + 90
        if bearing > 180:
            bearing -= 360
        return bearing
    
    def lineDistance(self,points):
        '''length of a line'''
        total = 0
        i = 0
        while i < len(points) - 1:
            total += self.distance(points[i], points[i + 1])
            i+=1        
        return total
    
    
    
    
    #helper functions
    def equals(self,a,b):
        '''Check equality of a point'''
        if a[0]==b[0] and a[1]==b[1]:
            return True
        else:
            return False
        
    def interpolate(self,a,b,t):
        '''interpolate a new point'''
        dx = b[0]-a[0]
        dy = b[1]-a[1]
        return [a[0]+dx*t, a[1]+dy*t]