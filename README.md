# IRG

IRG is an open-source python library for supporting an autonomous driving competition organized by the University of California, Berkeley, called ROAR. The library is currently developed and managed by a team of researchers at UCB.

Please review the license agreement and the third-party licenses before the installation of the software.

## Installation Guide on PC

1. Windows

If your PC includes an NVidia GPU that supports the latest CUDA SDK (e.g., 10.1), you should first install (1) the latest NVidia GPU driver; (2) CUDA SDK; and (3) cuDNN library.

- First, make sure miniconda Python 3.7 is installed on the system. Verify that conda has the latest updates
```bash
conda update -n base -c defaults conda
```

- In the base IRG project folder, create the IRG anaconda environment
```bash
conda env create -f install\envs\windows.yml
conda activate irg
pip install -e .[pc]
```

- Next, install tensorflow with GPU support
```bash
conda install tensorflow-gpu
```

- Finally, create a local executable directory
```bash
irg createcar --path ~\ROAR
```

2. Linux

If your PC includes an NVidia GPU that supports the latest CUDA SDK (e.g., 10.1), you should first install the latest NVidia GPU driver from the NVidia website.

- First, make sure miniconda Python 3.7 is installed on the system. Verify that conda has the latest updates
```bash
conda update -n base -c defaults conda
```

- In the base IRG project folder, create the IRG anaconda environment
```bash
conda env create -f install\envs\ubuntu.yml
conda activate irg
pip install -e .[pc]
```

- If the Linux machine supports NVidia CUDA, anaconda will  install tensorflow with GPU support
```bash
conda install tensorflow-gpu
```

- Finally, create a local executable directory
```bash
irg createcar --path ~\ROAR
```

3. Mac OS X

- First, make sure miniconda Python 3.7 is installed on the system. Verify that conda has the latest updates
```bash
conda update -n base -c defaults conda
```

- In the base IRG project folder, create the IRG anaconda environment
```bash
conda env create -f install\envs\mac.yml
conda activate irg
pip install -e .[pc]
```

- Finally, create a local executable directory
```bash
irg createcar --path ~\ROAR
```
