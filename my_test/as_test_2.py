from anastruct.fem.system import SystemElements

# add new model
mdl = SystemElements()

# add beam element
mdl.add_element([[0, 0], [0, 4]], EA=50, EI=10)
mdl.add_element([[0, 4], [6, 4]], EA=50, EI=10)
mdl.add_element([[6, 4], [6, 0]], EA=50, EI=10)

# add nodal load
mdl.point_load(2, 5, 0)
mdl.point_load(3, 5, 0)

# support setting
mdl.add_support_fixed(1)
mdl.add_support_fixed(4)
# output plot
mdl.solve()

mdl.show_structure(verbosity=0, scale=1)
mdl.show_bending_moment(verbosity=0, scale=1)
mdl.show_shear_force()
mdl.show_displacement(verbosity=0, scale=1)

print('{:-^80}'.format('Nodal Result'))

node_res = mdl.get_node_results_system()
for x in node_res:
    print('NodeID={:5} ,Fx={:8.3f} ,Fz={:8.3f} ,Ty={:8.3f} ,ux={:8.3f} ,uz={:8.3f} ,phi_y={:8.3f}'.format(*x))

print('{:-^80}'.format('Elemental Result'))

elem_list = mdl.element_map.keys()

for x in elem_list:
    a = mdl.get_element_results(x)
    try:
        print('ElemID={id:5},  L={length:8.3f}, N_1={N_1:8.3f}  ,N_2={N_2:8.3f}  ,Mmin={Mmin:8.3f}  ,Mmax={Mmax:8.3f}'
              ''.format(**a))
    except KeyError:
        print('ElemID={id:5},  L={length:8.3f}, N_1={N_1:8.3f}  ,N_2={N_2:8.3f} '.format(**a))
