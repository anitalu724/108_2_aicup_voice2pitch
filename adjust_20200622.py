import json, sys
import os
import operator

json_path = sys.argv[1]
jsobj = json.load(open(json_path))
BIAS = 1.2

TUNE_DICT = {"CB":[[48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76], [48, 60, 72]],
             "DB":[[50, 52, 54, 55, 57, 59, 61, 62, 64, 66, 67, 69, 71, 73, 74], [50, 62, 74]],
             "EB":[[49, 51, 52, 54, 56, 57, 59, 61, 63, 64, 66, 68, 69, 71, 73, 75, 76], [52, 64, 76]],
             "FB":[[45, 46, 48, 50, 52, 53, 55, 57, 58, 60, 62, 64, 65, 67, 69, 70, 72, 74, 76], [53, 65, 77]],
             "GB":[[48, 50, 52, 54, 55, 57, 59, 60, 62, 64, 66, 67, 69, 71, 72, 74, 76], [55, 67]],
             "AB":[[49, 50, 52, 54, 56, 57, 59, 61, 62, 64, 66, 68, 69, 71, 73, 74, 76], [57, 69]],
             "BB":[[49, 51, 52, 54, 56, 58, 59, 61, 63, 64, 66, 68, 70, 71, 73, 75, 76], [59, 71]],
             "JDB":[[49, 51, 53, 54, 56, 58, 60, 61, 63, 65, 66, 68, 70, 72, 73, 75, 76], []],
             "JEB":[[48, 50, 51, 53, 55, 56, 58, 60, 62, 63, 65, 67, 68, 70, 72, 74, 75], []],
             "JGB":[[49, 51, 53, 54, 56, 58, 59, 61, 63, 65, 66, 68, 70, 71, 73, 75], []],
             "JAB":[[49, 51, 53, 55, 56, 58, 60, 61, 63, 65, 67, 68, 70, 72, 73, 75, 76], []],
             "JBB":[[48, 50, 51, 53, 55, 57, 58, 60, 62, 63, 65, 67, 69, 70, 72, 74, 75], []]
             }

TONE_CHANGE_DICT = {"DB":[[48, 53, 60, 65],[49, 54, 61, 66]],
                   "EB":[[48, 50, 53, 55, 60, 62, 65, 67], [49, 51, 54, 56 ,61, 63, 66, 68]],
                   "FB":[[59, 71],[58, 70]],
                   "GB":[[53, 65],[54, 66]],
                   "AB":[[48, 53, 55, 60, 65, 67],[49, 54, 56, 61, 66, 68]],
                   "BB":[[48, 50, 53, 55, 57, 60, 62, 65, 67, 69],[49, 51, 54, 56, 58 ,61, 63, 66, 68, 70]]
             }


for i in range(1500):
    # i = 1
    
    index = str(i+1)
    print("__ " , index, " __")
    TUNE = int(jsobj[index][len(jsobj[index])-1][2])
    data_list = jsobj[index]
    pitch_list = [int(x[2]) for x in data_list]
    TUNE_RATIO = dict(TUNE_DICT)
    # Calculate 1
    
    for TUNE_CHOICE in TUNE_DICT:
        
        new_int = 0
        for pitch in pitch_list:
            if pitch in TUNE_DICT[TUNE_CHOICE][0]:
                new_int += 1
        if pitch_list[len(pitch_list)-1] in TUNE_DICT[TUNE_CHOICE][1]:
            print(TUNE_CHOICE, "BINGO")
            new_int += 30
        TUNE_RATIO[TUNE_CHOICE] = new_int/len(pitch_list)
    TUNE_RATIO = dict((k, v) for k, v in TUNE_RATIO.items() if v >= 0.7)
    if len(TUNE_RATIO) != 0:
        ACC_TUNE = max(TUNE_RATIO.items(), key=operator.itemgetter(1))[0]
        print(ACC_TUNE)
    
        if ACC_TUNE in TONE_CHANGE_DICT:
            for i in range(len(pitch_list)):
                if pitch_list[i] in TONE_CHANGE_DICT[ACC_TUNE][0]:
                    ind = TONE_CHANGE_DICT[ACC_TUNE][0].index(pitch_list[i])
                    jsobj[index][i][2] = TONE_CHANGE_DICT[ACC_TUNE][1][ind]
                    print("ori: ", pitch_list[i]," -> " , jsobj[index][i][2])
    # os._exit()

with open("adjust1.json", 'w') as outfile:
    json.dump(jsobj, outfile)   
    
        

    
    


        
    
        
        
