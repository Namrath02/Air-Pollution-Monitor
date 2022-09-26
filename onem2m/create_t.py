from oneM2M_functions import *

server = "https://esw-onem2m.iiit.ac.in"
cse = "/~/in-cse/in-name/"


# ------------------------------------------
# Fill code here to create AE
# specified by the URI
# ------------------------------------------
ae = "Indoor-Air-Pollution"
create_ae(server+cse, ae)
# ------------------------------------------
create_cnt(server+cse+ae, "Values")
create_cnt(server+cse+ae, "Description")
create_data_cin(server+cse+ae+"/Description", "[CO2, VOC-Index , PM2.5, PM10]")