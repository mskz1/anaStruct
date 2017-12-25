import sys
sys.path.append('C:\\Users\\user\\PycharmProjects\\anaStruct')

from anastruct.fem.system import SystemElements
import xlwings as xw


def test_model():
    sht = xw.Book.caller().sheets.active
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

    # fig_model = mdl.show_structure(verbosity=0, scale=1,show=False)
    # sht.pictures.add(fig_model,name="fig_model",update=True)

    fig_moment = mdl.show_bending_moment(verbosity=0, scale=1,show=False)
    sht.pictures.add(fig_moment,name="fig_moment",update=True)
    #
    # fig_shear = mdl.show_shear_force(show=False)
    # sht.pictures.add(fig_shear,name='fig_shear',update=True)
    #
    #
    # fig_disp = mdl.show_displacement(verbosity=0, scale=1,show=False)
    # sht.pictures.add(fig_disp,name='fig_disp',update=True)
