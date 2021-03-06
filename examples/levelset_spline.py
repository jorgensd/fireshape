import firedrake as fd
import fireshape.zoo as fsz
# import sys
# sys.path.append("/Users/paalbert/Documents/FIREDRAKE/fireshape")
import fireshape as fs
import ROL
import math

#n = 100
#mesh = fd.UnitSquareMesh(n, n)
n = 20
mesh = fd.UnitCubeMesh(n, n, n)

inner = fs.H1InnerProduct()#LaplaceInnerProduct()
bbox = [(-3, 4), (-3, 4), (-3,4)]
orders = [2, 2, 2]
levels = [3, 3, 3]
Q = fs.BsplineControlSpace(mesh, inner, bbox, orders, levels)
q = fs.ControlVector(Q)

mesh_m = Q.mesh_m
#(x, y) = fd.SpatialCoordinate(mesh_m)
#f = (pow(x-0.5, 2))+pow(y-0.5, 2) - 2.
(x, y, z) = fd.SpatialCoordinate(mesh_m)
f = (pow(x-0.5, 2))+pow(y-0.5, 2)+pow(z-0.5, 2) - 2.

out = fd.File("domain.pvd")

def cb():
    out.write(mesh_m.coordinates)

cb()
J = fsz.LevelsetFunctional(f, Q, cb=cb)

#params_dict = {
#    'General': {
#        'Secant': { 'Type': 'Limited-Memory BFGS', 'Maximum Storage': 25 } },
#    'Step': {
#        'Type': 'Line Search',
#        'Line Search': { 'Descent Method': { 'Type': 'Quasi-Newton Step' } }
#    },
#    'Status Test': {
#        'Gradient Tolerance': 1e-15, 'Relative Gradient Tolerance': 1e-10,
#        'Step Tolerance': 1e-16, 'Relative Step Tolerance': 1e-10,
#        'Iteration Limit': 150 }
#}

params_dict = {
    'General': {
        'Secant': {'Type': 'Limited-Memory BFGS',
                   'Maximum Storage': 25}},
    'Step': {
        'Type': 'Line Search',
        'Line Search': {'Descent Method': {
            'Type': 'Quasi-Newton Step'}}},
    'Status Test': {
        'Gradient Tolerance': 1e-7,
        'Relative Gradient Tolerance': 1e-6,
        'Step Tolerance': 1e-10, 'Relative Step Tolerance': 1e-10,
        'Iteration Limit': 150}}

params = ROL.ParameterList(params_dict, "Parameters")
problem = ROL.OptimizationProblem(J, q)
solver = ROL.OptimizationSolver(problem, params)
solver.solve()
