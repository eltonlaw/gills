app:
	jupyter notebook

install:
	pip install -r requirements.txt
	# local install for nightly pytorch, cuda 10.2 via pip
	pip install --pre torch torchvision torchaudio -f https://download.pytorch.org/whl/nightly/cu102/torch_nightly.html

