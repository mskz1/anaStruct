from anastruct.fem.system import SystemElements

# トラスモデルのテスト その4
# FAP検証モデル
# 座標値が小数点の時、微小な差異で別節点となってしまう。節点を先に生成することで対処


TRUSS_SPAN = 10.
TRUSS_DEPTH = 1.5
NUM_OF_PANEL = 5

EA_CHORD = 20500.
EI_CHORD = 0.205

EA_WEB = 20500.
EI_WEB = 0.205

ss = SystemElements()

del_x = TRUSS_SPAN / NUM_OF_PANEL

# upper node
u_node = []
x = 0.
u_node.append([x, 0])
for i in range(NUM_OF_PANEL):
    x += del_x
    u_node.append([x, 0])

# lower node
l_node = []
x = del_x / 2
l_node.append([x, -TRUSS_DEPTH])
for i in range(NUM_OF_PANEL - 1):
    x += del_x
    l_node.append([x, -TRUSS_DEPTH])

# upper chord member
for i in range(NUM_OF_PANEL):
    # ss.add_truss_element([u_node[i],u_node[i+1]],EA=EA_CHORD)
    ss.add_element([u_node[i], u_node[i + 1]], EA=EA_CHORD, EI=EI_CHORD)
    # ss.add_element([u_node[i],u_node[i+1]], EA=EA_CHORD, EI=EI_CHORD,spring={1: 0,2:0})

# lower chord member
for i in range(NUM_OF_PANEL - 1):
    # ss.add_truss_element([l_node[i],l_node[i+1]],EA=EA_CHORD)
    ss.add_element([l_node[i], l_node[i + 1]], EA=EA_CHORD, EI=EI_CHORD)
    # ss.add_element([l_node[i],l_node[i+1]], EA=EA_CHORD, EI=EI_CHORD,spring={1: 0,2:0})

# web member
for i in range(NUM_OF_PANEL):
    # ss.add_truss_element([u_node[i],l_node[i]],EA=EA_WEB)
    # ss.add_truss_element([l_node[i],u_node[i+1]],EA=EA_WEB)
    ss.add_element([u_node[i],l_node[i]], EA=EA_WEB, EI=EI_WEB)
    ss.add_element([l_node[i],u_node[i+1]], EA=EA_WEB, EI=EI_WEB)
    # ss.add_element([u_node[i], l_node[i]], EA=EA_WEB, EI=EI_WEB, spring={1: 0, 2: 0})
    # ss.add_element([l_node[i], u_node[i + 1]], EA=EA_WEB, EI=EI_WEB, spring={1: 0, 2: 0})

# support
ss.add_support_hinged(1)
ss.add_support_roll(NUM_OF_PANEL + 1)

# point load
for i in range(NUM_OF_PANEL + 1):
    ss.point_load(i + 1, 0, -10)

# output plot
ss.solve()
fsize=(12,6)
ss.show_structure(figsize=fsize)
ss.show_reaction_force(figsize=fsize)
ss.show_axial_force(factor = 0.004,figsize=fsize)
ss.show_bending_moment(figsize=fsize)
ss.show_displacement(figsize=fsize)

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

    # print('{:-^80}'.format('DEBUG OUT'))
    # for i in ss.node_map.keys():
    #     print(ss.node_map[i])
    # print('NodeID={id} ,X={x:16.4f} ,Y={y:16.4f}'.format(ss.node_map[i]))
