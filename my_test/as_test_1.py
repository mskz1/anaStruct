from anastruct.fem.system import SystemElements

# add new model
mdl = SystemElements()

# add beam element
mdl.add_element([[0, 0], [6, 0]], EA=50, EI=100)
mdl.add_element([[6, 0], [8, 0]], EA=50, EI=100)

# add nodal load
mdl.point_load(2, 0, -10)

# support setting
mdl.add_support_hinged(1)
mdl.add_support_roll(3)

# output plot
mdl.solve()
w,h = 5,4
# mdl.show_structure(verbosity=0, scale=1,figsize=(w,h))
# mdl.show_bending_moment(verbosity=0, scale=1,figsize=(w,h))
# mdl.show_shear_force(figsize=(w,h))
# mdl.show_displacement(verbosity=0, scale=1,figsize=(w,h))

print('{:-^80}'.format('Nodal Result') )
node_res = mdl.get_node_results_system()
print(node_res)

for x in node_res:
    print('NodeID={:5} ,Fx={:8.3f} ,Fz={:8.3f} ,Ty={:8.3f} ,ux={:8.3f} ,uz={:8.3f} ,phi_y={:8.3f}'.format(*x))

print('-----')
print(mdl.get_node_results_system(node_id=2))


print('{:-^80}'.format('Elemental Result') )

elem_list = mdl.element_map.keys()

for x in elem_list:
    a = mdl.get_element_results(x)
    try:
        print('ElemID={id:5},  L={length:8.3f}, N_1={N_1:8.3f}  ,N_2={N_2:8.3f}  ,Mmin={Mmin:8.3f}  ,Mmax={Mmax:8.3f}'.format(**a))
    except KeyError:
        print('ElemID={id:5},  L={length:8.3f}, N_1={N_1:8.3f}  ,N_2={N_2:8.3f} '.format(**a))
