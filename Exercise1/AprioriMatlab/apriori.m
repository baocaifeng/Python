function [resItems,resRules] = apriori(fname,minS,minC)
%aprior is a simple implement of the Apriori algorithm.
%   example:  aprior(fname)
%   Note: input can be excel,csv(comma-seperated value)
%=============================variable initialzie==========================
if nargin == 0
    error('Error: you need to specify at least one argument');
elseif nargin == 1
    minS = 0.15;
    minC = 0.6;
elseif nargin == 2
    minC = 0.6;
end



%% data read
[~,~,allData] = xlsread(fname);

%% get itemSet and TransactionList
[itemSet,transactionList] = getItemSetAndTransactionList(allData);

%% get the items with minSupport
% one-item
oneC = itemSet;
currentCSet = returnItemSetWithMinSupport(oneC,transactionList,minS);
largeSet = {};

k = 2;
while ~isempty(currentCSet)
    largeSet{end+1} = currentCSet;
    currentCSet = joinSet(currentCSet,k);
    currentCSet = returnItemSetWithMinSupport(currentCSet,transactionList,minS);
    k = k+1;
end

resItems = {};
for ii = 1:length(largeSet)
    for jj = 1:length(largeSet{ii})
        support = getFreq(largeSet{ii}{jj},transactionList);
        if support >= minS
            resItems{end+1,1} = {largeSet{ii}{jj},support};
        end
    end
end
resRules = {};
for ii = 1:length(largeSet)
    for jj = 1:length(largeSet{ii})
        subsets = subset(largeSet{ii}{jj});
        for kk = 1:length(subsets)
            pre = subsets{kk};
            post = setdiff(largeSet{ii}{jj},pre);
            if ~isempty(post)
                confidence = getFreq(largeSet{ii}{jj},transactionList)/getFreq(pre,transactionList);
                lift = getFreq(largeSet{ii}{jj},transactionList)/getFreq(pre,transactionList)/getFreq(post,transactionList);
                if confidence >= minC
                    resRules{end+1,1} = {pre,post,confidence,lift};
                end
            end
        end
    end
end

printResult(resItems,resRules);
save("resItems.mat", "resItems", "-mat");
save("resRules.mat", "resRules", "-mat");
end


%% function getFreq
function freq = getFreq(item,transactionList)
% This function return the frequency of item
freq = 0;
for ii = 1:length(transactionList)
    if all(ismember(item,transactionList{ii}))
        freq = freq+1;
    end
end
freq = freq/size(transactionList,1);
end


%% function Cell2String
function str = Cell2String(Cel)
% This function convert a cell array of cell to string.
str = [];
for ii = 1:length(Cel)
    str = [str,Cel{ii},','];
end
end

%% funtion subset
function subsets = subset(itemSet)
% This function return the all non-empty subsets of itemSet
subsets = {};
for ii = 1:length(itemSet)
    t = combnk(itemSet,ii);
    for jj = 1:size(t,1)
        subsets{end+1,1} = {t{jj,:}};
    end
end
end

%% function joinSet
function resItemSet = joinSet(itemSet,len)
% This function join the member in itemSet to create new element whose
% length = len

resItemSet = {};
for ii = 1:length(itemSet)
    for jj = 1:length(itemSet)
        newItem = union(itemSet{ii},itemSet{jj});
        if length(newItem) == len
            if ~exIsmember(newItem,resItemSet)
                 resItemSet{end+1,1} =newItem;
            end
        end
    end
end
end

%% function printResult
function printResult(Items,Rules)
LItems = {};
LRules = {};
for ii = 1:length(Items)
    LItems{ii,1} = Items{ii}{1};
    LItems{ii,2} = Items{ii}{2};
end
for ii = 1:length(Rules)
    LRules{ii,1} = Rules{ii}{1};
    LRules{ii,2} = Rules{ii}{2};
    LRules{ii,3} = Rules{ii}{3};
    LRules{ii,4} = Rules{ii}{4};
end
sortedItems = sortrows(LItems,2);
sortedRules = sortrows(LRules,3);
for ii =1:size(sortedItems)
    fprintf('item: %s, %.3f \n',Cell2String(sortedItems{ii,1}),sortedItems{ii,2});
end

for ii =1:size(sortedRules)
    fprintf('Rules: %s ==> %s, %.3f,%.3f \n',Cell2String(sortedRules{ii,1}),Cell2String(sortedRules{ii,2})...
        ,sortedRules{ii,3},sortedRules{ii,4});
end
end

%% function exIsmember
function output = exIsmember(inputA,inputB)
% this function checks if inputA is in inputB
output = false;
for ii = 1:size(inputB)
    if all(ismember(inputA,inputB{ii}))
        output = true;
    end
end
end

%% function getItemSetAndTransactionList
function [itemSet,transactionList] = getItemSetAndTransactionList(allData)
% get the itemSet and transactionList
transactionList ={};
itemSet = {};
for ii = 1:size(allData,1)
    transaction = allData(ii,:);
    transaction(cellfun(@(x) any(isnan(x)),transaction)) = [];
    
    for jj = 1 :length(transaction)
        if isfloat(transaction{jj})
            transaction{jj}=num2str(transaction{jj});
        end
    end
    transactionList{end+1,1} = transaction;   
end
itemSet = unique([transactionList{:}]);
for ii = 1:length(itemSet)
    itemSet{ii} = itemSet(ii);
end
itemSet  =itemSet';
end
  
%% funtion returnItemSetWithMinSupport
function [subItemSet] = returnItemSetWithMinSupport(itemSet,transactionList,...
    minSupport)
% This function calculate the support of each item in itemSet, and return a
% subitem each element of which has at least the minSupport

freq = [];
subItemSet = {};
for ii = 1:length(itemSet)
    freq(ii) = 0;
    for jj = 1:size(transactionList,1)
        if all(ismember(itemSet{ii},transactionList{jj}))
            freq(ii) = freq(ii)+1;
        end
    end
    if (freq(ii)/size(transactionList,1))>=minSupport
        subItemSet{end+1,1} = itemSet{ii};
    end
end
end