from DubinsPark import DubinsPark

if __name__ == '__main__':
    bo = DubinsPark(13.716, .05)
    max_x = 40.0
    min_x = -40.0
    max_y = 40.0
    min_y = -40.0
    L2 = 10.192
    for i in range(100):
        track_vector = bo.generate()
        while (max(track_vector[:, 0]) >= max_x - L2 or 
                min(track_vector[:, 0]) <= min_x + L2 or 
                max(track_vector[:, 1]) >= max_y - L2 or 
                min(track_vector[:, 1]) <= min_y + L2):
            print('regenerating..')
            track_vector = bo.generate()	
        #bo.display(i)
        bo.send_to_txt(i)
