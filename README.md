# install_subpack
installs a FAW subpack for SubLab 1.1.x because for some reason it wont accept the pack i bought. This script copies the presets to the right folders and adds the samples to sublab's db.

1. download and put the install.py in your FAW install directory, (entirely safe, please cross check my code before you do this)

`C:\Program Files\FAW\SubLab`

2. copy your subpack or subxlpack to `C:\Program Files\FAW\SubLab`

3. open powershell/cmd/bash as admin and execute: 

`python install.py <xyz>.subpack`

Modifying SubLab.db needs admin rights and also writing the samples out to `/SubLab/Pack/*.wav` needs admin rights, i was too lazy to figure this out for non-admin execution and also getting the fucking paths right. pretty straightforward to modify if something breaks on your end. 

### notes:
- annoying ass VST to set up.
- crippling adhd means i hyperfocus on the most useless shit 
- fun challenge though :D
