import traceback
import numpy as np
import timeit
from CRYODATA import GasCalc, StopCRYODATA
from CRYODATA import HeCalc, GPCalc
import PlantSim
from PlantSim import HeatExchanger as Hx


def main() -> None:
    Hx0665: Hx = Hx('ASH0665-1', 'Hx0665', 2, 31,
                    {'A': 'Helium', 'D': 'Nitrogen'})
    layer0665_A = Hx.Layer("A", True)
    layer0665_D = Hx.Layer("D", False)
    fin0665_4 = Hx.Fin("250S1808", "Serrated", 250, 18, 8, lance=1 / 8)
    fin0665_5 = Hx.Fin("250R0624/5", "Perforated", 250, 6, 24, perforations=5)
    fin0665_6 = Hx.Fin("250R1224/25", "Perforated", 250, 12, 24, perforations=25)
    fin0665_7 = Hx.Fin("250R1812/5", "Perforated", 250, 18, 12, perforations=5)
    layer0665_A.addFlowPath(fin0665_5, 80, 180, np.arctan(180 / 80))
    layer0665_A.addFlowPath(fin0665_6, 10, 180, 0)
    layer0665_A.addFlowPath(fin0665_4, 450, 180, 0)
    layer0665_A.addFlowPath(fin0665_6, 10, 180, 0)
    layer0665_A.addFlowPath(fin0665_5, 80, 180, np.arctan(180 / 80))
    layer0665_D.addFlowPath(fin0665_7, 650, 180, 0)
    Hx0665.layerGlobalPatternFill(0, 30, [layer0665_D, layer0665_A])
    Hx0665.calculatePatternFlowPaths()
    Hx0665.print()
    Hx0664: Hx = Hx('ASH0664-1', 'Hx0664', 4, 112,
                    {'A': 'Helium', 'B': 'Helium', 'C': 'Helium',
                     'D': 'Nitrogen', 'DUMMY': 'Dummy'})
    layer0664_Dummy = Hx.Layer("DUMMY", None)
    layer0664_A = Hx.Layer("A", False)
    layer0664_B = Hx.Layer("B", True)
    layer0664_C = Hx.Layer("C", True)
    layer0664_D = Hx.Layer("D", True)
    fin0664_6 = Hx.Fin("150S1808", "Serrated", 150, 18, 8, lance=1 / 8)
    fin0664_7 = Hx.Fin("150R1824/25", "Perforated", 150, 18, 24, perforations=25)
    fin0664_8 = Hx.Fin("150R1412/5", "Perforated", 150, 14, 12, perforations=5)
    fin0664_9 = fin0665_4
    fin0664_10 = fin0665_5
    fin0664_11 = Hx.Fin("350R1812/5", "Perforated", 350, 18, 12, perforations=5)
    fin0664_12 = Hx.Fin("350S1808", "Serrated", 350, 18, 8, lance=1 / 8)
    fin0664_13 = Hx.Fin("350R0624/5", "Perforated", 350, 6, 24, perforations=5)
    fin0664_14 = Hx.Fin("350P0624", "Plain", 350, 6, 24)
    layer0664_Dummy.addFlowPath(fin0664_13, 65, 570, 0)
    layer0664_Dummy.addFlowPath(fin0664_14, 2870, 570, 0)
    layer0664_Dummy.addFlowPath(fin0664_13, 50, 570, 0)
    layer0664_Dummy.addFlowPath(fin0664_14, 365, 570, 0)
    layer0664_A.addFlowPath(fin0664_8, 240, 570, np.arctan(570 / 240))
    layer0664_A.addFlowPath(fin0664_7, 10, 570, 0)
    layer0664_A.addFlowPath(fin0664_6, 2910, 570, 0)
    layer0664_A.addFlowPath(fin0664_8, 160, 570, np.arctan(570 / 160))
    layer0664_B.addFlowPath(fin0664_10, 120, 570, np.arctan(570 / 120))
    layer0664_B.addFlowPath(fin0664_9, 2970, 570, 0)
    layer0664_B.addFlowPath(fin0664_10, 230, 570, np.arctan(570 / 230))
    layer0664_C.addFlowPath(fin0664_13, 150, 570, np.arctan(570 / 150))
    layer0664_C.addFlowPath(fin0664_11, 2960, 570, 0)
    layer0664_C.addFlowPath(fin0664_13, 240, 570, np.arctan(570 / 240))
    layer0664_D.addFlowPath(fin0664_13, 150, 570, np.arctan(570 / 150))
    layer0664_D.addFlowPath(fin0664_12, 2960, 570, 0)
    layer0664_D.addFlowPath(fin0664_13, 240, 570, np.arctan(570 / 240))
    Hx0664.layerLocalPatternFill([0, -1], [layer0664_Dummy])
    Hx0664.layerGlobalPatternFill(1, 55, [layer0664_C, layer0664_A, layer0664_B,
                                          layer0664_A, layer0664_C, layer0664_C, layer0664_A, layer0664_B,
                                          layer0664_D, layer0664_A, layer0664_C])
    Hx0664.layerGlobalPatternFill(56, 110, [layer0664_C, layer0664_A, layer0664_B,
                                            layer0664_D, layer0664_A, layer0664_C, layer0664_C, layer0664_A,
                                            layer0664_B, layer0664_A, layer0664_C])
    Hx0664.calculatePatternFlowPaths()
    Hx0664.print()
    Hx0666: Hx = Hx('ASH0666-1','HX-1002/1003', 7, 67,
                    {'A': 'Helium', 'B': 'Helium', 'C': 'Helium', 'DUMMY': 'Dummy'})
    layer0666_Dummy = Hx.Layer("DUMMY", None)
    layer0666_A = Hx.Layer("A", False)
    layer0666_B = Hx.Layer("B", True)
    layer0666_C = Hx.Layer("C", True)
    fin0666_5 = Hx.Fin("150S1808", "Serrated", 150, 18, 8)
    fin0666_6 = Hx.Fin("150R1824/25", "Perforated", 150, 18, 24)
    fin0666_7 = Hx.Fin("150R1824/10", "Perforated", 150, 18, 24)
    fin0666_8 = Hx.Fin("150R1412/5", "Perforated", 150, 14, 12)
    fin0666_9 = Hx.Fin("350S1510", "Serrated", 350, 15, 10)
    fin0666_10 = Hx.Fin("350R0624/5", "Perforated", 350, 6, 24)
    fin0666_11 = Hx.Fin("350P0624", "Plain", 350, 6, 24)
    layer0666_Dummy.addFlowPath(fin0666_10, 515, 370, 0)
    layer0666_Dummy.addFlowPath(fin0666_10, 50, 370, 0)
    layer0666_Dummy.addFlowPath(fin0666_11, 1470, 370, 0)
    layer0666_Dummy.addFlowPath(fin0666_10, 50, 370, 0)
    layer0666_Dummy.addFlowPath(fin0666_11, 315, 370, 0)
    layer0666_A.addFlowPath(fin0666_8, 110, 370, np.arctan(370/110))
    layer0666_A.addFlowPath(fin0666_7, 10, 370, 0)
    layer0666_A.addFlowPath(fin0666_5, 390, 370, 0)
    layer0664_A.addFlowPath(fin0666_8, 100, 370, 0)  # Port Here
    layer0666_A.addFlowPath(fin0666_5, 1550, 370, 0)
    layer0666_A.addFlowPath(fin0666_6, 10, 370, 0)
    layer0666_A.addFlowPath(fin0666_8, 200, 370, np.arctan(370/200))
    layer0666_B.addFlowPath(fin0666_10, 120, 370, np.arctan(370/120))
    layer0666_B.addFlowPath(fin0666_9, 2060, 370, 0)
    layer0666_B.addFlowPath(fin0666_10, 190, 370, np.arctan(370/190))
    layer0666_C.addFlowPath(fin0666_9, 2400, 370, 0)
    atm = 100e3
    print(Hx0664.run(['A', 'B', 'C', 'D'], [300, 300, 300, 80], [1.1 * atm, 1.7 * atm, 16 * atm, atm],
                     [10, 10, 10, 10]), sep='')
    print(PlantSim.fullConvectionCoefficientCalculation(3, 300, 100e3, 250 * 2.54e-5), sep='-')

    return None


if __name__ == '__main__':
    try:
        print(f'Program Took: {timeit.timeit(main, number=1)} Seconds')
        pass
    except Exception as N:
        traceback.print_exc()
        print(N)
        pass
    finally:
        # print(StopCRYODATA())
        pass
