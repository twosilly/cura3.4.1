# This PostProcessing Plugin script is released
# under the terms of the AGPLv3 or higher

from ..Script import Script
#from UM.Logger import Logger
# from cura.Settings.ExtruderManager import ExtruderManager

from UM.Logger import Logger
import re
import random
class ColorChange(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        OutPut="""{
            "name":"切换层",
            "key": "ColorChange",
            "metadata": {},
            "version": 2,
            "settings":
            {
               """

        bbb = 5
        ccc = """                                    
                "layer_number":    
                {
                    "label": "换色层高：",
                    "description": "",
                    "unit": "%",
                    "type": "float",
                    "default_value": 0,
                    "minimum_value": 0,
                    "minimum_value_warning": 0,
                    "maximum_value_warning": 100
                },
                "a_trigger":
                {
                    "label": "切换到挤出头：",
                    "description": "",
                    "type": "enum",
                    "options": {"T0":"T0","T1":"T1"},
                    "default_value": "T1"
                }
            }
        }
        """
        return OutPut + ccc



    def getHeight(self, dat):
        try:
            global totalLayer
            totalLayer = -1
            height = 0.0
            prepareEndFlag = False
            done = False
            for layerDat in dat:
                lines = layerDat.split('\n')
                for line in lines:
                    if line.endswith(';End of Gcode'):
                        done = True
                        break
                    if line:
                        code = self.getValue(line, 'G1 X', None)
                        if code == 1 or code == 0:
                            pass
                        height = self.getValue(line, 'Z', height)

                    elif line.startswith(';LAYER_COUNT:'):
                        totalLayer = int(self.getValue(line, ';LAYER_COUNT:', totalLayer))
                    elif line.startswith(';End of Gcode'):
                        done = True
                        break
                    elif line.startswith(';LAYER:'):
                        if int(self.getValue(line, ';LAYER:', 0)) == totalLayer - 1:
                            prepareEndFlag = True
                    else:
                        if prepareEndFlag:
                            done = True
                            break

                if done:
                    break
            return round(float(height),2)
        except Exception as e:
            print(e)
            return 0.0





    def execute(self, data: list):
        height = self.getHeight(data)
        aaaaa = ','.join(data)
        CGG = re.findall(r"(?<=LAYER_COUNT:).*?(?=\n)", aaaaa)
        CHH=float(height)/float(CGG[0])
        """data is a list. Each index contains a layer"""
        xv = self.getSettingValueByKey("a_trigger")
        lm2 = str(self.getSettingValueByKey("layer_number"))

        stringcopy = ""
        stringcopy = stringcopy + "G91 ;relative \n"
        stringcopy = stringcopy + xv + "\n"
        stringcopy = stringcopy + "G90;absolute\n"



        lm1 = lm2.split(',')
        if len(lm1) > 0:
            aaaaa = ','.join(data)
            MXSS = aaaaa.count('LAYER_COUNT')
            CGG = re.findall(r"(?<=LAYER_COUNT:).*?(?=\n)", aaaaa)

            ltemp = []
            ltemp = lm1[:]
            if MXSS > 1:
                    for i in ltemp:
                        lm1.append(str(int(i)+100))
            if MXSS > 2:
                    for i in ltemp:
                        lm1.append(str(int(i)+200))
            if MXSS > 3:
                    for i in ltemp:
                        lm1.append(str(int(i)+300))

            for temp2 in lm1:
                temp2 = int( temp2.strip() )
                temp2 = int( (int(CGG[0]))* temp2* 0.01 )
                if temp2 < len(data):
                    layer = data[ temp2 + 2 ]
                    lines = layer.split("\n")
                    lines.insert(2, stringcopy )
                    final_line = "\n".join( lines )
                    data[ temp2 + 2 ] = final_line
        return data