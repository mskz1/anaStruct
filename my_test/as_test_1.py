from anastruct.fem.system import SystemElements

# add new model
mdl = SystemElements()

# add beam element
mdl.add_element([[0, 0], [2, 0]], EA=50, EI=100)
mdl.add_element([[2, 0], [4, 0]], EA=50, EI=100)

# add nodal load
mdl.point_load(2, 0, -10)

# support setting
mdl.add_support_hinged(1)
mdl.add_support_roll(3)

# output plot
mdl.solve()

mdl.show_structure(verbosity=0, scale=1)
mdl.show_bending_moment(verbosity=0, scale=1)
mdl.show_shear_force()
mdl.show_displacement(verbosity=0, scale=1)

print('{:-^80}'.format('Nodal Result') )
# print('{:-<80}'.format('Nodal Result'))
# print(mdl.get_node_displacements())
# for x in mdl.get_node_results_system():
#	print(x)


node_res = mdl.get_node_results_system()
for x in node_res:
    # print(x)
    print('NodeID={:5} ,Fx={:8.3f} ,Fz={:8.3f} ,Ty={:8.3f} ,ux={:8.3f} ,uz={:8.3f} ,phi_y={:8.3f}'.format(*x))
# print(mdl.get_node_displacements(2))
# print(mdl.get_node_displacements(3))

# print(mdl.get_element_results(1,verbose=False))
# print(mdl.get_element_results(2,verbose=False))
print('{:-^80}'.format('Elemental Result') )
# for x in mdl.get_element_results():
#     print(x)
#

elem_list = mdl.element_map.keys()

for x in elem_list:
    a = mdl.get_element_results(x)
    # print(a)
    try:
        print('ElemID={id:5},  L={length:8.3f}, N_1={N_1:8.3f}  ,N_2={N_2:8.3f}  ,Mmin={Mmin:8.3f}  ,Mmax={Mmax:8.3f}'.format(**a))
    except KeyError:
        print('ElemID={id:5},  L={length:8.3f}, N_1={N_1:8.3f}  ,N_2={N_2:8.3f} '.format(**a))
