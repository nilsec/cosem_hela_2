import daisy
import neuroglancer
import numpy as np
from funlib.show.neuroglancer import add_layer
from read_nml import parse_nml

neuroglancer.set_server_bind_address('0.0.0.0')

tracing = "/nrs/funke/ecksteinn/micron_experiments/cosem_hela_2_full/00_data/exports/hela_2_full_p10_g0_s7.nml"
voxel_size = np.array([4,4,4])

f_raw = "/groups/cosem/cosem/data/HeLa_Cell2_4x4x4nm/HeLa_Cell2_4x4x4nm.n5"
dset_raw = '/volumes/raw'

f_sm = "/nrs/cosem/cosem/training/v0003.2/setup31/HeLa_Cell2_4x4x4nm/HeLa_Cell2_4x4x4nm_it1400000.n5"
dset_sm = "microtubules"

sm = daisy.open_ds(f_sm, dset_sm)
raw = daisy.open_ds(f_raw, dset_raw)
raw.voxel_size = daisy.Coordinate(tuple(voxel_size))

edge_connectors_tracing = []
nodes_tracing = []
k = 0
if tracing is not None:
    tracing_node_dic, tracing_edge_list = parse_nml(tracing)

    for e in tracing_edge_list:
        try:
            pos_u = tracing_node_dic[e[0]][::-1] * voxel_size
            pos_v = tracing_node_dic[e[1]][::-1] * voxel_size

            edge_connectors_tracing.append(neuroglancer.LineAnnotation(point_a=pos_u,
                                                                   point_b=pos_v,
                                                                   id=k,
                                                                   segments=None))

            k += 1
        except:
            pass

    for node_id, node_pos in tracing_node_dic.items():
        x = node_pos[2] * voxel_size[2]
        y = node_pos[1] * voxel_size[1]
        z = node_pos[0] * voxel_size[0]
        
        annotation = neuroglancer.EllipsoidAnnotation(center=(x,y,z), 
                                                       radii=(tuple([10] * 3)),
                                                       id=node_id,
                                                       segments=None
                                                       )

        nodes_tracing.append(annotation)

viewer = neuroglancer.Viewer()        
with viewer.txn() as s:
    add_layer(s, raw, 'raw')
    add_layer(s, sm, 'sm')
    s.layers['edges_tracing'] = neuroglancer.AnnotationLayer(voxel_size=(1,1,1),
                                                       filter_by_segmentation=False,
                                                       annotations=edge_connectors_tracing)
    s.layers['nodes_tracing'] = neuroglancer.AnnotationLayer(voxel_size=(1,1,1),
                                                       filter_by_segmentation=False,
                                                       annotations=nodes_tracing)
print(viewer)
