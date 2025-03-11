if not(exist("AspenEDR", "var"))
    [~] = system("C:\Program Files\AspenTech\Aspen Exchanger Design and Rating V14.0\XEQ\AspenEDR.exe &");
    pause(5);
    AspenEDR = actxserver('BJACWIN.BJACApp');
    AspenEDR.Visible = true;
    % AspenPlateFinApp = AspenEDR.GetApp("PlateFin");
end
OutputTypes = ["Strm_InletTemperature","Strm_OutletTemperature","Strm_InletPressure","Strm_OutletPressure","Strm_FlowRate"];
InputTypes = ["Strm_InletTemperature","Strm_OutletTemperature","Strm_FlowRate","Strm_DrawOffTemperature"];
% TimeAvailable = 5*24*3600;
% AvgRunTime = 30;
% RunAvailable = TimeAvailable/AvgRunTime;
MassflowRuns = 5; %4
TemperatureRuns = 5; %9
TemperatureTestPoints = linspace(320,80,TemperatureRuns);
MassflowTestPoints = linspace(0.01,0.25,MassflowRuns);
if not(exist("TestInitialConditions","var"))
    TestInitialConditions = combinations(TemperatureTestPoints,TemperatureTestPoints,TemperatureTestPoints,MassflowTestPoints,MassflowTestPoints,MassflowTestPoints);
    for i = size(TestInitialConditions,1):-1:1
        if TestInitialConditions{i,1} < TestInitialConditions{i,3} || TestInitialConditions{i,2} < TestInitialConditions{i,3}
            TestInitialConditions(i,:) = [];
        end
    end
end
for i = 1:size(TestInitialConditions,1)
    InputArray = [TestInitialConditions{i,1:3};[TestInitialConditions{i,3}-0.01,TestInitialConditions{i,3}-0.01,TestInitialConditions{i,3}-0.01];TestInitialConditions{i,4:6};[TestInitialConditions{i,3}-0.01,"",""]];
    InputArray(1,3) = TestInitialConditions{i,3}-0.02;
    try
        stateCode = OpenFile("Hx1002-1003", AspenEDR);
        stateCode = ProvideInputs(InputTypes,InputArray,AspenEDR,"PlateFin");
        if AspenEDR.GetApp("PlateFin").CanRun
            stateCode = AspenEDR.GetApp("PlateFin").Run;
        end
        [Results, stateCode] = CollectResults(OutputTypes,AspenEDR,"PlateFin");
        writematrix(Results,"Results\Result"+string(i)+".txt")
    catch
        continue
    end
    continue
end

function [stateCode] = OpenFile(name, AspenEDR)
    if boolean(upper(erase(AspenEDR.GetFileName, ".EDR")) == upper(name))
        stateCode = 1;
    else
        if not(AspenEDR.IsSaved)
            AspenEDR.FileSave
        end
        AspenEDR.FileOpen('M:\cryo\Buhrig\Projects\Heat Exchanger Simulation\Aspen Files\'+upper(name)+'.EDR');
        stateCode = 0;
    end
    return
end

function [stateCode] = ProvideInputs(InputTypes,InputValues,AspenEDR,AppType)
    numOfDiffResults = size(InputTypes,2);
    InputResultsInterface = AspenEDR.GetApp(AppType).Arrays;
    numOfDiffStrms = InputResultsInterface.Item("Strm_Name").GetSize;
    for i = 1:numOfDiffStrms
        for j = 1:numOfDiffResults
            InputResultsInterface.Item(InputTypes(j)).GetElement(i).szValuePureSI = string(InputValues(j,i));
        end
    end
    stateCode = 0;
end

function [OutputResults, stateCode] = CollectResults(ResultTypes,AspenEDR,AppType)
    try
        numOfDiffResults = size(ResultTypes,2);
        OutputResultsInterface = AspenEDR.GetApp(AppType).ResultArrays;
        numOfDiffStrms = OutputResultsInterface.Item("Strm_Name").GetSize;
        OutputResults = zeros(numOfDiffStrms,numOfDiffResults);
        if AspenEDR.GetApp(AppType).HasResults
            for i = 1:numOfDiffStrms
                for j = 1:numOfDiffResults
                    OutputResults(i,j) = OutputResultsInterface.Item(ResultTypes(j)).GetElement(i).ValuePureSI;
                end
            end
        end
        stateCode = 0;
    catch
        warning("Failed to Collect Data")
        stateCode = 1;
    end
end