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


def _get_keyword_cell(sht, keyword, max_row=50, offset=0):
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


def get_data_group(sht, key_word, max_row=50, offset=0):
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


def get_params(sht, key_word, max_row=50, offset=0):
    """key_wordで指定したデータ群のパラメーター一覧をリストで返す"""
    cell = _get_keyword_cell(sht, key_word, max_row, offset)
    return _get_param_list(sht, cell)

# ------------------------------------
if __name__ == '__main__':
    # ws = xw.apps[0].books['frame_model.xlsx'].sheets['sheet1']
    ws = xw.sheets.active
    # print(get_params(ws, 'NODE'))
    #
    # node_dic = get_data_group(ws, 'NODE')
    # print(node_dic)
    #
    # elem_dic = get_data_group(ws, 'ELEM')
    #
    # print(get_params(ws, 'ELEM'))
    # print(elem_dic)
    #
    print('読み込みデータ-----------------')
    node_dic = get_data_group(ws, kNODE)
    print('NODE data as dict', '-' * 30)
    print(node_dic)
    print('-' * 30)

    elem_dic = get_data_group(ws, kELEM)

    print('ELEM data as dict', '-' * 30)
    print(elem_dic)
    print('-' * 30)

    sec_dic = get_data_group(ws, kSEC_PROP)
    print('SEC_PROP data as dict', '-' * 30)
    print(sec_dic)
    print('-' * 30)

    nld_dic = get_data_group(ws, kNODAL_LOAD)
    print('NODAL_LOAD data as dict', '-' * 30)
    print(nld_dic)
    print('-' * 30)

    print('整形データ')
    print('=' * 30)
    print('Element Definition', '-' * 30)
    for idx in elem_dic[kID]:
        s_node_id = get_data(elem_dic, kID, idx, kNODE1)
        e_node_id = get_data(elem_dic, kID, idx, kNODE2)
        sec_id = get_data(elem_dic, kID, idx, kSEC)
        s_pt = [get_data(node_dic, kID, s_node_id, kX_COORD), get_data(node_dic, kID, s_node_id, kY_COORD)]
        e_pt = [get_data(node_dic, kID, e_node_id, kX_COORD), get_data(node_dic, kID, e_node_id, kY_COORD)]
        E = get_data(sec_dic, kID, sec_id, kE)
        A = get_data(sec_dic, kID, sec_id, kA)
        I = get_data(sec_dic, kID, sec_id, kI)
        print('elem_id={}, coord=({},{})-({},{}), E={}, A={}, I={}'.format(
            idx, s_pt[0], s_pt[1], e_pt[0], e_pt[1], E, A, I))

    print('Nodal Load Definition', '-' * 20)
    for nid in nld_dic[kNODE_ID]:
        px = get_data(nld_dic, kNODE_ID, nid, kP_X)
        py = get_data(nld_dic, kNODE_ID, nid, kP_Y)
        m = get_data(nld_dic, kNODE_ID, nid, kM)
        print('Load applied Node id={}, Px={}, Py={}, M={}'.format(nid, px, py, m))

    print('Fixed Node Definition', '-' * 20)
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
    print('Pin supported node ids =', pin_support_node_ids)
    print('Roller(x) supported node ids =', roller_x_support_node_ids)
    print('Roller(y) supported node ids =', roller_y_support_node_ids)
    print('Fixed supported node ids = ', fixed_support_node_ids)
