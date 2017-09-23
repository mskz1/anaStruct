from anastruct.fem.system import SystemElements

# トラスモデルのテスト その２

#TODO 座標値が小数点の時、微小な差異で別節点となってしまう。


TRUSS_SPAN = 10.
TRUSS_DEPTH = 1.8
NUM_OF_PANEL = 6

EA_CHORD = 200.
EI_CHORD = 1000.

EA_WEB = 200.
EI_WEB = 1000.

ss = SystemElements()

del_x = TRUSS_SPAN / NUM_OF_PANEL
# upper chord member
p1 = [0, 0]
p2 = [0, 0]
for i in range(NUM_OF_PANEL):
    p2[0] = p1[0] + del_x
    # ss.add_element([p1, p2], EA=EA_CHORD, EI=EI_CHORD)
    ss.add_truss_element([p1, p2], EA=EA_CHORD)
    p1 = p2[:]

# lower chord member
p1 = [0.5 * del_x, -TRUSS_DEPTH]
p2 = [0, -TRUSS_DEPTH]
for i in range(NUM_OF_PANEL - 1):
    p2[0] = p1[0] + del_x
    # ss.add_element([p1, p2], EA=EA_CHORD, EI=EI_CHORD)
    ss.add_truss_element([p1, p2], EA=EA_CHORD)
    p1 = p2[:]

# web member
p1 = [0, 0]
p2 = [0, -TRUSS_DEPTH]
for i in range(NUM_OF_PANEL):
    p2[0] = p1[0] + 0.5 * del_x
    # ss.add_element([p1, p2], EA=EA_WEB, EI=EI_WEB)
    ss.add_truss_element([p1, p2], EA=EA_WEB)
    x1 = p1[0]
    p1[0] = x1 + del_x
    # ss.add_element([p2, p1], EA=EA_WEB, EI=EI_WEB)
    ss.add_truss_element([p2, p1], EA=EA_WEB)

# support
ss.add_support_hinged(1)
ss.add_support_roll(NUM_OF_PANEL + 1)

# point load
for i in range(NUM_OF_PANEL + 1):
    ss.point_load(i + 1, 0, -10)

# output plot
ss.solve()

ss.show_structure()

ss.show_reaction_force()
ss.show_axial_force()
ss.show_bending_moment()
ss.show_displacement()

# text output =============================
print('{:-^80}'.format('Nodal Result'))

node_res = ss.get_node_results_system()

for x in node_res:
    print('NodeID={:5} ,Fx={:8.3f} ,Fz={:8.3f} ,Ty={:8.3f} ,ux={:8.3f} ,uz={:8.3f} ,phi_y={:8.3f}'.format(*x))

print('{:-^80}'.format('Elemental Result'))
elem_list = ss.element_map.keys()

for x in elem_list:
    a = ss.get_element_results(x)
    # print(a)
    try:
        print(
            'ElemID={id:5} ,L={length:8.3f} ,N1={N_1:8.3f} ,N2={N_2:8.3f} ,Mmin={Mmin:8.3f} ,Mmax={Mmax:8.3f}'.format(
                **a))
    except KeyError:
        print('ElemID={id:5} ,L={length:8.3f} ,N1={N_1:8.3f} ,N2={N_2:8.3f}'.format(**a))

print('{:-^80}'.format('DEBUG OUT'))
for i in ss.node_map.keys():
    print(ss.node_map[i])
    # print('NodeID={id} ,X={x:16.4f} ,Y={y:16.4f}'.format(ss.node_map[i]))
