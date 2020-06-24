import sys
import json
import time

import numpy as np


if __name__ == '__main__':
    tStart = time.time()

    start, end = int(sys.argv[1]), int(sys.argv[2])
    ans_dict = {}
    for song_id in range(start, end+1):
        json_path = "%d/%d_feature.json" % (song_id, song_id)
        jsobj = json.load(open(json_path))
        tim = jsobj['time']
        vocal_pitch = jsobj['vocal_pitch']
        vocal, vocal_start, t = [], [], []
        cnt_zero = 0
        song_start = 0
        for i, x in enumerate(vocal_pitch):
            if x == 0:
                cnt_zero += 1
                continue
            elif i > 0 and i+1 < len(vocal_pitch) and abs(vocal_pitch[i-1]-x) >= 1 and abs(vocal_pitch[i+1]-x) >= 1:
                continue
            vocal.append(x)
            t.append(tim[i])
            if song_start == 0:
                vocal_start.append(1)
                cnt_zero = 0
                song_start = 1
            elif vocal_pitch[i-1] == 0:
                if cnt_zero <= 2:
                    vocal_start.append(0)
                else:
                    vocal_start.append(1)
                cnt_zero = 0
            else:
                vocal_start.append(0)

        vocal = np.array(vocal)
        vocal_start = np.array(vocal_start)
        record_NT = np.full((len(vocal), 600, 2), 1e9)

        for i, _ in enumerate(vocal):
            for j in range(min(600, i+1)):
                if vocal_start[i] == 1:
                    if i == 0 and j == 0:
                        record_NT[i, j, 0] = 0
                        record_NT[i, j, 1] = 0
                    elif j == 0:
                        continue
                    else:
                        record_NT[i, j, 0] = record_NT[i-1, j-1, 0]
                        record_NT[i, j, 1] = i
                else:
                    same_note = record_NT[int(record_NT[i-1, j, 1]), j, 0] + np.sum(np.abs(vocal[int(record_NT[i-1, j, 1]):i+1]-np.median(vocal[int(record_NT[i-1, j, 1]):i+1]))) if record_NT[i-1, j, 1] < 1e8 else 1e9
                    change_note = 1e9
                    if j > 0 and record_NT[i-1, j-1, 1] + 5 < i:
                        change_note = record_NT[i-1, j-1, 0]
                    if change_note < same_note:
                        record_NT[i, j, 0] = change_note
                        record_NT[i, j, 1] = i
                    else:
                        record_NT[i, j, 0] = same_note
                        record_NT[i, j, 1] = record_NT[i-1, j, 1]
        
        min_note = np.sum(vocal_start)-1
        min_err, min_err_pos = 1e9, 0
        for i in range(min_note, 600):
            if min_err > record_NT[len(vocal)-1, i, 0]:
                min_err = record_NT[len(vocal)-1, i, 0]
                min_err_pos = i
        select_pos = min_err_pos
        for i in range(min_note, min_err_pos):
            if min_err*1.25 > record_NT[len(vocal)-1, i, 0]:
                select_pos = i
                break
        res = []
        cur_idx = len(vocal)
        while select_pos >= 0:
            nxt_idx = int(record_NT[cur_idx-1, select_pos, 1])
            cur_note = np.around(np.median(vocal[nxt_idx:cur_idx]))
            # print(nxt_idx, cur_idx, cur_note)
            res.append([t[nxt_idx], t[cur_idx-1], cur_note])
            cur_idx = nxt_idx
            select_pos -= 1

        ans_dict[str(song_id)] = res[::-1]
        print(song_id)

    with open(sys.argv[3], 'w') as outfile:
        json.dump(ans_dict, outfile)
    tEnd = time.time()
    print ("It cost %f sec" % (tEnd - tStart))
    # print ("Data No:", the_dir)

