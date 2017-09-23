from anastruct.fem.system import SystemElements

# トラスモデルのテスト その２

# add new model
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


# text output =============================
print('{:-^80}'.format('Nodal Result') )
# node_res = ss.get_node_displacements()

node_res = ss.get_node_results_system()

for x in node_res:
    print('ID:{:5}  ,Fx:{:8.3f}  ,Fz:{:8.3f}  ,ux:{:8.3f}  ,uy:{:8.3f}  ,phi_y:{:8.3f}'.format(*x))


print('{:-^80}'.format('Elemental Result') )
elem_list = ss.element_map.keys()

for x in elem_list:
    a = ss.get_element_results(x)
    # print(a)
    try:
        print('ID:{id:5},  L:{length:8.3f}, N_1:{N_1:8.3f}  ,N_2:{N_2:8.3f}  ,Mmin:{Mmin:8.3f}  ,Mmax:{Mmax:8.3f}'.format(**a))
    except KeyError:
        print('ID:{id:5},  L:{length:8.3f}, N_1:{N_1:8.3f}  ,N_2:{N_2:8.3f} '.format(**a))

