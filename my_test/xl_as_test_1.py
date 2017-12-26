import sys
sys.path.append('C:\\Users\\user\\PycharmProjects\\anaStruct')

from anastruct.fem.system import SystemElements
import xlwings as xw


def test_model():
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

def test_model2():
    # sht = xw.Book.caller().sheets.active
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

    fig_model = mdl.show_structure(verbosity=0, scale=1,show=False)
    # sht.pictures.add(fig_model,name="fig_model",update=True)
    print(fig_model)

    fig_moment = mdl.show_bending_moment(verbosity=0, scale=1,show=False)
    # sht.pictures.add(fig_moment,name="fig_moment",update=True)
    print(fig_moment)

    fig_shear = mdl.show_shear_force(show=False)
    # sht.pictures.add(fig_shear,name='fig_shear',update=True)
    print(fig_shear)

    fig_disp = mdl.show_displacement(verbosity=0, scale=1,show=False)
    # sht.pictures.add(fig_disp,name='fig_disp',update=True)
    print(fig_disp)

if __name__ == '__main__':
    test_model2()
