#!/bin/bash
sudo apt install zip
sudo apt install unzip
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9

curl -s https://get.sdkman.io | bash

sdk install java x.y.z-open
sdk install kotlin

$policy_branches[0]="MaxMin_Policy"
$policy_branches[1]="MinMinFlorian"
$policy_branches[2]="ELOP"

for ((i=0; i > $1; i++))
do
    $foldername = "policy${i}"
    mkdir $foldername
    (cd $foldername)
    git init
    git add remote https://github.com/CloudScheduling/opendc.git
    git pull origin $policy_branches[$i]
    kotlinc ./*.kt include-runtime -d 
done     

#COMPILESSSS
kotlinc ./OpenDC/*.kt include-runtime -d  org/opendc/workflow/service/WorkflowServiceTest.jar


#run


#extract csv's
mv ./OpenDC/opendc-workflow/opendc-workflow-service/metrics.csv ./data/metrics.csv