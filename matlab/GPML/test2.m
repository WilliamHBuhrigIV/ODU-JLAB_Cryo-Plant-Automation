%%%%%%%%%%      Gaussian Process Regression (GPR)               %%%%%%%%%
% Demo: prediction using GPR
% ---------------------------------------------------------------------%
clc
close all
clear all
addpath(genpath(pwd))
% load data
%{
x :   training inputs
y :   training targets
xt:   testing inputs
yt:   testing targets
%}
% multiple input-multiple output
% load('./data/data_2.mat')
% % % a = 0:pi/10000:pi;
% % % b = 0:pi/10000:pi;
% % % at = 0:0.2:pi;
% % % bt = 0:0.2:pi;
% % % func1 = @(x1, x2) x1.^2 + x2.^2;
% % % func2 = @(x1, x2) sin(x1+x2);
% % % c = func1(a,b);
% % % d = func2(a,b);
% % % ct = func1(at,bt);
% % % dt = func2(at,bt);
% % % x = [a;b]';
% % % y = [c;d]';
% % % xt = [at;bt]';
% % % yt = [ct;dt]';

input_1 = 0:1:375;
input_2 = 0:1:375;

test_input_1 = 20.1:20.1:360.1;
test_input_2 = 20.1:20.1:360.1;

function_a = @(x1, x2) (x1.^2)+(x2.^2);
function_b = @(x1, x2) (x1.^2).*(x2.^2);

result_a = function_a(input_1,input_2);
result_b = function_b(input_1,input_2);

test_result_a = function_a(test_input_1,test_input_2);
test_result_b = function_b(test_input_1,test_input_2);

x = [input_1;input_2]';
y = [result_a;result_b]';
xt = [test_input_1;test_input_1]';
yt = [test_result_a;test_result_b]';



% Set the mean function, covariance function and likelihood function
% Take meanConst, covRQiso and likGauss as examples
meanfunc = @meanConst;
covfunc = @covRQiso; 
likfunc = @likGauss; 
% Initialization of hyperparameters
hyp = struct('mean', 0, 'cov', [2 2 2], 'lik', -1);
% meanfunc = [];
% covfunc = @covSEiso; 
% likfunc = @likGauss; 
% 
% hyp = struct('mean', [], 'cov', [0 0], 'lik', -1);
% Optimization of hyperparameters
hyp2 = minimize(hyp, @gp, -5, @infGaussLik, meanfunc, covfunc, likfunc,x, y);
% Regression using GPR
% yfit is the predicted mean, and ys is the predicted variance
[yfit ys] = gp(hyp2, @infGaussLik, meanfunc, covfunc, likfunc,x, y, xt);
% Visualization of prediction results
% First output
plotResult(yt(:,1), yfit(:,1))
% Second output
% plotResult(yt(:,2), yfit(:,2))