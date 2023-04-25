##############################################################################
# Script: OndeGPU.py
#-----------------------------------------------------------------------------
# Desc: Script to check availability of GPUs in various stores
# Author: Miguel Silva
# Contact: github.com/miguelpmsilva
#-----------------------------------------------------------------------------
# Change History:
# Update Date:          
##############################################################################

##############################################################################
# Imports
##############################################################################
from colorama import init, Back, Style
from bs4 import BeautifulSoup
import telegram
import requests
import time

init()

##############################################################################
# Custom Variables - Change this for your needs
##############################################################################

Lojas = {
    "PCDIGA" : {
        "AMD RX 5600 XT" : {
            "links" : ["placa-grafica-msi-radeon-rx-5600-xt-gaming-mx-6g-0",
                    "placa-grafica-xfx-radeon-rx-5600-xt-14gbps-6gb-thicc-ii-pro-rx-56xt6df46",
                    "placa-grafica-xfx-radeon-rx-5600-xt-14gbps-6gb-thicc-iii-pro-rx-56xt6tf48",
                    "placa-grafica-xfx-radeon-rx-5600-xt-14gbps-6gb-thicc-iii-ultra-rx-56xt6tb48",
                    "placa-grafica-xfx-radeon-rx-5600-xt-12gbps-6gb-thicc-ii-pro-rx-56xt6dfd6",
                    "placa-grafica-xfx-radeon-rx-5600-xt-12gbps-6gb-thicc-iii-ultra-rx-56xt6tbd8",
                    "placa-grafica-msi-radeon-rx-5600-xt-mech-oc-6g-912-v381-227",
                    "placa-grafica-msi-radeon-rx-5600-xt-gaming-x-6g-912-v381-232",
                    "placa-grafica-sapphire-radeon-rx-5600-xt-pulse-6gb-11296-01-20g",
                    "placa-grafica-asus-tuf-gaming-x3-radeon-rx-5600-xt-6gb-oc-90yv0ea0-m0na00",
                    "placa-grafica-asus-rog-strix-radeon-rx-5600-xt-6g-oc-90yv0eb0-m0na00",
                    "placa-grafica-sapphire-radeon-rx-5600-xt-be-pulse-6gb-11296-05-20g",
                    "placa-grafica-asus-rog-strix-radeon-rx-5600-xt-6g-top-90yv0eb2-m0na00",
                    "placa-grafica-powercolor-radeon-rx-5600-xt-red-devil-6gb-oc-axrx-5600xt-6gbd6-3dhe-oc"],
            "PrecoMax" : 300.00
        },
        "AMD RX 5700 XT" : {
            "links" : ["placa-grafica-asus-rog-strix-radeon-rx-5700-xt-8gb-oc-90yv0d90-m0na00",
                    "placa-grafica-xfx-radeon-rx-5700-xt-8gb-thicc-iii-ultra-rx-57xt8tbd8",
                    "placa-grafica-powercolor-radeon-rx-5700-xt-red-dragon-8gb-oc-axrx-5700xt-8gbd6-3dhr-oc",
                    "placa-grafica-sapphire-radeon-rx-5700-xt-nitro-be-8gb-oc-11293-10-40g",
                    "placa-grafica-gigabyte-radeon-rx-5700-xt-gaming-8gb-oc-gv-r57xtgaming-oc-8gd",
                    "placa-grafica-sapphire-radeon-rx-5700-xt-nitro-8gb-oc-11293-03-40g",
                    "placa-grafica-msi-radeon-rx-5700-xt-mech-oc-8g-recondicionado-912-v381-015"],
            "PrecoMax" : 450.00
        },
        "NVIDIA RTX 3060 Ti" : {
            "links" : ["placa-grafica-gigabyte-geforce-rtx-3060-ti-eagle-8gb-gddr6-gvn306teo-00-g",
                    "placa-grafica-asus-tuf-gaming-rtx-3060-ti-8gb-gddr6-90yv0g11-m0na00",
                    "placa-grafica-asus-dual-geforce-rtx-3060-ti-8gb-gddr6-90yv0g13-m0na00",
                    "placa-grafica-pny-geforce-rtx-3060-ti-8gb-gddr6-uprising-dual-fan-vcg3060t8dfmpb",
                    "placa-grafica-pny-geforce-rtx-3060-ti-8gb-gddr6-xlr8-revel-epic-x-dual-fan-vcg3060t8dfxppb",
                    "placa-grafica-zotac-gaming-geforce-rtx-3060-ti-8gb-gddr6-twin-edge-oc-zt-a30610h-10m",
                    "placa-grafica-zotac-gaming-geforce-rtx-3060-ti-8gb-gddr6-twin-edge-zt-a30610e-10m",
                    "placa-grafica-gigabyte-geforce-rtx-3060-ti-eagle-oc-8gb-gddr6-gvn306teo-00-10",
                    "placa-grafica-gigabyte-geforce-rtx-3060-ti-aorus-master-8gb-gddr6-gvn306tam-00-10",
                    "placa-grafica-gigabyte-geforce-rtx-3060-ti-gaming-oc-pro-8gb-gddr6-gvn306tgop-00-10",
                    "placa-grafica-gigabyte-geforce-rtx-3060-ti-gaming-oc-8gb-gddr6-gvn306tgo-00-10",
                    "placa-grafica-msi-geforce-rtx-3060-ti-ventus-2x-8gb-gddr6-oc-912-v390-009",
                    "placa-grafica-msi-geforce-rtx-3060-ti-ventus-3x-8gb-gddr6-oc-912-v397-001",
                    "placa-grafica-msi-geforce-rtx-3060-ti-gaming-x-trio-8gb-gddr6-912-v390-053",
                    "placa-grafica-asus-rog-strix-geforce-rtx-3060-ti-8gb-gddr6-oc-90yv0g02-m0na00",
                    "placa-grafica-asus-rog-strix-geforce-rtx-3060-ti-8gb-gddr6-90yv0g00-m0na00",
                    "placa-grafica-asus-tuf-gaming-rtx-3060-ti-8gb-gddr6-oc-90yv0g10-m0na00",
                    "placa-grafica-asus-dual-geforce-rtx-3060-ti-8gb-gddr6-oc-90yv0g12-m0na00",
                    "placa-grafica-msi-geforce-rtx-3060-ti-ventus-2x-ocv1-8gb-gddr6-oc-912-v397-003",
                    "placa-grafica-zotac-gaming-geforce-rtx-3060-amp-12gb-gddr6-white-edition-zt-a30600f-10p",
                    "placa-grafica-zotac-gaming-geforce-rtx-3060-12gb-gddr6-twin-edge-oc-zt-a30600h-10m",
                    "placa-grafica-zotac-gaming-geforce-rtx-3060-12gb-gddr6-twin-edge-zt-a30600e-10m"],
            "PrecoMax" : 600.00
        },
        "NVIDIA RTX 3070" : {
            "links" : ["placa-grafica-asus-tuf-gaming-geforce-rtx-3070-8gb-gddr6-oc-edition-90yv0fq6-m0na00",
                    "placa-grafica-gigabyte-geforce-rtx-3070-eagle-8gb-gddr6-gv-n3070eagle-8gd",
                    "placa-grafica-zotac-gaming-geforce-rtx-3070-8gb-gddr6-amp-holo-zt-a30700f-10p",
                    "placa-grafica-asus-rog-strix-geforce-rtx-3070-8gb-gddr6-oc-editon-90yv0fr1-m0na00",
                    "placa-grafica-gigabyte-geforce-rtx-3070-aorus-master-8gb-gddr6-gv-n3070aorus-m-8gd",
                    "placa-grafica-pny-geforce-rtx-3070-8gb-gddr6-xlr8-gaming-epic-x-rgb-triple-fan-vcg30708tfxppb",
                    "placa-grafica-asus-rog-strix-geforce-rtx-3070-8gb-gddr6-90yv0fr0-m0na00",
                    "placa-grafica-zotac-gaming-geforce-rtx-3070-8gb-gddr6-twin-edge-oc-white-edition-zt-a30700j-10p",
                    "placa-grafica-gigabyte-geforce-rtx-3070-gaming-oc-8g-gv-n3070gaming-oc-8gd",
                    "placa-grafica-asus-dual-geforce-rtx-3070-8gb-gddr6-oc-editon-90yv0fq0-m0na00",
                    "placa-grafica-zotac-gaming-geforce-rtx-3070-8gb-gddr6-twin-edge-oc-zt-a30700h-10p",
                    "placa-grafica-gigabyte-geforce-rtx-3070-vision-oc-8gb-gddr6-gv-n3070vision-oc-8gd",
                    "placa-grafica-gigabyte-geforce-rtx-3070-eagle-8gb-gddr6-oc-edition-gv-n3070eagle-oc-8gd",
                    "placa-grafica-msi-geforce-rtx-3070-suprim-x-8g-912-v390-005",
                    "placa-grafica-pny-geforce-rtx-3070-8gb-gddr6-dual-fan-vcg30708dfmpb",
                    "placa-grafica-msi-geforce-rtx-3070-ventus-2x-8g-oc-912-v390-008",
                    "placa-grafica-zotac-gaming-geforce-rtx-3070-8gb-gddr6-twin-edge-zt-a30700e-10p"],
            "PrecoMax" : 650.00
        },
        "NVIDIA RTX 3080" : {
            "links" : ["placa-grafica-zotac-gaming-geforce-rtx-3080-10gb-gddr6x-trinity-zt-a30800d-10p",
                    "placa-grafica-msi-geforce-rtx-3080-ventus-3x-10g-oc-912-v389-001",
                    "placa-grafica-pny-geforce-rtx-3080-10gb-gddr6x-xlr8-gaming-epic-x-rgb-triple-fan-vcg308010tfxmpb",
                    "placa-grafica-pny-geforce-rtx-3080-10gb-gddr6x-xlr8-gaming-epic-x-rgb-triple-fan-vcg308010tfxppb",
                    "placa-grafica-asus-tuf-gaming-geforce-rtx-3080-10gb-gddr6x-90yv0fb0-m0nm00",
                    "placa-grafica-zotac-gaming-geforce-rtx-3080-10gb-gddr6x-trinity-oc-zt-a30800j-10p",
                    "placa-grafica-asus-tuf-gaming-geforce-rtx-3080-10gb-gddr6x-oc-edition-90yv0fb1-m0nm00",
                    "placa-grafica-msi-geforce-rtx-3080-gaming-x-trio-10g-912-v389-005",
                    "placa-grafica-msi-geforce-rtx-3080-suprim-x-10g-912-v389-006",
                    "placa-grafica-gigabyte-geforce-rtx-3080-eagle-10gb-gddr6x-oc-edition-gvn3080eo-00-10",
                    "placa-grafica-asus-rog-strix-geforce-rtx-3080-10gb-gddr6x-90yv0fa0-m0nm00",
                    "placa-grafica-gigabyte-geforce-rtx-3080-gaming-10gb-gddr6x-oc-edition-gvn3080go-00-10",
                    "placa-grafica-gigabyte-geforce-rtx-3080-vision-10gb-gddr6x-oc-edition-gv-n3080vision-oc-10",
                    "placa-grafica-asus-rog-strix-geforce-rtx-3080-10gb-gddr6x-oc-edition-90yv0fa1-m0nm00",
                    "placa-grafica-zotac-gaming-geforce-rtx-3080-10gb-gddr6x-amp-holo-zt-a30800f-10p",
                    "placa-grafica-gigabyte-geforce-rtx-3080-aorus-master-10gb-gddr6x-gvn3080am-00-10",
                    "placa-grafica-asus-ekwb-geforce-rtx-3080-10gb-gddr6x-90yv0f60-m0nm00",
                    "placa-grafica-gigabyte-geforce-rtx-3080-aorus-xtreme-10gb-gddr6x-gv-n3080aorus-x-10gd"],
            "PrecoMax" : 800.00
        }
    },
    
    "Globaldata" : {
        "AMD RX 5600 XT" : {
            "links" : ["grafica-asus-radeon-rx-5600-xt-rog-strix-oc-6gb-90yv0eb0-m0na00",
                    "grafica-sapphire-radeon-rx-5600-xt-pulse-6gb-gd6-11296-01-20g",
                    "grafica-asus-radeon-rx-5600-xt-tuf-gaming-x3-evo-oc-6gb-90yv0ea0-m0na00"],
            "PrecoMax" : 300.00
        },
        "AMD RX 5700 XT" : {
            "links" : ["grafica-sapphire-radeon-rx-5700-xt-pulse-8gb-gd6-11293-01-20g",
                    "grafica-gigabyte-radeon-rx-5700-xt-gaming-oc-8gb-gv-r57xtgaoc8g",
                    "grafica-asus-radeon-rx-5700-xt-tuf-gaming-x3-oc-8gb-90yv0da0-m0na00",
                    "grafica-sapphire-radeon-rx-5700-xt-nitro-8gb-gd6-11293-03-40g",
                    "grafica-powercolor-radeon-rx-5700-xt-red-devil-8gb-gd6-rx5700xt8gbd6-3dhe",
                    "grafica-asus-radeon-rx-5700-xt-rog-strix-gaming-oc-8gb-90yv0d90-m0na00",
                    "grafica-msi-radeon-rx-5700-xt-mech-oc-8g-4719072666064",
                    "grafica-msi-radeon-rx-5700-xt-gaming-x-8g-912-v381-032"],
            "PrecoMax" : 450.00
        },
        "NVIDIA RTX 3060 Ti" : {
            "links" : ["grafica-msi-geforce-rtx-3060-ti-ventus-2x-ocv1-8g-912-v397-003",
                    "grafica-zotac-geforce-rtx-3060-ti-twin-edge-oc-8gb-gd6-zt-a30610h-10m",
                    "grafica-zotac-geforce-rtx-3060-ti-twin-edge-8gb-gd6-zt-a30610e-10m",
                    "grafica-asus-geforce-rtx-3060-ti-dual-8gb-gd6-90yv0g13-m0na00",
                    "grafica-asus-geforce-rtx-3060-ti-dual-oc-8gb-gd6-90yv0g12-m0na00",
                    "grafica-asus-geforce-rtx-3060-ti-tuf-gaming-8gb-gd6-90yv0g11-m0na00",
                    "grafica-asus-geforce-rtx-3060-ti-tuf-gaming-oc-8gb-gd6-90yv0g10-m0na00",
                    "grafica-asus-geforce-rtx-3060-ti-rog-strix-oc-8gb-gd6-90yv0g02-m0na00",
                    "grafica-asus-geforce-rtx-3060-ti-rog-strix-8gb-gd6-90yv0g00-m0na00",
                    "grafica-msi-geforce-rtx-3060-ti-gaming-x-trio-8g-912-v390-053",
                    "grafica-msi-geforce-rtx-3060-ti-ventus-3x-oc-8g-4719072763152",
                    "grafica-gigabyte-geforce-rtx-3060-ti-gaming-oc-pro-8gb-gd6-gvn306tgop-00-10",
                    "grafica-gigabyte-geforce-rtx-3060-ti-gaming-oc-8gb-gd6-gvn306tgo-00-10",
                    "grafica-gigabyte-geforce-rtx-3060-ti-eagle-oc-8gb-gd6-gvn306teo-00-10",
                    "grafica-gigabyte-geforce-rtx-3060-ti-eagle-8gb-gd6-gvn306te-00-10",
                    "grafica-gigabyte-geforce-rtx-3060-ti-aorus-master-8gb-gd6-gvn306tam-00-10"],
            "PrecoMax" : 620.00
        },
        "NVIDIA RTX 3070" : {
            "links" : ["grafica-zotac-geforce-rtx-3070-twin-edge-8gb-gd6-zt-a30700e-10p",
                    "grafica-asus-geforce-rtx-3070-dual-8gb-gd6-90yv0fq1-m0na00",
                    "grafica-zotac-geforce-rtx-3070-twin-edge-oc-8gb-gd6-zt-a30700h-10p",
                    "grafica-zotac-geforce-rtx-3070-twin-edge-white-oc-8gb-gd6-zt-a30700j-10p",
                    "grafica-msi-geforce-rtx-3070-ventus-2x-oc-8g-912-v390-008",
                    "grafica-asus-geforce-rtx-3070-dual-oc-8gb-gd6-90yv0fq0-m0na00",
                    "grafica-zotac-geforce-rtx-3070-amp-holo-8gb-gd6-zt-a30700f-10p",
                    "grafica-gigabyte-geforce-rtx-3070-gaming-oc-8gb-gd6-gv-n3070gam-oc-8g",
                    "grafica-gigabyte-geforce-rtx-3070-eagle-oc-8gb-gd6-gvn3070eo-00-10",
                    "grafica-gigabyte-geforce-rtx-3070-vision-oc-8gb-gd6-gvn3070vo-00-10",
                    "grafica-msi-geforce-rtx-3070-ventus-3x-oc-8g-912-v390-007",
                    "grafica-gigabyte-geforce-rtx-3070-aorus-master-8gb-gd6-gvn3070am-00-11",
                    "grafica-asus-geforce-rtx-3070-tuf-gaming-oc-8gb-gd6-90yv0fq6-m0na00",
                    "grafica-msi-geforce-rtx-3070-gaming-x-trio-8g-912-v390-006",
                    "grafica-asus-geforce-rtx-3070-rog-strix-8gb-gd6-90yv0fr0-m0na00",
                    "grafica-msi-geforce-rtx-3070-suprim-x-8g-4719072763046",
                    "grafica-asus-geforce-rtx-3070-rog-strix-oc-8gb-gd6-90yv0fr1-m0na00",
                    "grafica-asus-geforce-rtx-3070-rog-strix-white-8gb-gd6-90yv0fr6-m0na00",
                    "grafica-asus-geforce-rtx-3070-ek-8gb-gd6-90yv0fu0-m0na00",
                    "grafica-asus-geforce-rtx-3070-rog-strix-oc-white-8gb-gd6-90yv0fr5-m0na00"],
            "PrecoMax" : 700.00
        },
        "NVIDIA RTX 3080" : {
            "links" : ["grafica-msi-geforce-rtx-3080-ventus-3x-10g-oc-4719072762520",
                    "grafica-zotac-geforce-rtx-3080-amp-extreme-holo-10gb-gd6x-zt-a30800b-10p",
                    "grafica-msi-geforce-rtx-3080-gaming-x-trio-10g-4719072762544",
                    "grafica-asus-geforce-rtx-3080-tuf-gaming-10gd6x-90yv0fb0-m0nm00",
                    "grafica-msi-geforce-rtx-3080-suprim-x-10g-4719072762537",
                    "grafica-asus-geforce-rtx-3080-rog-strix-oc-10gd6x-90yv0fa1-m0nm00",
                    "grafica-gigabyte-geforce-rtx-3080-aorus-xtreme-10gb-gd6x-gvn3080ax-00-10",
                    "grafica-zotac-geforce-rtx-3080-trinity-oc-10gb-gd6x-zt-a30800j-10p",
                    "grafica-gigabyte-geforce-rtx-3080-vision-oc-10gb-gd6x-gvn3080visoc-10",
                    "grafica-asus-geforce-rtx-3080-rog-strix-10gd6x-90yv0fa0-m0nm00",
                    "grafica-zotac-geforce-rtx-3080-amp-holo-10gb-gd6x-zt-a30800f-10p",
                    "grafica-gigabyte-geforce-rtx-3080-eagle-oc-10gb-gd6x-gvn3080eagleoc10gd",
                    "grafica-asus-geforce-rtx-3080-tuf-gaming-oc-10gd6x-90yv0fb1-m0nm00",
                    "grafica-gigabyte-geforce-rtx-3080-eagle-10gb-gd6x-gv-n3080eagle-10gd",
                    "grafica-asus-geforce-rtx-3080-ek-10gd6x-90yv0f60-m0nm00",
                    "grafica-asus-geforce-rtx-3080-rog-strix-oc-white-10gd6x-90yv0fa5-m0nm00",
                    "grafica-asus-geforce-rtx-3080-rog-strix-white-10gd6x-90yv0fa6-m0nm00",
                    "grafica-gigabyte-geforce-rtx-3080-aorus-master-oc-10gb-gd6x-gvn3080am-00-10",
                    "grafica-zotac-geforce-rtx-3080-trinity-10gb-gd6x-zt-a30800d-10p",
                    "grafica-gigabyte-geforce-rtx-3080-gaming-oc-10gb-gd6x-gvn3080gamingoc10g"],
            "PrecoMax" : 800.00
        }
    },
    
    "PcComponentes" : {
        "AMD RX 5600 XT" : {
            "links" : ["sapphire-pulse-radeon-rx-5600-xt-6gb-gddr6"],
            "PrecoMax" : 300.00
        },
        "AMD RX 5700 XT" : {
            "links" : ["asus-radeon-rx-5700-xt-rog-strix-gaming-oc-edition-8gb-gddr6",
                    "powercolor-red-devil-radeon-rx-5700-xt-8-gb-gddr6",
                    "gigabyte-amd-radeon-rx-5700-xt-gaming-oc-8gb-gddr6",
                    "gigabyte-aorus-radeon-rx-5700-xt-8gb-gddr6",
                    "sapphire-nitro-radeon-rx-5700-xt-8gb-gddr6",
                    "gigabyte-amd-radeon-rx-5700-xt-8gb-gddr6",
                    "msi-amd-radeon-rx-5700-xt-mech-oc-8gb-gddr6",
                    "gigabyte-amd-radeon-rx-5700-8gb-gddr6",
                    "powercolor-red-devil-radeon-rx-5700-xt-8gb-gddr6-reacondicionado",
                    "gigabyte-amd-radeon-rx-5700-xt-gaming-oc-8gb-gddr6-reacondicionado",
                    "asus-amd-radeon-rx-5700-dual-evo-oc-edition-8gb-gddr6",
                    "gigabyte-amd-radeon-rx-5700-gaming-oc-8gb-gddr6",
                    "sapphire-amd-radeon-rx-5700-8gb-gddr6"],
            "PrecoMax" : 450.00
        },
        "AMD Radeon VII" : {
            "links" : ["sapphire-radeon-vii-16-gb-hbm2"],
            "PrecoMax" : 800.00
        },
        "NVIDIA RTX 3060 Ti" : {
            "links" : ["evga-geforce-rtx-3060-ti-ftw3-ultra-8gb-gddr6-reacondicionado",
                    "gigabyte-geforce-rtx-3060-ti-gaming-oc-pro-8gb-gddr6-reacondicionado",
                    "zotac-geforce-rtx-3060ti-d6-twin-edge-oc-8gb-gddr6-reacondicionado",
                    "msi-rtx-3060-ti-ventus-2x-oc-8gb-gddr6-reacondicionado",
                    "asus-geforce-rtx-3060ti-dual-o8g-8gb-gddr6-reacondicionado",
                    "asus-rog-strix-geforce-rtx-3060ti-o8g-gaming-8gb-gddr6-reacondicionado",
                    "asus-tuf-geforce-rtx-3060ti-o8g-gaming-8gb-gddr6-reacondicionado",
                    "msi-rtx-3060-ti-gaming-x-trio-8gb-gddr6-reacondicionado",
                    "zotac-geforce-rtx-3060-ti-d6-twin-edge-8gb-gddr6-reacondicionado",
                    "evga-geforce-rtx-3060-ti-xc-8gb-gddr6-reacondicionado",
                    "gigabyte-geforce-rtx-3060-ti-eagle-oc-8gb-gddr6-reacondicionado",
                    "gigabyte-aorus-geforce-rtx-3060-ti-master-8gb-gddr6-reacondicionado",
                    "pny-geforce-rtx-3060ti-xlr8-gaming-revel-epic-x-rgb-edition-8gb-gddr6-reacondicionado"],
            "PrecoMax" : 600.00
        },
        "NVIDIA RTX 3070" : {
            "links" : ["gigabyte-geforce-rtx-3070-gaming-oc-8gb-gddr6-reacondicionado",
                    "evga-geforce-rtx-3070-xc3-ultra-gaming-8gb-gddr6-reacondicionado",
                    "gigabyte-aorus-geforce-rtx-3070-master-8gb-gddr6-reacondicionado",
                    "gigabyte-geforce-rtx-3070-eagle-oc-8gb-gddr6-reacondicionado",
                    "zotac-gaming-geforce-rtx-3070-twin-edge-oc-8gb-gddr6-reacondicionado",
                    "msi-geforce-rtx-3070-gaming-x-trio-8gb-gddr6-reacondicionado",
                    "msi-geforce-rtx-3070-ventus-3x-oc-8gb-gddr6-reacondicionado",
                    "gigabyte-geforce-rtx-3070-vision-oc-8gb-gddr6-reacondicionado",
                    "gigabyte-geforce-rtx-3070-eagle-8gb-gddr6-reacondicionado",
                    "asus-tuf-gaming-geforce-rtx-3070-oc-8gb-gddr6-reacondicionado",
                    "msi-geforce-rtx-3070-ventus-2x-oc-8gb-gddr6-reacondicionado",
                    "zotac-gaming-geforce-rtx-3070-twin-edge-8gb-gddr6-reacondicionado",
                    "asus-geforce-rtx-3070-dual-8gb-gddr6-reacondicionado",
                    "asus-geforce-rtx-3070-dual-oc-edition-8gb-gddr6-reacondicionado",
                    "asus-rog-strix-gaming-geforce-rtx-3070-oc-8gb-gddr6-reacondicionado",
                    "pny-geforce-rtx-3070-xlr8-gaming-revel-epic-x-rgb-triple-fan-edition-8gb-gddr6-reacondicionado",
                    "asus-ekwb-geforce-rtx-3070-8gb-gddr6-reacondicionado"],
            "PrecoMax" : 700.00
        }
    },
    
    "ClickFiel" : {
        "AMD RX 5600 XT" : {
            "links" : ["2/8683/Placa-Grafica-Asus-TUF-Gaming-X3-Radeon-RX-5600-XT-6GB-OC",
                    "2/8684/Placa-Grafica-Asus-ROG-Strix-Radeon-RX-5600-XT-6G-OC"],
            "PrecoMax" : 300.00
        },
        "AMD RX 5700 XT" : {
            "links" : ["2/8306/Placa-Grafica-Asus-TUF-Gaming-X3-Radeon-RX-5700-XT-8GB-OC",
                    "2/8488/Placa-Grafica-Asus-ROG-Strix-Radeon-RX-5700-XT-8GB-OC"],
            "PrecoMax" : 450.00
        },
        "NVIDIA RTX 3060 Ti" : {
            "links" : ["2/9759/Placa-Grafica-Asus-Dual-GeForce-RTX-3060Ti-8GB-GDDR6",
                    "2/9822/Placa-Grafica-Gigabyte-GeForce-RTX-3060Ti-Eagle-OC-8GB-GDDR6",
                    "2/9760/Placa-Grafica-Asus-TUF-Gaming-GeForce-RTX-3060Ti-8GB-GDDR6",
                    "2/9778/Placa-Grafica-Gigabyte-GeForce-RTX-3060Ti-Gaming-PRO-OC-8GB-GDDR6",
                    "2/9761/Placa-Grafica-Asus-TUF-Gaming-GeForce-RTX-3060Ti-8GB-GDDR6-OC",
                    "2/9777/Placa-Grafica-Gigabyte-GeForce-RTX-3060Ti-Gaming-OC-8GB-GDDR6",
                    "2/9758/Placa-Grafica-Asus-Dual-GeForce-RTX-3060Ti-8GB-GDDR6-OC-Editon",
                    "2/9762/Placa-Grafica-Asus-ROG-Strix-GeForce-RTX-3060Ti-8GB-GDDR6",
                    "2/9763/Placa-Grafica-Asus-ROG-Strix-GeForce-RTX-3060Ti-8GB-GDDR6-OC"],
            "PrecoMax" : 600.00
        },
        "NVIDIA RTX 3070" : {
            "links" : ["2/9821/Placa-Grafica-Gigabyte-GeForce-RTX-3070-Eagle-8GB-GDDR6-OC-Edition",
                    "2/9611/Placa-Grafica-Asus-GeForce-RTX-3070-ROG-Strix-8GB-GDDR6",
                    "2/9564/Placa-Grafica-Asus-Dual-GeForce-RTX-3070-8GB-GDDR6-OC-Editon",
                    "2/9612/Placa-Grafica-Asus-GeForce-RTX-3070-TUF-Gaming-OC-8GB-GDDR6",
                    "2/9807/Placa-Grafica-Gigabyte-GeForce-RTX-3070-Aorus-Master-8GB-GDDR6",
                    "2/9635/Placa-Grafica-Gigabyte-GeForce-RTX-3070-Gaming-OC-8GB-GDDR6",
                    "2/9912/Placa-Grafica-Gigabyte-GeForce-RTX-3070-Vision-OC-8GB-GDDR6"],
            "PrecoMax" : 700.00
        }
    },
    
    "nanoChip" : {
        "AMD RX 5700 XT" : {
            "links" : ["msi-radeon-rx5700-evoke-oc-8gb-ddr6-pci-e-40-msirx5700evoke8oc",
                    "asus-radeon-rx5700-dual-evo-oc-8gb-ddr6-pci-e-40-asusrx5700dlevo8gb"],
            "PrecoMax" : 450.00
        },
        "NVIDIA RTX 3060 Ti" : {
            "links" : ["asus-geforce-rtx3060-ti-dual-oc-8gb-ddr6-pci-e-30-asusdualortx3060ti",
                    "asus-geforce-rtx3060-ti-tuf-gaming-oc-8gb-gddr6-asusrtx3060titfoc8",
                    "nvidia/msi-geforce-rtx3060-ti-ventus-2x-8gb-oc-gddr6-msirtx3060tiven2x8"],
            "PrecoMax" : 600.00
        },
        "NVIDIA RTX 3070" : {
            "links" : ["asus-geforce-rtx-3070-dual-8gb-gddr6-asusrtx3070oc8g",
                    "gigabyte-geforce-rtx-3070-eagle-8gb-ddr6-gigabyteg3070eag",
                    "gigabyte-geforce-rtx-3070-eagle-oc-8gb-ddr6-gigabyteg3070eagoc"],
            "PrecoMax" : 650.00
        },
        "NVIDIA RTX 3080" : {
            "links" : ["gigabyte-geforce-rtx-3080-eagle-oc-10gb-ddr6-gigabytegvn3080eag",
                    "asus-geforce-rtx3080-tuf-gaming-10gb-gddr6-asusrtx3080tuf10gb"],
            "PrecoMax" : 750.00
        }
    },

    "CHIP7" : {
        "AMD RX 5700 XT" : {
            "links" : ["65527-msi-radeon-rx-5700-xt-evoke-oc-8-gb-gddr6-4719072666057.html",
                    "66539-sapphire-pulse-radeon-rx-5700-xt-8-gb-gddr6-4895106287693.html"],
            "PrecoMax" : 450.00
        },
        "NVIDIA RTX 3060 Ti" : {
            "links" : ["90770-placa-grafica-kfa2-rtx-3060-ti-1-click-oc-8gb-gddr6-36ISL6MD1VDK.html",
                    "91755-asus-dual-rtx3060ti-8g-nvidia-geforce-rtx-3060-ti-8-gb-gddr6-4718017962995.html",
                    "90206-asus-dual-rtx3060ti-o8g-nvidia-geforce-rtx-3060-ti-8-gb-gddr6-4718017963046.html",
                    "90155-gigabyte-geforce-rtx-3060-ti-eagle-8g-nvidia-8-gb-gddr6-4719331307776.html",
                    "91754-asus-tuf-gaming-tuf-rtx3060ti-8g-gaming-nvidia-geforce-rtx-3060-ti-8-gb-gddr6-4718017953184.html"],
            "PrecoMax" : 600.00
        }
    },

    "Castro Electrónica" : {
        "AMD RX 5700 XT" : {
            "links" : ["placa-grafica-radeon-rx-5700-xt-red-devil-8gb-oc--powercolor"],
            "PrecoMax" : 450.90
        },
        "NVIDIA RTX 3073" : {
            "links" : ["placa-grafica-geforce-rtx-3070-ventus-2x-8g-oc--msi",
                    "placa-grafica-geforce-rtx-3070-gaming-oc-8g--gigabyte",
                    "placa-grafica-geforce-rtx-3070-8gb-xlr8-gaming-epic-x-rgb-triple-fan--pny",
                    "placa-grafica-geforce-rtx-3070-8gb-tuf-gaming-oc--asus"],
            "PrecoMax" : 650.00
        }
    }
}

##############################################
# Script Body
##############################################

def SendTelegramMessage(loja,modelo,preco,preco_sIVA,PrecoMax,link):
    print()
    bot=telegram.Bot("TELEGRAM_BOT_TOKEN") #Token do Telegram Bot
    chat_id="CHAT_ID" #CHAT ID
    keyboard = [[telegram.InlineKeyboardButton(loja,url=link)]]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id,"<b>GRÁFICA DISPONÍVEL</b>\n\nLOJA: "+loja+"\nMODELO: "+modelo+"\nPREÇO: %.2f€" %preco+"\nPREÇO S/ IVA: %.2f€" %preco_sIVA+"\nRECOMENDADO: %.2f€" %PrecoMax,reply_markup=reply_markup,parse_mode='HTML')

while True:
    for loja in Lojas:
        print('------------------------'+loja+'----------------------------------')
        for modelo in Lojas[loja]:
            for link in Lojas[loja][modelo]["links"]:
                
                if loja == "PCDIGA":
                    try:
                        fullURL="https://www.pcdiga.com/"+link
                        source = requests.get(fullURL).text
                        soup = BeautifulSoup(source,'lxml')
                        div_grafica = soup.find('div', class_='page-title-wrapper product')
                        nome_grafica = div_grafica.h1.span.text
                        esgotado = soup.find('div', {"id": "skrey_estimate_date_product_page_wrapper"})
                        preco = float(soup.find('span', class_='price').text[:-2].replace(',', '.').replace(' ', ''))
                        preco_sIVA = preco/1.23
                        precoMax = Lojas[loja][modelo]["PrecoMax"]
                                        
                        try: esgotado_check = esgotado.span.text
                        except: esgotado_check = "EM STOCK"
                        
                        if esgotado_check == 'Sem stock':
                            print(nome_grafica + ' | ' + Back.RED + esgotado_check + Style.RESET_ALL + ' | ' + "%.2f€" %preco)
                        else:
                            print(nome_grafica + ' | ' + Back.GREEN + esgotado_check + Style.RESET_ALL + ' | ' + "PVP: %.2f€" %preco + ' | ' + "S/ IVA: %.2f€" %preco_sIVA + ' | ' + "Preço Máximo: %.2f€" %precoMax)
                            if preco < precoMax:
                                SendTelegramMessage(loja,modelo,preco,preco_sIVA,precoMax,fullURL)
                    except:
                            print("Não foi possível carregar a página")

                if loja == "Globaldata":
                    try:
                        fullURL="https://www.globaldata.pt/"+link
                        source = requests.get(fullURL).text
                        soup = BeautifulSoup(source,'lxml')
                        div_grafica = soup.find('div', class_='ck-product-cta-box-inner')
                        nome_grafica = div_grafica.h1.text
                        esgotado = soup.find('span', class_='availability-text')
                        preco = float(soup.find('span', class_='price__amount').text[1:-2].replace(',', '.').replace(' ', ''))
                        preco_sIVA = preco/1.23
                        precoMax = Lojas[loja][modelo]["PrecoMax"]
                        esgotado_check = esgotado.span.text
                    
                        if esgotado_check == 'Online - Esgotado':
                            print(nome_grafica + ' | ' + Back.RED + esgotado_check + Style.RESET_ALL + ' | ' + "%.2f€" %preco)
                        else:
                            print(nome_grafica + ' | ' + Back.GREEN + esgotado_check + Style.RESET_ALL + ' | ' + "PVP: %.2f€" %preco + ' | ' + "S/ IVA: %.2f€" %preco_sIVA + ' | ' + "Preço Máximo: %.2f€" %precoMax)
                            if preco < precoMax:
                                SendTelegramMessage(loja,modelo,preco,preco_sIVA,precoMax,fullURL)
                    except:
                        print("Não foi possível carregar a página")
                            
                if loja == "PcComponentes":
                    fullURL="https://www.pccomponentes.pt/"+link
                    source = requests.get(fullURL).text
                    soup = BeautifulSoup(source,'lxml')
                    div_nome_grafica = soup.find('div', class_='ficha-producto__encabezado')
                    nome_grafica = div_nome_grafica.h1.strong.text
                    esgotado = soup.find('div', id='btnsWishAddBuy')
                    preco = float(((soup.find('span', class_='baseprice').text)+(soup.find('span', class_='cents').text)).replace(',', '.'))
                    preco_sIVA = preco/1.23
                    precoMax = Lojas[loja][modelo]["PrecoMax"]
                    esgotado_check = esgotado.strong.text[1:-1]
                
                    if esgotado_check == 'Avisa-me':
                        print(nome_grafica + ' | ' + Back.RED + esgotado_check + Style.RESET_ALL + ' | ' + "%.2f€" %preco)
                    else:
                        print(nome_grafica + ' | ' + Back.GREEN + esgotado_check + Style.RESET_ALL + ' | ' + "PVP: %.2f€" %preco + ' | ' + "S/ IVA: %.2f€" %preco_sIVA + ' | ' + "Preço Máximo: %.2f€" %precoMax)
                        if preco < precoMax:
                            SendTelegramMessage(loja,modelo,preco,preco_sIVA,precoMax,fullURL)

                if loja == "ClickFiel":
                    fullURL="https://www.clickfiel.pt/"+link
                    source = requests.get(fullURL).text
                    soup = BeautifulSoup(source,'lxml')
                    div_grafica = soup.find('div', class_='produto-detalhes')
                    nome_grafica = div_grafica.h1.text
                    esgotado = soup.find('div', class_='disponibilidades')
                    preco = float(((soup.find('div', class_='produto-detalhes').find('span', class_='whole').text[1:])+(soup.find('div', class_='produto-detalhes').find('span', class_='fraction').text)).replace(',', '.'))
                    preco_sIVA = preco/1.23
                    precoMax = Lojas[loja][modelo]["PrecoMax"]
                    esgotado_check = esgotado.span.text

                    if esgotado_check == 'ESGOTADO':
                        print(nome_grafica + ' | ' + Back.RED + esgotado_check + Style.RESET_ALL + ' | ' + "%.2f€" %preco)
                    else:
                        print(nome_grafica + ' | ' + Back.GREEN + esgotado_check + Style.RESET_ALL + ' | ' + "PVP: %.2f€" %preco + ' | ' + "S/ IVA: %.2f€" %preco_sIVA + ' | ' + "Preço Máximo: %.2f€" %precoMax)
                        if preco < precoMax:
                            SendTelegramMessage(loja,modelo,preco,preco_sIVA,precoMax,fullURL)

                if loja == "Castro Electrónica":
                    fullURL="https://www.castroelectronica.pt/product/"+link
                    source = requests.get(fullURL).text
                    soup = BeautifulSoup(source,'lxml')
                    nome_grafica = soup.find('h1', class_='prod-detail-name').text
                    esgotado = soup.find('div', class_='product-availability-text')
                    preco = float((soup.find('span', class_='product-opportunity-new-price').text[:-1]).replace(',', '.'))
                    preco_sIVA = preco/1.23
                    precoMax = Lojas[loja][modelo]["PrecoMax"]

                    try: esgotado_check = esgotado.strong.text
                    except: esgotado_check = "EM STOCK"
                    if esgotado_check == 'Disponível Apenas Sob Encomenda' or 'Only Available Under Order':
                        print(nome_grafica + ' | ' + Back.RED + esgotado_check + Style.RESET_ALL + ' | ' + "%.2f€" %preco)
                    else:
                        print(nome_grafica + ' | ' + Back.GREEN + esgotado_check + Style.RESET_ALL + ' | ' + "PVP: %.2f€" %preco + ' | ' + "S/ IVA: %.2f€" %preco_sIVA + ' | ' + "Preço Máximo: %.2f€" %precoMax)
                        if preco < precoMax:
                            SendTelegramMessage(loja,modelo,preco,preco_sIVA,precoMax,fullURL)

                if loja == "CHIP7":
                    fullURL="https://www.chip7.pt/"+link
                    source = requests.get(fullURL).text
                    soup = BeautifulSoup(source,'lxml')
                    nome_grafica = soup.find('div', class_='product-title').find('h1').text
                    preco = float(soup.find('span', id='our_price_display').text[:-2].replace(',', '.').replace(' ', ''))
                    preco_sIVA = preco/1.23
                    precoMax = Lojas[loja][modelo]["PrecoMax"]
                    esgotado_check = soup.find('div', class_='chip7-disponibilidade').text[1:]

                    if esgotado_check == 'Dísponivel':
                        print(nome_grafica + ' | ' + Back.GREEN + esgotado_check + Style.RESET_ALL + ' | ' + "PVP: %.2f€" %preco + ' | ' + "S/ IVA: %.2f€" %preco_sIVA + ' | ' + "Preço Máximo: %.2f€" %precoMax)
                        if preco < precoMax:
                            SendTelegramMessage(loja,modelo,preco,preco_sIVA,precoMax,fullURL)
                    else:
                        print(nome_grafica + ' | ' + Back.RED + esgotado_check + Style.RESET_ALL + ' | ' + "%.2f€" %preco)


                if loja == "nanoChip":
                    fullURL="https://www.nanochip.pt/pt-pt/produto/"+link
                    source = requests.get(fullURL).text
                    soup = BeautifulSoup(source,'lxml')
                    nome_grafica = soup.find('title').text
                    preco = float(soup.find('div', class_='price_two').find("span").text[:-2].replace(',', '.'))
                    preco_sIVA = preco/1.23
                    precoMax = Lojas[loja][modelo]["PrecoMax"]
                    esgotado_check = soup.find('div', class_='stockinfo').find("span").text

                    if esgotado_check == 'ESGOTADO':
                        print(nome_grafica + ' | ' + Back.RED + esgotado_check + Style.RESET_ALL + ' | ' + "%.2f€" %preco)
                    else:
                        print(nome_grafica + ' | ' + Back.GREEN + esgotado_check + Style.RESET_ALL + ' | ' + "PVP: %.2f€" %preco + ' | ' + "S/ IVA: %.2f€" %preco_sIVA + ' | ' + "Preço Máximo: %.2f€" %precoMax)
                        if preco < precoMax:
                            SendTelegramMessage(loja,modelo,preco,preco_sIVA,precoMax,fullURL)

    time.sleep(60)
              
              
