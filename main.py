from DubinsPark import DubinsPark

if __name__ == '__main__':
    bo = DubinsPark(13.167, .05)
    for i in range(25):
        bo.generate()
        bo.display(i)
        bo.send_to_txt(i)
