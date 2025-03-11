import numpy as np
from CRYODATA import GasCalc as GC

newline: str = f"{'--------------------------------------------------------------------------------':<80}\n"


def fullConvectionCoefficientCalculation(surfaceTemperature: float, fluidTemperature: float, fluidPressure: float,
                                         characteristicLength) -> float:
    avgTemperature = np.divide(surfaceTemperature + fluidTemperature, 2)
    Pr: float = GC(GC.f['Helium'], GC.i["Prandtl Number"], GC.i['Temperature'], avgTemperature, GC.i['Pressure'],
                   fluidPressure)
    volumetricExpansivity: float = GC(GC.f['Helium'], GC.i["Expansivity"], GC.i['Temperature'], avgTemperature,
                                      GC.i['Pressure'], fluidPressure)
    dynamicViscosity: float = GC(GC.f['Helium'], GC.i["Viscosity"], GC.i['Temperature'], avgTemperature,
                                 GC.i['Pressure'], fluidPressure)
    density: float = GC(GC.f['Helium'], GC.i["Density"], GC.i['Temperature'], avgTemperature, GC.i['Pressure'],
                        fluidPressure)
    conductionCoefficient: float = GC(GC.f['Helium'], GC.i["Conductivity"], GC.i['Temperature'], avgTemperature,
                                      GC.i['Pressure'], fluidPressure)
    print(dynamicViscosity, density)
    kinematicViscosity: float = kinematicViscosityCalculation(dynamicViscosity, density)
    Gr: float = grashofNumberCalculation(volumetricExpansivity, surfaceTemperature, fluidTemperature,
                                         characteristicLength, kinematicViscosity)
    Ra: float = rayleighNumberCalculation(Gr, Pr)
    return convectionCoefficientCalculation(Ra, Pr, conductionCoefficient, characteristicLength)


def convectionCoefficientCalculation(Rayleigh: float, Prandtl: float, conductionCoefficient: float,
                                     characteristicLength: float) -> float:
    return conductionCoefficient / characteristicLength * (0.825 + 0.387 * np.power(Rayleigh, 1 / 6) /
                                                           np.power(1 + np.power(np.divide(0.492, Prandtl), 9 / 16),
                                                                    np.divide(4, 9)))


def rayleighNumberCalculation(Grashof: float, Prandtl: float) -> float:
    return np.multiply(Grashof, Prandtl)


def grashofNumberCalculation(volumetricExpansivity: float, surfaceTemperature, fluidTemperature, characteristicLength,
                             kinematicViscosity, gravity=9.81) -> float:
    return np.divide(gravity * volumetricExpansivity * np.abs(surfaceTemperature - fluidTemperature) *
                     np.power(characteristicLength, 3), np.power(kinematicViscosity, 2))


def kinematicViscosityCalculation(dynamicViscosity: float, density: float) -> float:
    return np.divide(dynamicViscosity, density)


class HeatExchanger:
    # For Aluminum Material Properties NIST
    # https://www.nist.gov/mml/acmd/aluminum-6061-t6-uns-aa96061
    class Layer:
        def __init__(self, StreamLetter: str, ForwardFlowDirection: bool | None):
            # Flow Direction is with respect to the Majority of Flow
            self.fluid: str = StreamLetter
            self.contraflow: bool = ForwardFlowDirection
            self.FinOrder: list[HeatExchanger.Fin] = []
            self.LengthOrder: list[float] = []
            self.WidthOrder: list[float] = []
            self.AngleOrder: list[float] = []
            self.Calculated: bool = False
            self.FinArea: float = 0
            self.WallArea: float = 0
            self.Length: float = 0
            pass

        def calculateLayerFlowPath(self) -> None:
            self.Calculated = True
            self.FinArea: float = 0
            self.WallArea: float = 0
            self.Length: float = 0
            for fins in range(len(self.FinOrder)):
                self.FinArea: float = (self.FinArea + self.FinOrder[fins].density * self.WidthOrder[fins] *
                                       self.LengthOrder[fins] * self.FinOrder[fins].height *
                                       (1 if self.AngleOrder[fins] == 0 else 1 / 2))
                self.WallArea: float = (self.WallArea + self.LengthOrder[fins] * self.WidthOrder[fins] *
                                        (1 if self.AngleOrder[fins] == 0 else 1 / 2))
                self.Length: float = self.Length + (self.LengthOrder[fins] if self.AngleOrder[fins] == 0 else np.divide(
                    np.sqrt(np.square(self.WidthOrder[fins]) + np.square(self.LengthOrder[fins])), np.sqrt(2)))
            return None

        def addFlowPath(self, Fin, Length: float, Width: float, Angle: float) -> None:
            self.FinOrder.append(Fin)
            self.LengthOrder.append(Length / 1000)
            self.WidthOrder.append(Width / 1000)
            self.AngleOrder.append(Angle)
            return None

        def __str__(self):
            flowpath: list[str] = [newline, f"|{'Layer':^19}|{'Stream ' + self.fluid:^58}|\n", newline,
                                   f'|{"Specification":^19}|{"Length (mm)":^19}|{"Width (mm)":^19}|{"Angle (Degree)":^18}|\n']
            for fin in range(len(self.FinOrder)):
                flowpath.append(f'|{self.FinOrder[fin].specification:^19}|{self.LengthOrder[fin] * 1000:^19.1f}'
                                f'|{self.WidthOrder[fin] * 1000:^19.1f}|{np.rad2deg(self.AngleOrder[fin]):^18.6f}|\n')
            flowpath.append(newline)
            if self.Calculated:
                flowpath.append(
                    f'|{"Wall Area (m^2)":^19}={self.WallArea:^19.4f}|{"Fin Area (m^2)":^19}={self.FinArea:^18.4f}|\n' + newline)
            return ''.join(flowpath)

    class Fin:
        def __init__(self, SpecificationName: str, FinType: str, FinHeightThouInch: int, FinPerInch: int,
                     FinThicknessThouInch: int, **kwargs):
            # ALL IMPERIAL INPUT
            self.specification: str = SpecificationName
            self.type: str = FinType
            self.height: float = FinHeightThouInch * 2.54e-5
            self.density: float = FinPerInch * 39.3701
            self.thickness: float = FinThicknessThouInch * 2.54e-5
            pass

        def __str__(self):
            fins: list[str] = [newline, f"|{'Fin':^19}|{self.specification:^58}|\n", newline,
                               f'|{"Type":^19}|{"Height (mm)":^19}|',
                               f'{"Thickness (mm)":^19}|{"Density (Fin/m)":^18}|\n|{self.type:^19}|{self.height * 1000:^19.3f}'
                               f'|{self.thickness * 1000:^19.3f}|{self.density:^18.3f}:\n', newline]
            return ''.join(fins)

    def __init__(self, DocumentationSource: str, HeatExchangerName: str, Inlets: int, LayerNumber: int,
                 FlowStreams: dict[str, str]) -> None:
        self.DocumentationSource: str = DocumentationSource
        self.HeatExchangerName: str = HeatExchangerName
        self.Inlets: int = Inlets
        self.NumberOfLayers: int = LayerNumber
        self.FlowStreams: dict[str, str] = FlowStreams
        self.FlowStreams.update({"NULL": "UNIMPLEMENTED LAYERS"})
        self.LayerOrder: list[HeatExchanger.Layer] = []
        self.Layers: list[HeatExchanger.Layer] = []
        for i in range(self.NumberOfLayers):
            self.LayerOrder.append(HeatExchanger.Layer("NULL", None))
        pass

    def updateLayers(self) -> None:
        self.Layers.clear()
        for layer in self.LayerOrder:
            if self.Layers.__contains__(layer):
                pass
            else:
                self.Layers.append(layer)
        return None

    def print(self) -> None:
        print(self.__str__())
        streams: list[str] = list(self.FlowStreams.keys())
        try:
            streams.remove('NULL')
        except ValueError:
            pass
        Layers = self.Layers
        for stream in streams:
            for layer in Layers:
                if stream == layer.fluid:
                    print(layer.__str__())
                    Layers.remove(layer)
                else:
                    pass
        return None

    def layerLocalPatternFill(self, StartingPoints: list[int], Pattern: list[Layer]) -> None:
        for starts in StartingPoints:
            for i in range(starts, starts + len(Pattern)):
                self.LayerOrder[i] = Pattern[np.mod(i - starts, len(Pattern))]
        self.updateLayers()
        return None

    def layerGlobalPatternFill(self, Start: int, End: int, Pattern: list[Layer]) -> None:
        for i in range(Start, End + 1):
            self.LayerOrder[i] = Pattern[np.mod(i - Start, len(Pattern))]
        self.updateLayers()
        return None

    def calculatePatternFlowPaths(self) -> None:
        self.updateLayers()
        for layer in self.Layers:
            if layer.contraflow is not None:
                layer.calculateLayerFlowPath()
        return None

    def run(self, StreamOrder: list[str], InletTemperature: list[float], InletPressure: list[float],
            InletMassFlow: list[float]) -> list[float]:
        if self.Inlets != len(StreamOrder):
            raise ValueError(f"Unbalanced Stream Inputs: {len(StreamOrder)} Received, {self.Inlets} Requested")
        if self.Inlets != len(InletTemperature):
            raise ValueError(f"Unbalanced Temp. Inputs: {len(InletTemperature)} Received, {self.Inlets} Requested")
        if self.Inlets != len(InletPressure):
            raise ValueError(f"Unbalanced Pressure Inputs: {len(InletPressure)} Received, {self.Inlets} Requested")
        if self.Inlets != len(InletMassFlow):
            raise ValueError(f"Unbalanced Massflow Inputs: {len(InletMassFlow)} Received, {self.Inlets} Requested")
        Cp: list[float] = []
        for stream in range(len(StreamOrder)):
            Cp.append(GC(GC.f[self.FlowStreams[StreamOrder[stream]]], GC.i["Cp"], GC.i['Temperature'],
                         InletTemperature[stream], GC.i['Pressure'], InletPressure[stream]))
        Capacity: list[float] = []
        for stream in range(len(StreamOrder)):
            Capacity.append(InletMassFlow[stream] * Cp[stream])
        print(Cp, Capacity)
        OutletTemperature = InletTemperature
        return OutletTemperature

    def __str__(self) -> str:
        layers: list[str] = [newline, f"|{'Heat Exchanger':^19}|{self.HeatExchangerName:^58}|\n", newline,
                             f'|{"Layer #":^9}|{"Stream":^9}|{"Direction":^13}|{"Fluid Name":^44}|\n']
        for layer in reversed(range(len(self.LayerOrder))):
            layers.append(f'|{layer:^9}|{self.LayerOrder[layer].fluid:^9}'
                          f'|{"⟵" if self.LayerOrder[layer].contraflow else "⟶" if self.LayerOrder[layer].contraflow is not None else "↔":^13}|'
                          f'{self.FlowStreams[self.LayerOrder[layer].fluid]:^44}|\n')
        layers.append(newline)
        return ''.join(layers)
