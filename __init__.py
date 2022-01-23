'''
PyAdjust
Author: Manoel Victor Frutuoso Barrionuevo
Contact: manoelvfb@live.ca
Date: 23/01/2022
'''

from __future__ import absolute_import
from __future__ import print_function
from os import path

# Avoid importing "expensive" modules here (e.g. scipy), since this code is
# executed on PyMOL's startup. Only import such modules inside functions.

def __init_plugin__(app=None):
    '''
    Add an entry to the PyMOL "Plugin" menu
    '''
    from pymol.plugins import addmenuitemqt
    addmenuitemqt('PyAdjust', run_plugin_gui)


# global reference to avoid garbage collection of our dialog
dialog = None

def run_plugin_gui():
    '''
    Open our custom dialog
    '''
    global dialog

    if dialog is None:
        dialog = make_dialog()

    dialog.show()

def make_dialog():
    from pymol import cmd
    from numpy import array, linalg
    from pymol.Qt import QtWidgets
    from pymol.Qt.utils import loadUi
    from pymol.Qt.utils import getSaveFileNameWithExt
    
    dialog = QtWidgets.QDialog()

    uifile = path.join(path.dirname(__file__), 'pyadjust.ui')
    form = loadUi(uifile, dialog)

    def draw_PBC():
        from pymol.cgo import LINEWIDTH, BEGIN, LINES, \
                              COLOR, VERTEX, END
        cell = array([[form.ax.value(), form.ay.value(), form.az.value()], \
                      [form.bx.value(), form.by.value(), form.bz.value()], \
                      [form.cx.value(), form.cy.value(), form.cz.value()]], \
                     dtype = float)

        b_yx = cell[0] + cell[1]
        t_zx = cell[0] + cell[2]
        t_zy = cell[1] + cell[2]
        t_yx = cell.sum(axis = 0)

        PBC_BOX = [ \
            LINEWIDTH, 1, BEGIN, LINES, \
            COLOR, 0., 0., 0., \

            VERTEX, 0.0, 0.0, 0.0, \
            VERTEX, cell[0, 0], cell[0, 1], cell[0, 2], \

            VERTEX, 0.0, 0.0, 0.0, \
            VERTEX, cell[1, 0], cell[1, 1], cell[1, 2], \

            VERTEX, 0.0, 0.0, 0.0, \
            VERTEX, cell[2, 0], cell[2, 1], cell[2, 2], \

            VERTEX, cell[0, 0], cell[0, 1], cell[0, 2], \
            VERTEX, b_yx[0], b_yx[1], b_yx[2], \

            VERTEX, cell[1, 0], cell[1, 1], cell[1, 2], \
            VERTEX, b_yx[0], b_yx[1], b_yx[2], \

            VERTEX, cell[2, 0], cell[2, 1], cell[2, 2], \
            VERTEX, t_zx[0], t_zx[1], t_zx[2], \

            VERTEX, cell[2, 0], cell[2, 1], cell[2, 2], \
            VERTEX, t_zy[0], t_zy[1], t_zy[2], \

            VERTEX, cell[1, 0], cell[1, 1], cell[1, 2], \
            VERTEX, t_zy[0], t_zy[1], t_zy[2], \

            VERTEX, t_zy[0], t_zy[1], t_zy[2], \
            VERTEX, t_yx[0], t_yx[1], t_yx[2], \

            VERTEX, t_yx[0], t_yx[1], t_yx[2], \
            VERTEX, t_zx[0], t_zx[1], t_zx[2], \

            VERTEX, cell[0, 0], cell[0, 1], cell[0, 2], \
            VERTEX, t_zx[0], t_zx[1], t_zx[2], \

            VERTEX, b_yx[0], b_yx[1], b_yx[2], \
            VERTEX, t_yx[0], t_yx[1], t_yx[2], \

            END \
        ]
        cmd.load_cgo(PBC_BOX, 'PBC_CELL')
        return True

    def pick():
        selected = False

        refer = cmd.get_coords('sele')

        if refer is not None:
            size = len(refer)
            if size >= 2:
                refer = refer.sum(axis = 0)/size
            else:
                refer = refer[0]
            selected = True

        else:
            print('First, click over the atom(s) you want.')

        if selected:
            form.at_x.setText(f'{refer[0]:10.6f}')
            form.at_y.setText(f'{refer[1]:10.6f}')
            form.at_z.setText(f'{refer[2]:10.6f}')

    def run():
        def centralize_xy(cell, positions):
            point = array([float(form.at_x.text()), \
                           float(form.at_y.text()), \
                           0.], dtype = float)
            centre = (cell[0] + cell[1])/2
            d = point - centre
            positions -= d
            icell = linalg.inv(cell)
            ipos = positions.dot(icell)
            for i, row in enumerate(ipos):
                for j, c in enumerate(row):
                    if c >= 1.: ipos[i, j] -= 1
                    if c < 0.: ipos[i, j] += 1
            for i, row in enumerate(ipos):
                if row[2] > .98: ipos[i, 2] -= 1.
            return ipos.dot(cell)

        cell = array([[form.ax.value(), form.ay.value(), form.az.value()], \
                      [form.bx.value(), form.by.value(), form.bz.value()], \
                      [form.cx.value(), form.cy.value(), form.cz.value()]], \
                     dtype = float)
        obj = cmd.get_object_list('all')[0]
        positions = cmd.get_coordset(obj)
        new_positions = centralize_xy(cell, positions)
        for i, row in enumerate(new_positions):
            cmd.alter_state('1', f'rank {i}', \
                            f'(x, y, z) =  ({row[0]}, {row[1]}, {row[2]})')
        pick()

    form.button_PBC.clicked.connect(draw_PBC)
    form.pick_atom.clicked.connect(pick)
    form.button_adjust.clicked.connect(run)

    return dialog
