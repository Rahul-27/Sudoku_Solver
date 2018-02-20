import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

import cx_Freeze
from cx_Freeze import setup, Executable

target = Executable(
    script="Sudoku_Solver.py",
    icon="icon.ico"
    )

cx_Freeze.setup(
    name = "_SudokuSolver_",
    version = "0.01",
    description = "Automatic Sudoku Puzzle Solver",
    author = "Rahul Sarkar",
    options = {"build_exe" : {"include_files" : ["tcl86t.dll", "tk86t.dll","0_act.jpg","0_inact.jpg","1_act.jpg","1_inact.jpg","2_act.jpg","2_inact.jpg","3_act.jpg","3_inact.jpg","4_act.jpg","4_inact.jpg","5_act.jpg","5_inact.jpg","6_act.jpg","6_inact.jpg","7_act.jpg","7_inact.jpg","8_act.jpg","8_inact.jpg","9_act.jpg","9_inact.jpg","Back.jpg","back_hov.jpg","back_nor.jpg","back_or_hov.jpg","back_or_nor.jpg","back_or_pre.jpg","back_pre.jpg","clear.jpg","Game_screen.jpg","Grid.jpg","load_hov.jpg","load_nor.jpg","load_pre.jpg","Main_Menu.ogg","Music_Vol.jpg","no_hov.jpg","no_nor.jpg","no_pre.jpg","options.jpg","options_hov.jpg","options_nor.jpg","options_pre.jpg","quit_hov.jpg","quit_nor.jpg","quit_pre.jpg","reset_hov.jpg","reset_nor.jpg","reset_pre.jpg","r_u_sure.jpg","save_hov.jpg","save_nor.jpg","save_pre.jpg","solve_hov.jpg","solve_inact.jpg","solve_nor.jpg","solve_pre.jpg","start_hov.jpg","start_nor.jpg","start_pre.jpg","sudoku_solver.jpg","yes_hov.jpg","yes_nor.jpg","yes_pre.jpg"]}},
    executables = [target]
    )
