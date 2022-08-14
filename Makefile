.ONESHELL:
SHELL=/bin/bash
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

create_env:
	conda create --name geospatial_webapp -y

# In MacOS, the command "make setup_env" was stuck at solving environment when it reached 
# 'conda install python=3.7.7 -c conda-forge -y' and hence I would recommend executing 
# the following commands manually in the terminal. 
# The commands ran successfully in the terminal (.zsh). 
# One can also create the environment using the .yml file.

setup_env:
	conda init
	# Commented the below line for running on macOS. The line should be uncommented for running on Linux.
	# source ~/.bashrc
	# conda activate geospatial_webapp
	$(CONDA_ACTIVATE) geospatial_webapp
	conda install python=3.7.7 -c conda-forge -y
	./env_setup/install_packages.sh
	python -m ipykernel install --user --name=geospatial_webapp

export_env:
	conda env export --no-builds > geospatial_webapp.yml