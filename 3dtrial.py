# -*- coding: utf-8 -*-
"""
Created on Sun May 10 18:07:49 2015

@author: Wipp's
"""

import plotly.plotly as py
from plotly.graph_objs import *
# auto sign-in with credentials or use py.sign_in()
trace1 = Scatter3d(
        x=[1,2,3],
        y=[3,4,5],
        z=[1,3,4])
data = Data([trace1])
py.plot(data)