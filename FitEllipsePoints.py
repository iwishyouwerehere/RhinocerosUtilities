#https://discourse.mcneel.com/t/fit-ellipse-through-points/168208

import json
import numpy as np
from numpy.linalg import eig, inv

with open(Points.json', 'r') as file:
    points_data = json.load(file)

x = [p['X'] for p in points_data]
y = [p['Y'] for p in points_data]

def fit_ellipse(x, y):
    x, y = np.array(x), np.array(y)
    D = np.vstack([x**2, x*y, y**2, x, y, np.ones_like(x)]).T
    S = np.dot(D.T, D)
    C = np.zeros([6, 6])
    C[0, 2] = C[2, 0] = 2; C[1, 1] = -1
    E, V = eig(np.dot(inv(S), C))
    n = np.argmax(E)
    a = V[:, n]
    return a

ellipse_params = fit_ellipse(x, y)

# conic equation Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0
# for ellipse, we need B^2 - 4AC < 0 (for a real ellipse)

A, B, C, D, E, F = ellipse_params
is_ellipse = B**2 - 4*A*C < 0

is_ellipse, ellipse_params.tolist() 
