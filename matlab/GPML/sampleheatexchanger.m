% Data Generation File for Simple Heat Exchanger
clear; clc; format long;

Fluid_Kinematic_Viscocity = .61*10^-4;
Fluid_Dynamic_Viscocity = 1.5*10^-5;
Fluid_Thermal_Conductivity = 0.115;
Fluid_Specific_Heat = 5197;
Fluid_Density = 0.244;
Prantle_Number = 0.619;
Fluid_Layers = [5,5];
Fluid_Massflow = [0.01,0.011];
Fluid_Specific_Heat_Capacity = [5200, 5200];
Fluid_Inlet_Temperature = [60, 70];
Fluid_Capacity_Rate = Fluid_Massflow.*Fluid_Specific_Heat_Capacity;

Fin_Thickness = 0.001; 
Wall_Spacing = 0.01;
Hx_Length = 1;
Hx_Width = 0.1;
Plate_Thickness = 0.05;

Average_Heat_Transfer_Area = Hx_Width*Hx_Length;

Flow_Area = Hx_Width*Wall_Spacing*Fluid_Layers;
Free_Stream_Velocity = Fluid_Massflow./Fluid_Density./Flow_Area;
Reynolds_Number = Free_Stream_Velocity.*Hx_Length./Fluid_Kinematic_Viscocity;
Nesault_Number = 0.037.*Reynolds_Number.^(4/5).*Prantle_Number;

Fluid_Thermal_Convection = Nesault_Number.*Fluid_Thermal_Conductivity./Hx_Length;
Aluminum_Thermal_Conductivity = 237; 

Fin_Effectiveness_Parameter = sqrt(2.*Fluid_Thermal_Convection./(Aluminum_Thermal_Conductivity*Fin_Thickness));
Fin_Length = Wall_Spacing/2;
Fin_Surface_Effectiveness = tanh(Fin_Effectiveness_Parameter.*Fin_Length)./(Fin_Effectiveness_Parameter.*Fin_Length);
Fin_Area = Hx_Length*Fin_Length;
Surface_Temperature_Effectiveness = 1 - Fin_Area/Average_Heat_Transfer_Area.*(1-Fin_Surface_Effectiveness);
Average_Heat_Transfer_Conductance = 1/( ...
    1/(Surface_Temperature_Effectiveness(1)*Fluid_Thermal_Convection(1)) ...
    + 1/(Surface_Temperature_Effectiveness(2)*Fluid_Thermal_Convection(2)) ...
    + Plate_Thickness/(Aluminum_Thermal_Conductivity));
Transfer_Units = Average_Heat_Transfer_Area.*Average_Heat_Transfer_Conductance./min(Fluid_Capacity_Rate);
Hx_Efficiency = ((1-exp(-Transfer_Units*(1-min(Fluid_Capacity_Rate)/max(Fluid_Capacity_Rate)))) ...
    /(1-(min(Fluid_Capacity_Rate)/max(Fluid_Capacity_Rate)*exp(-Transfer_Units*(1-min(Fluid_Capacity_Rate)/max(Fluid_Capacity_Rate))))));
Outlet_Temperature = [Hx_Efficiency./Fluid_Capacity_Rate(1).*Fluid_Capacity_Rate(2).*(Fluid_Inlet_Temperature(2)-Fluid_Inlet_Temperature(1))+Fluid_Inlet_Temperature(1), -(Hx_Efficiency.*(Fluid_Inlet_Temperature(2)-Fluid_Inlet_Temperature(1))-Fluid_Inlet_Temperature(2))];