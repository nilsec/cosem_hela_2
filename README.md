Install requirements
```
pip install -r requirements.txt
```

Reconstruction contained as an xml file (node ids, positions, and edges) in 
```
hela_2_full_p10_g0_s7.nml
```
The script
```
read_nml.py
```
reads in the reconstruction and returns a dictionary of node ids to node attributes (position) as well as an edge list. 

View the reconstruction via 
```
python -i view_reconstruction.py
```
and copy-paste the printed link into Chrome.
