import string

from anastruct.fem.system import SystemElements

# トラスモデルのテスト

# add new model
# mdl = se.SystemElements(xy_cs=False)
ss = SystemElements()

# add beam element
# lower chord
ss.add_element([[0, 0], [1, 0]], EA=200, EI=1000)
ss.add_element([[1, 0], [2, 0]], EA=200, EI=1000)
ss.add_element([[2, 0], [3, 0]], EA=200, EI=1000)
ss.add_element([[3, 0], [4, 0]], EA=200, EI=1000)

# upper chord
ss.add_element([[0.5, 1], [1.5, 1]], EA=200, EI=1000)
ss.add_element([[1.5, 1], [2.5, 1]], EA=200, EI=1000)
ss.add_element([[2.5, 1], [3.5, 1]], EA=200, EI=1000)

# web
ss.add_truss_element([[0, 0], [0.5, 1]], EA=100)
ss.add_truss_element([[0.5, 1], [1, 0]], EA=100)

ss.add_truss_element([[1, 0], [1.5, 1]], EA=100)
ss.add_truss_element([[1.5, 1], [2, 0]], EA=100)

ss.add_truss_element([[2, 0], [2.5, 1]], EA=100)
ss.add_truss_element([[2.5, 1], [3, 0]], EA=100)

ss.add_truss_element([[3, 0], [3.5, 1]], EA=100)
ss.add_truss_element([[3.5, 1], [4, 0]], EA=100)

# add nodal load
ss.point_load(6, 0, -5)
ss.point_load(7, 0, -5)
ss.point_load(8, 0, -5)
ss.point_load(9, 0, -5)

# support setting
ss.add_support_hinged(1)
ss.add_support_roll(5)

# output plot
ss.solve()

ss.show_structure(verbosity=0, scale=1)

ss.show_reaction_force()
ss.show_axial_force()
ss.show_bending_moment(verbosity=0, scale=1)
ss.show_displacement(verbosity=0, scale=1)

print('{:-^80}'.format('Nodal Result') )
# node_res = ss.get_node_displacements()

node_res = ss.get_node_results_system()

for x in node_res:
    print(x)

# print(x for x in node_res)
# print(ss.get_node_displacements(2))
# print(ss.get_node_displacements(3))

print('{:-^80}'.format('Elemental Result') )
elem_list = ss.element_map.keys()
for x in elem_list:
    print(ss.get_element_results(x))

# print(ss.get_element_results(1,verbose=False))
# print(ss.get_element_results(2,verbose=False))
