import sys
sys.path.append('C:\\Users\\user\\PycharmProjects\\anaStruct')

from anastruct.fem.system import SystemElements
import xlwings as xw

kNODE = 'NODE'
kID = 'ID'
kX_COORD, kY_COORD = ('X_COORD', 'Y_COORD')
kFIX_X, kFIX_Y, kFIX_R = ('FIX_X', 'FIX_Y', 'FIX_R')

kELEM = 'ELEM'
kNODE1, kNODE2 = ('NODE1', 'NODE2')
kPIN1, kPIN2 = ('PIN1', 'PIN2')
kSEC = 'SEC'

kNODAL_LOAD = 'NODAL_LOAD'
kNODE_ID = 'NODE_ID'
kP_X, kP_Y, kM = ('P_X', 'P_Y', 'M')

kSEC_PROP = 'SEC_PROP'
kE, kA, kI = ('E', 'A', 'I')


def _get_keyword_cell(sht, keyword, max_row=500, offset=0):
    """keywordが入力されている最初のセルを返す
    デフォルトでは、A列を１行目から探す。他の列を探す場合は、offsetで指定"""
    for i in range(1, max_row):
        # openpyxl
        # current_cell = sht.cell(row=i, column=1 + offset)
        # xlwings
        current_cell = sht.range(i,1+offset)
        if current_cell.value == keyword:
            return current_cell
    raise 'KEYWORD NOT FOUND ERROR'


def _get_param_list(sht, cell):
    """cell位置の右側にある、パラメーターのリストを返す。
    空のセルの手前までを範囲とする。"""
    res = []
    r = cell.row
    # openpyxl
    # c = cell.col_idx
    # xlwings
    c = cell.column
    inc = 1
    # while sht.cell(row=r, column=c + inc).value:
    while sht.range(r, c+inc).value:
        # res.append(sht.cell(row=r, column=c + inc).value)
        res.append(sht.range(r, c + inc).value)
        inc += 1
    return res


def _get_data_num(sht, cell):
    """データの数（行数）を返す。
    最初のパラメーターのデータには空欄がないことを仮定している"""
    r = cell.row
    # c = cell.col_idx
    c = cell.column
    inc = 1
    # data = sht.cell(row=r + inc, column=c + 1).value
    data = sht.range(r + inc, c + 1).value
    while data:
        inc += 1
        # data = sht.cell(row=r + inc, column=c + 1).value
        data = sht.range(r + inc, c + 1).value
    return inc


def get_data_group(sht, key_word, max_row=500, offset=0):
    """key_wordで指定したデータ群をdictで返す
    """
    cell = _get_keyword_cell(sht, key_word, max_row, offset)
    params = _get_param_list(sht, cell)
    res = {}
    data_list = []
    r = cell.row
    # c = cell.col_idx
    c = cell.column
    data_num = _get_data_num(sht, cell)
    for i, param_name in enumerate(params):
        for inc in range(1, data_num):
            # data_list.append(sht.cell(row=r + inc, column=c + i + 1).value)
            data_list.append(sht.range(r + inc, c + i + 1).value)
        res[param_name] = data_list
        data_list = []
    return res


def get_data(data, key_src, val, key_target):
    """dataから　必要なデータを取り出し、返す"""
    return data[key_target][data[key_src].index(val)]


def get_params(sht, key_word, max_row=500, offset=0):
    """key_wordで指定したデータ群のパラメーター一覧をリストで返す"""
    cell = _get_keyword_cell(sht, key_word, max_row, offset)
    return _get_param_list(sht, cell)

#------------------------------------
def generate_model():
    ws = xw.sheets.active
    mdl = SystemElements()

    node_dic = get_data_group(ws, kNODE)
    elem_dic = get_data_group(ws, kELEM)
    sec_dic = get_data_group(ws, kSEC_PROP)
    nld_dic = get_data_group(ws, kNODAL_LOAD)
    for idx in elem_dic[kID]:
        s_node_id = get_data(elem_dic, kID, idx, kNODE1)
        e_node_id = get_data(elem_dic, kID, idx, kNODE2)
        sec_id = get_data(elem_dic, kID, idx, kSEC)
        s_pt = [get_data(node_dic, kID, s_node_id, kX_COORD), get_data(node_dic, kID, s_node_id, kY_COORD)]
        e_pt = [get_data(node_dic, kID, e_node_id, kX_COORD), get_data(node_dic, kID, e_node_id, kY_COORD)]
        E = get_data(sec_dic, kID, sec_id, kE)
        A = get_data(sec_dic, kID, sec_id, kA)
        I = get_data(sec_dic, kID, sec_id, kI)
        # add element data
        mdl.add_element([[s_pt[0], s_pt[1]], [e_pt[0], e_pt[1]]], EA=E*A, EI=E*I)

    for nid in nld_dic[kNODE_ID]:
        px = get_data(nld_dic, kNODE_ID, nid, kP_X)
        py = get_data(nld_dic, kNODE_ID, nid, kP_Y)
        m = get_data(nld_dic, kNODE_ID, nid, kM)
        if px or py:
            mdl.point_load(int(nid), px, py)
        if m:
            mdl.moment_load(int(nid),m)

    pin_support_node_ids = []
    roller_x_support_node_ids = []
    roller_y_support_node_ids = []
    fixed_support_node_ids = []
    for nid in node_dic[kID]:
        if get_data(node_dic, kID, nid, kFIX_R):
            fixed_support_node_ids.append(nid)
        fix_x = get_data(node_dic, kID, nid, kFIX_X)
        fix_y = get_data(node_dic, kID, nid, kFIX_Y)
        if fix_x and fix_y:
            pin_support_node_ids.append(nid)
        elif fix_x and not (fix_y):
            roller_y_support_node_ids.append(nid)
        elif fix_y and not (fix_x):
            roller_x_support_node_ids.append(nid)
    for nid in pin_support_node_ids:
        mdl.add_support_hinged(int(nid))

    for nid in roller_x_support_node_ids:
        mdl.add_support_roll(int(nid))

    for nid in roller_y_support_node_ids:
        mdl.add_support_roll(int(nid),direction=1)
    for nid in fixed_support_node_ids:
        mdl.add_support_fixed(int(nid))

    #show model
    w = 500
    h = 300
    # fig = mdl.show_structure(show = False,verbosity=0)
    ws.pictures.add(mdl.show_structure(show = False), name = 'fig_model', update=True,width=w,height=h)

    #solve
    mdl.solve()
    ws.pictures.add(mdl.show_bending_moment(show = False), name = 'fig_moment', update=True,width=w,height=h)
    ws.pictures.add(mdl.show_axial_force(show = False), name = 'fig_axial', update=True,width=w,height=h)
    ws.pictures.add(mdl.show_displacement(show = False), name = 'fig_disp', update=True,width=w,height=h)


def solve_model():
    sht = xw.Book.caller().sheets.active
    # add new model
    mdl = SystemElements()

    x2 = sht.range('A2').value
    x3 = sht.range('B2').value

    # add beam element
    mdl.add_element([[0, 0], [x2, 0]], EA=50, EI=100)
    mdl.add_element([[x2, 0], [x3, 0]], EA=50, EI=100)

    # add nodal load
    mdl.point_load(2, 0, -10)

    # support setting
    mdl.add_support_hinged(1)
    mdl.add_support_roll(3)

    # output plot
    mdl.solve()
    w=300
    h=200
    fig_model = mdl.show_structure(show=False)
    sht.pictures.add(fig_model,name="fig_model",update=True,left = 0,top=0,width=w,height=h)

    fig_moment = mdl.show_bending_moment(show=False)
    sht.pictures.add(fig_moment,name="fig_moment",update=True,left = w+100,top=0,width=w,height=h)

    fig_shear = mdl.show_shear_force(show=False)
    sht.pictures.add(fig_shear,name='fig_shear',update=True,left = 0,top=h+50,width=w,height=h)


    fig_disp = mdl.show_displacement(show=False)
    sht.pictures.add(fig_disp,name='fig_disp',update=True,left = w+100,top=h+50,width=w,height=h)


if __name__ == '__main__':
    pass

# ------------------------------------
