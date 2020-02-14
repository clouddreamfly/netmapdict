#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import Tkinter
import tkMessageBox



MAP_SIZE = 256
display_col_count = MAP_SIZE / 16

class NetMapDict:
    
    def generate(self):
        MapDatas = list(range(MAP_SIZE))
        random.shuffle(MapDatas)
        
        SendByteMap = list(range(MAP_SIZE))
        RecvByteMap = list(range(MAP_SIZE))
        
        for i in range(len(MapDatas)):
            SendByteMap[i] = MapDatas[i]
            index = SendByteMap[i]
            RecvByteMap[index] = i
            
        return SendByteMap, RecvByteMap
    
    def output(self, SendByteMap, RecvByteMap, display_col_count):
        
        SendByteMapTable = "g_SendByteMap[%d] = {\n"%(MAP_SIZE)
        for i in range(MAP_SIZE):
            col_index = i % display_col_count
            row_index = i // display_col_count
            if col_index == 0:
                SendByteMapTable += '\t'
            
            SendByteMapTable += "0x%02X"%(SendByteMap[row_index * display_col_count + col_index])
            
            if i != (MAP_SIZE - 1):
                if col_index != (display_col_count - 1):
                    SendByteMapTable += ', '
                else:
                    SendByteMapTable += ','
            if col_index == (display_col_count - 1) or i == (MAP_SIZE - 1):
                SendByteMapTable += "\n"
            
        SendByteMapTable += "};\n"
        
        
        RecvByteMapTable = "g_RecvByteMap[%d] = {\n"%(MAP_SIZE)
        for i in range(MAP_SIZE):
            col_index = i % display_col_count
            row_index = i // display_col_count
            if col_index == 0:
                RecvByteMapTable += '\t'
                
            RecvByteMapTable += "0x%02X"%(RecvByteMap[row_index * display_col_count + col_index])
            
            if i != (MAP_SIZE - 1):
                if col_index != (display_col_count - 1):
                    RecvByteMapTable += ', '
                else:
                    RecvByteMapTable += ','
            if col_index == (display_col_count - 1) or i == (MAP_SIZE - 1):
                RecvByteMapTable += "\n"
            
        RecvByteMapTable += "};\n"      
        
        return SendByteMapTable, RecvByteMapTable
        
    
    def test(self, SendByteMap, RecvByteMap):
        
        send_count = random.randint(0, MAP_SIZE)
        recv_count = send_count
        test_count = 2
        test_index = 0
        
        print("test: begin =====================================\n")
        while(test_count > 0):
            test_count -= 1
            test_index += 1
            send_datas = list(range(MAP_SIZE))
            random.shuffle(send_datas)
            
            encrypt_datas = []
            for data in send_datas:
                
                encrypt_data = SendByteMap[(data + send_count) % MAP_SIZE]
                encrypt_datas.append(encrypt_data)
                send_count = (send_count + 4) % MAP_SIZE
            
            recv_datas = []   
            for data in encrypt_datas:
                recv_data = (RecvByteMap[data] - recv_count) % MAP_SIZE
                recv_datas.append(recv_data)
                recv_count = (recv_count + 4) % MAP_SIZE  
             
            print("test: count=%d" % (test_index))
            for i in range(len(send_datas)):
                send_data = send_datas[i]
                recv_data = recv_datas[i]
                if (send_data == recv_data):
                    print i, "==>", send_data , "==>", recv_data
                else:
                    print "test: fail !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n"
                    return False
        
        
        print "test: end =====================================\n\n"
        return True
        
    

class MainDialog:
    
    def __init__(self):
        
        self.dialog = dialog = Tkinter.Tk()
        dialog.title("网络映射字典")
        dialog.geometry("640x480")
        #dialog.resizable(0,0)
        dialog.minsize(640, 480)
        
        paned = Tkinter.PanedWindow(dialog, orient=Tkinter.VERTICAL) 
        paned.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=Tkinter.YES)  
        
        frame = Tkinter.Frame(paned)  
        frame.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=Tkinter.YES)
        frame_sb_x = Tkinter.Scrollbar(frame, orient=Tkinter.HORIZONTAL)
        frame_sb_y = Tkinter.Scrollbar(frame, orient=Tkinter.VERTICAL)
        frame_sb_x.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)  
        frame_sb_y.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)  
        self.txt_content = txt_content = Tkinter.Text(frame, state=Tkinter.DISABLED, wrap=Tkinter.NONE)
        txt_content.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=Tkinter.YES)
        txt_content.configure(xscrollcommand = frame_sb_x.set)
        txt_content.configure(yscrollcommand = frame_sb_y.set)
        frame_sb_x.configure(command = txt_content.xview)  
        frame_sb_y.configure(command = txt_content.yview)   
    
        frame1 = Tkinter.Frame(paned)
        frame1.pack(side=Tkinter.BOTTOM)
        btn_generate = Tkinter.Button(frame1, text = "生成", width = 16, height = 2, command = self.OnBtnGenerate)
        btn_test = Tkinter.Button(frame1, text = "测试", width = 16, height = 2, command = self.OnBtnTest)
        btn_copy = Tkinter.Button(frame1, text = "复制", width = 16, height = 2, command = self.OnBtnCopy)
        btn_generate.pack(side=Tkinter.LEFT, padx = 10, pady = 10)
        btn_test.pack(side=Tkinter.LEFT, padx = 10, pady = 10)
        btn_copy.pack(side=Tkinter.LEFT, padx = 10, pady = 10)

        
        self.send_byte_map_data = None
        self.recv_byte_map_data = None
        
        
        
    def OnBtnGenerate(self):
        
        obj = NetMapDict()
        self.send_byte_map_data, self.recv_byte_map_data = obj.generate()
        send_byte_map_data_content, recv_byte_map_content = obj.output(self.send_byte_map_data, self.recv_byte_map_data, display_col_count)
        
        self.txt_content.configure(state = Tkinter.NORMAL)
        self.txt_content.delete(1.0, Tkinter.END)
        self.txt_content.insert(Tkinter.END, u"// 网络数据加密解密映射字典表\n\n")
        self.txt_content.insert(Tkinter.END, send_byte_map_data_content + "\n\n" + recv_byte_map_content)
        self.txt_content.configure(state = Tkinter.DISABLED)
    
    def OnBtnTest(self):
        
        if self.send_byte_map_data == None or self.recv_byte_map_data == None:
            tkMessageBox.showinfo(u"提示", u"请先生成数据，再进行测试")
            return
        
        result = NetMapDict().test(self.send_byte_map_data, self.recv_byte_map_data)
        if result == True:
            tkMessageBox.showinfo(u"提示", u"生成数据成功")
        else:
            tkMessageBox.showerror(u"错误", u"生成数据失败")
    
    def OnBtnCopy(self):
        
        self.dialog.clipboard_clear()
        self.dialog.clipboard_append(self.txt_content.get(1.0, Tkinter.END))
        
        
    def runloop(self):
        
        self.dialog.mainloop()


def main():
    
    dialog = MainDialog()
    dialog.runloop()

    
if __name__ == "__main__":
    main()

