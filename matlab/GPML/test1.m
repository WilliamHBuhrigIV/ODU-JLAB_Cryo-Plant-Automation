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
% multiple input-single output
%load('./data/data_12.mat')
a = 0:0.02:10;
b = 0:0.02:10;
at = 0.1:0.2:9.9;
bt = 0.1:0.2:9.9;
func1 = @(x1, x2) x1.^2 + x2.^2;
func2 = @(x1, x2) (x1.^2)./(x2.^2);
c = func1(a,b);
d = func2(a,b);
ct = func1(at,bt);
dt = func2(at,bt);
x = [a;b]';
y = [c;d]';
xt = [at;bt]';
yt = [ct;dt]';
% Set the mean function, covariance function and likelihood function
% Take meanConst, covRQiso and likGauss as examples
meanfunc = @meanConst;
covfunc = @covRQiso; 
likfunc = @likGauss; 
% Initialization of hyperparameters
hyp = struct('mean', 3, 'cov', [0 0 0], 'lik', -1);
% meanfunc = [];
% covfunc = @covSEiso; 
% likfunc = @likGauss; 
% % Initialization of hyperparameters
% hyp = struct('mean', [], 'cov', [0 0], 'lik', -1);
% Optimization of hyperparameters
hyp2 = minimize(hyp, @gp, -20, @infGaussLik, meanfunc, covfunc, likfunc,x, y);
% Regression using GPR
% yfit is the predicted mean, and ys is the predicted variance
[yfit ys] = gp(hyp2, @infGaussLik, meanfunc, covfunc, likfunc,x, y, xt);
% Visualization of prediction results
plotResult(yt, yfit)