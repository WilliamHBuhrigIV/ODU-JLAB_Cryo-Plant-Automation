import matlab.engine as matlab
import time


class GasCalc:
    f = {'Ammonia': 1, 'Argon': 2, 'iso-Butane': 3, 'n-Butane': 4, 'Carbon Dioxide': 5, 'Carbon Monoxide': 6,
         'Deuterium': 7, 'Ethylene': 8, 'Helium-4': 10, 'equil Hydrogen': 11, 'normal Hydrogen': 12,
         'ortho Hydrogen': 13, 'paraHydrogen': 14, 'Hydrogen Sulfide': 15, 'Krypton': 16, 'Methane': 17, 'Neon': 18,
         'Nitrogen': 19, 'Nitrogen Trifluoride': 20, 'Oxygen': 21, 'Propane': 22, 'Water': 23, 'Xenon': 24,
         'Refrigerant-11': 25, 'Refrigerant-12': 26, 'Refrigerant-22': 27, 'Refrigerant-32': 28, 'Refrigerant-123': 29,
         'Refrigerant-124': 30, 'Refrigerant-125': 31, 'Refrigerant-134A': 32, 'Refrigerant-152A': 33, 'Helium': 0}
    i = {'Quality': 0, 'Pressure': 1, 'Temperature': 2, 'Density': 3, 'Specific Volume': 4, 'PV/RT': 5,
         'dP/dT @constant Saturation': 6, 'Latent Heat': 7, 'Entropy': 8, 'Enthalpy': 9, 'Helmholtz': 10,
         'Internal Energy': 11, 'Gibbs Energy': 12, 'Fugacity': 13, 'Cp': 14, 'Cv': 15, 'Gamma': 16, 'Expansivity': 17,
         'Gruneisen Parameter': 18, 'Isothermal Compressibility': 19, 'Sound Speed': 20, 'J-T Coefficient': 21,
         'dP/dD @constant Temperature': 22, 'dP/dT @constant Density': 23, '(dH/dV)*V @constant Pressure': 24,
         'Viscosity': 25, 'Conductivity': 26, 'Prandtl Number': 27, 'Thermal Diffusivity': 28, 'Surface Tension': 29,
         'Dielectric Constant': 30, 'Refraction Index': 31, 'Isochoric dT @Lambda': 32, 'Isobaric dT @Lambda': 33,
         'Superfluid Density Fraction': 34, '2nd Sound Velocity': 35, '4th Sound Velocity': 36,
         'Gorter-Mellink Mutual Friction Constant': 37, 'Super Fluid Thermal Conductivity Function': 38,
         '(T-T_lambda)': 39, 'dH/dT @constant Density': 40, 'dS/dT @constant Density': 41, 'c2*gmolwt': 42}
    GasBanList = [4, 10, 12, 31, 32, 33, 34, 35, 36, 37, 38, 39]
    HeBanList = [40, 41, 42]

    def __new__(cls, FluidID: int, PropID: int, Input1: int | str, Value1: float, Input2: int | str, Value2: float,
                Unit=1, Phase=0) -> float:
        if not FluidID:
            if any(ele in [PropID, Input1, Input2] for ele in GasCalc.GasBanList):
                raise ValueError('Improper Inputs: Helium Doesn\'t support All possible Inputs')
            else:
                return HeCalc(HeCalc.i[list(GasCalc.i.keys())[list(GasCalc.i.values()).index(PropID)]],
                              HeCalc.i[list(GasCalc.i.keys())[list(GasCalc.i.values()).index(Input1)]], Value1,
                              HeCalc.i[list(GasCalc.i.keys())[list(GasCalc.i.values()).index(Input2)]], Value2,
                              Unit, Phase)
        else:
            if any(ele in [PropID, Input1, Input2] for ele in GasCalc.HeBanList):
                raise ValueError(f'Improper Inputs: {GasCalc.f.get(FluidID)} Doesn\'t support All possible Inputs')
            else:
                return GPCalc(FluidID, GPCalc.i[list(GasCalc.i.keys())[list(GasCalc.i.values()).index(PropID)]],
                              GPCalc.i[list(GasCalc.i.keys())[list(GasCalc.i.values()).index(Input1)]], Value1,
                              GPCalc.i[list(GasCalc.i.keys())[list(GasCalc.i.values()).index(Input2)]], Value2,
                              Unit, Phase)


class HeCalc:
    i = {'Quality': 0, 'Pressure': 1, 'Temperature': 2, 'Density': 3, 'Specific Volume': 4, 'PV/RT': 5,
         'dP/dT @constant Saturation': 6, 'Latent Heat': 7, 'Entropy': 8, 'Enthalpy': 9, 'Helmholtz': 10,
         'Internal Energy': 11, 'Gibbs Energy': 12, 'Fugacity': 13, 'Cp': 14, 'Cv': 15, 'Gamma': 16, 'Expansivity': 17,
         'Gruneisen Parameter': 18, 'Isothermal Compressibility': 19, 'Sound Speed': 20, 'J-T Coefficient': 21,
         'dP/dD @constant Temperature': 22, 'dP/dT @constant Density': 23, '(dH/dV)*V @constant Pressure': 24,
         'Viscosity': 25, 'Conductivity': 26, 'Prandtl Number': 27, 'Thermal Diffusivity': 28, "Surface Tension": 29,
         'Dielectric Constant': 30, 'Refraction Index': 31, 'Isochoric dT @Lambda': 32, 'Isobaric dT @Lambda': 33,
         'Superfluid Density Fraction': 34, '2nd Sound Velocity': 35, '4th Sound Velocity': 36,
         'Gorter-Mellink Mutual Friction Constant': 37, 'Super Fluid Thermal Conductivity Function': 38,
         '(T-T_lambda)': 39}

    def __new__(cls, Index: int | str, Input1: int | str, Value1: float, Input2: int | str, Value2: float,
                Unit=1, Phase=0) -> float:
        return eng.HeCalc(Index, Phase, Input1, Value1, Input2, Value2, Unit)


class GPCalc:
    f = {'Ammonia': 1, 'Argon': 2, 'iso-Butane': 3, 'n-Butane': 4, 'Carbon Dioxide': 5, 'Carbon Monoxide': 6,
         'Deuterium': 7, 'Ethylene': 8, 'Helium-4': 10, 'equil Hydrogen': 11, 'normal Hydrogen': 12,
         'ortho Hydrogen': 13, 'paraHydrogen': 14, 'Hydrogen Sulfide': 15, 'Krypton': 16, 'Methane': 17, 'Neon': 18,
         'Nitrogen': 19, 'Nitrogen Trifluoride': 20, 'Oxygen': 21, 'Propane': 22, 'Water': 23, 'Xenon': 24,
         'Refrigerant-11': 25, 'Refrigerant-12': 26, 'Refrigerant-22': 27, 'Refrigerant-32': 28, 'Refrigerant-123': 29,
         'Refrigerant-124': 30, 'Refrigerant-125': 31, 'Refrigerant-134A': 32, 'Refrigerant-152A': 33}
    i = {'Quality': 0, 'Pressure': 1, 'Temperature': 2, 'Density': 3, 'Entropy': 4, 'Enthalpy': 5, 'Internal Energy': 6,
         'dP/dD @constant Temperature': 7, 'dP/dT @constant Density': 8, 'Cv': 9, 'Cp': 10, 'Gamma': 11,
         'Expansivity': 12, 'Gruneisen Parameter': 13, 'Isothermal Compressibility': 14, 'Sound Speed': 15,
         'J-T Coefficient': 16, '(dH/dV)*V @constant Pressure': 17, 'dH/dT @constant Density': 18,
         'dS/dT @constant Density': 19, 'c2*gmolwt': 20, 'Viscosity': 21, 'Conductivity': 22, 'Thermal Diffusivity': 23,
         'Prandtl Number': 24, 'Surface Tension': 25, 'Dielectric Constant': 26, 'PV/RT': 27,
         'dP/dT @constant Saturation': 28, 'Latent Heat': 29, 'Fugacity': 30}

    def __new__(cls, FluidID: int, PropID: int, Input1: int | str, Value1: float, Input2: int | str, Value2: float,
                Unit=1, Phase=0) -> float:
        return eng.GPCalc(FluidID, PropID, Phase, Input1, Value1, Input2, Value2, Unit)


def StopCRYODATA() -> bool:
    return bool(eng.CDClose())


t0: float = time.time()
matlab_state = ""
try:
    engine = list(matlab.find_matlab())[0]
    if engine == '':
        raise Exception('No Matlab Sessions are shared Creating New Session')
    eng: matlab = matlab.connect_matlab(engine)
    matlab_state = eng.matlab.engine.engineName()
except Exception as N:
    print(N)
    eng: matlab = matlab.start_matlab()
    matlab_state = eng.matlab.engine.engineName()
try:
    excel = eng.actxGetRunningServer('Excel.Application')
    excel_status = 'Found Instance'
except Exception as N:
    print(N)
    if not eng.CDStart():
        raise ConnectionError("Excel Failed to Kill all Processes or Failed Creating the Proces")
    excel_status = 'Created Instance'
eng.addpath(r'M:\cryo\Buhrig\CRYODATA', nargout=0)
if f'{HeCalc(3, 1, 100e3, 2, 4):.12f}' != '129.858859681731':
    raise ValueError("HeCalc Failed Value Test")
if f'{GPCalc(19, 3, 1, 100e3, 2, 65):.12f}' != '861.849945360304':
    raise ValueError("GPCalc Failed Value Test")
t1: float = time.time()
newline: str = f"{'--------------------------------------------------------------------------------':<80}\n"
print(newline, f'|{"HEPAK & GASPAK":^78}|\n', newline, f'|{"Matlab Connection":^22}={matlab_state:^16}|{"Excel Connection":^19}={excel_status:^18}|\n', newline,
      f'|{"":^39}|{"Total Initialize Time (s)":^28}={t1 - t0:^9.4f}|\n', newline, sep='')
