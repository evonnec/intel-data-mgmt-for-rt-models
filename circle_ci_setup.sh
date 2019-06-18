#!/bin/bash
echo "--------------------------------------------"

echo "Hey there! This script will run your circle ci for intel-data-mgmt-for-rt-models."
echo ""
echo ""

su root
curl -fLSs https://circle.ci/cli | bash
#sudo curl -fLSs https://circle.ci/cli | DESTDIR=/opt/bin bash
sudo snap install docker circleci
sudo snap connect circleci:docker docker
circleci setup

echo ""
echo ""
echo "we're done with setting up circle CI, you'll need to add the token to get into the github repo"
