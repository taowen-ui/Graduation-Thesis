import re
import os
import os.path
import json
import glob


class read_lawfile:
    def __init__(self, chapter_mode=r"第[零一二三四五六七八九十百千万]+章 +.+\b", part_mode=r"第[零一二三四五六七八九十百千万]+节 +.+\b", entry_mode=r"第[零一二三四五六七八九十百千万]+条 \b", num_mode=r"\n[零一二三四五六七八九十百千万]+、"):
        # 识别章、节、条
        self.chapter_mode = chapter_mode
        self.part_mode = part_mode
        self.entry_mode = entry_mode
        self.num_mode = num_mode

    def read_file(self, file_path):
        # 读取文件
        self.law = {}
        f = open(file_path, encoding='utf-8')
        content = f.read()
        content = content.replace("\n\n", "\n")      #把双换行改成单换行？
        content = content.replace("#", "")           #去掉#号                得到了content
        # print(content)
        chapter_p = re.search(self.chapter_mode, content)             #匹配章节位置
        if chapter_p is None:                             #找不到章节
            entry_p = re.search(self.entry_mode, content)
            if entry_p is not None:
                return self.read_entrys(content)
            else:
                return self.read_nums(content)
        while chapter_p is not None:                    #匹配到章节
            c_start = chapter_p.start()
            c_end = chapter_p.end()
            key = content[c_start:c_end]            #key为章节内容
            # print(key)
            content = content[c_end:]          #删去此章节
            
            chapter_p = re.search(self.chapter_mode, content)
            if chapter_p is not None:
                end = chapter_p.start()
                c_content = content[:end]
                self.law[key] = self.read_parts(c_content)
            # print(content[c_start:c_end])
            else:
                self.law[key] = self.read_parts(content)
        f.close()
        return self.law
    
    def read_parts(self, content):               #读一节
        parts = {}
        part_p = re.search(self.part_mode, content)
        if part_p is None:
            return self.read_entrys(content)
        while part_p is not None:
            r_start = part_p.start()
            r_end = part_p.end()
            key = content[r_start:r_end]
            content = content[r_end+1:]
        
            part_p = re.search(self.part_mode, content)
            if part_p is not None:
                end = part_p.start()
                r_content = content[:end]
                parts[key] = self.read_entrys(r_content)
            else:
                parts[key] = self.read_entrys(content)
        return parts

    def read_entrys(self, content):
        entrys = {}
        entry_p = re.search(self.entry_mode, content)
        while entry_p is not None:
            e_start = entry_p.start()
            e_end = entry_p.end()
            key = content[e_start:e_end]
            content = content[e_end:]
        
            entry_p = re.search(self.entry_mode, content)
            if entry_p is not None:
                end = entry_p.start()
                e_content = content[:end]
                entrys[key] = e_content
            else:
                entrys[key] = content
        return entrys
    
    def read_nums(self, content):
        nums = {}
        num_p = re.search(self.num_mode, content)
        while num_p is not None:
            n_start = num_p.start()
            n_end = num_p.end()
            key = content[n_start:n_end]
            content = content[n_end:]
        
            num_p = re.search(self.num_mode, content)
            if num_p is not None:
                end = num_p.start()
                n_content = content[:end]
                nums[key[1:]] = n_content
            else:
                nums[key[1:]] = content
        return nums
    # entry_p = re.search(entry_mode, content)
    # while entry_p is not None:
    #     start = entry_p.start()
    #     end = entry_p.end()
    #     # print(content[start:end])
    #     content = content[end:]
    #     law[content[start:end]] = read_entrys(content)
    #     chapter_p = re.search(chapter_mode, content)

    def show(self):
        for key in self.law:
            print(key, '\n')
            for item in self.law[key]:
                print(item, ' ', self.law[key][item])


def main():
    # file_path = "D:/11496/Documents/project/Laws-master/刑法/刑法.md"
    # r = read_lawfile()
    # dict = r.read_file(file_path)
    # # r.show()
    # # print(dict)
    # with open('./a.json', 'w') as f:
    #     # json.dumps(dict, f, ensure_ascii=False)
    #     json.dump(dict, f, ensure_ascii=False)

    path = r'D:/11496/Documents/project/Laws-master/**'
    file_list = glob.glob(path, recursive=True)
    files = []
    print(len(file_list))
    # print(type(file_list))
    for file in file_list:
        if ("README" in file) or ("index" in file) or (".md" not in file) or ("\\案例\\" in file) or ("\\其他\\" in file):
            continue
        else:
            files.append(file)

    for file in files:
        json_path = file.replace("D:/11496/Documents/project/Laws-master", "D:/11496/Documents/project/Laws-master/json")
        json_path = json_path.replace(".md", ".json")    #改文件名称
        r = read_lawfile()
        dict = r.read_file(file)     #dict就是self.law，字典
        path = os.path.dirname(json_path)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(json_path, 'w', encoding='utf-8') as f:
            # json.dumps(dict, f, ensure_ascii=False)
            json.dump(dict, f, ensure_ascii=False)         #改格式jason


if __name__ == '__main__':
    main()
