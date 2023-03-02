import os
import sys

def listdir_nohidden(path):
    for entry in os.listdir(path):
        if not entry[0] == '.':
            yield entry

def str_size(nbyte):
    k = 0
    while nbyte >> (k + 10):
        k += 10
    units = ("B", "KB", "MB", "GB")
    size_by_unit = round(nbyte / (1 << k), 2) if k else nbyte
    return str(size_by_unit) + units[k // 10]

class Tree():
    mode_descriptions = {
        'df': 'Directory First',
        'do': 'Directory Only',
        'ff': 'File First',
        'od': 'Ordered'
    }

    def __init__(self, path, indent=4, mode='ff', layer=0,
        sparse=True, dtail='/', show_hidden=False, show_size=False,
        show_absolute_path_of_rootdir=False):
        indent = min(max(indent, 1), 8)
        self.sparse = sparse
        self.dtail = dtail
        self.layer = layer if layer > 0 else 65535
        self.indent_space = ' ' * indent
        self.down_space = '│' + ' ' * (indent - 1)
        self.vert_horiz = '├' + '─' * (indent - 1)
        self.turn_horiz = '└' + '─' * (indent - 1)

        self.traverses = {
            'df': self.df,
            'do': self.do,
            'ff': self.ff,
            'od': self.od
        }
        self.listdir = os.listdir if show_hidden else listdir_nohidden
        self.show_size = show_size
        self.show_absolute_path_of_rootdir = show_absolute_path_of_rootdir

        self.chmod(mode)
        self.generate(path)

    def write(self, filename):
        with open(filename, 'w+', encoding='utf-8') as fd:
            # ![](../../../../../Screen Shot 2022-11-28 at 8.46.31 PM.png)
            fd.write('mode: %s\n' % self.mode)
            fd.write('\n')
            fd.write(self.tree)

    def print(self):
        print(self.tree)

    def chmod(self, mode):
        assert mode in self.traverses
        self.traverse = self.traverses[mode]
        self.mode = self.mode_descriptions[mode]

    def generate(self, path):
        """
        metadata: [(path, isfile?, size) or None], maybe use to open file
        size: file size, or number of files in a Directory, is a string
        """
        assert os.path.isdir(path)
        self.metadata = []
        self.lines = [path]
        if not self.show_absolute_path_of_rootdir:
            self.lines[0] = os.path.basename(path)
        self.traverse(path, '', 0)

        if self.lines[-1] == '':
            self.lines.pop()
            self.metadata.pop()

        if self.show_size:
            sep = self.indent_space
            size_len = max(len(md[2]) for md in self.metadata if md)
            for i, mdata in enumerate(self.metadata):
                size = mdata[2] if mdata else ' '
                size = '%*s' % (size_len, size)
                if self.lines[i]:
                    self.lines[i] = size + sep + self.lines[i]

        self.tree = '\n'.join(self.lines) + '\n'

    def get_dirs_files(self, dirpath):
        dirs, files = [], []
        for leaf in self.listdir(dirpath):
            path = os.path.join(dirpath, leaf)
            if os.path.isfile(path):
                files.append((leaf, path))
            else:
                dirs.append((leaf, path))
        self.metadata.append((dirpath, False, str(len(dirs) + len(files))))

        return dirs, files

    def add_dirs(self, dirs, prefix, recursive, layer):
        fprefix = prefix + self.down_space
        dprefix = prefix + self.vert_horiz
        for dirname, path in dirs[:-1]:
            self.lines.append(dprefix + dirname + self.dtail)
            recursive(path, fprefix, layer + 1)

        fprefix = prefix + self.indent_space
        dprefix = prefix + self.turn_horiz
        dirname, path = dirs[-1]
        self.lines.append(dprefix + dirname + self.dtail)
        recursive(path, fprefix, layer + 1)

    def add_files(self, files, fprefix):
        for filename, path in files:
            size = str_size(os.path.getsize(path))
            self.lines.append(fprefix + filename)
            self.metadata.append((path, True, size))
        if self.sparse and files:
            self.lines.append(fprefix.rstrip())
            self.metadata.append(None)

    def df(self, dirpath, prefix, layer):
        dirs, files = self.get_dirs_files(dirpath)
        if layer < self.layer:
            if dirs:
                self.add_dirs(dirs, prefix, self.df, layer)
            self.add_files(files, prefix + self.indent_space)

    def do(self, dirpath, prefix, layer):
        dirs, files = self.get_dirs_files(dirpath)
        if layer < self.layer and dirs:
            self.add_dirs(dirs, prefix, self.do, layer)

    def ff(self, dirpath, prefix, layer):
        dirs, files = self.get_dirs_files(dirpath)
        if layer < self.layer:
            if dirs:
                self.add_files(files, prefix + self.down_space)
                self.add_dirs(dirs, prefix, self.ff, layer)
            else:
                self.add_files(files, prefix + self.indent_space)

    def od(self, dirpath, prefix, layer):
        def add_leaf(leaf):
            path = os.path.join(dirpath, leaf)
            if os.path.isfile(path):
                size = str_size(os.path.getsize(path))
                self.lines.append(dprefix + leaf)
                self.metadata.append((path, True, size))
            if os.path.isdir(path):
                self.lines.append(dprefix + leaf + self.dtail)
                self.od(path, fprefix, layer + 1)

        leaves = list(self.listdir(dirpath))
        self.metadata.append((dirpath, False, str(len(leaves))))

        if layer < self.layer and leaves:
            leaves.sort()

            fprefix = prefix + self.down_space
            dprefix = prefix + self.vert_horiz
            for leaf in leaves[:-1]:
                add_leaf(leaf)

            fprefix = prefix + self.indent_space
            dprefix = prefix + self.turn_horiz
            add_leaf(leaves[-1])

#self, dirs, prefix, recursive, layer
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

def main():
    """
    mapper
    """
    for line in sys.stdin:
        data = line.strip().split(" ")
        if len(data) == 5:
            student_id = data[0]
            os_name = data[2]
            key = student_id + '_' + os_name
            print"\t".join([key,"file1"])
        elif len(data) == 4:
            student_id = data[0]
            os_name = data[-1]
            key = student_id + '_' + os_name
            print"\t".join([key,"file2"])
#if __name__ == "__main__":
#    main()
main()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import json

dic_result = {}
pre_key = ""
def post_deal(pre_key):
    # print pre_key
    # 相同key的数据的处理
    global dic
    os_name = pre_key.strip().split("_")[1]
    # print dic
    # if 'click' in dic and dic['click'] == 'yes' :#and 'active' in dict and dic['active'] == 'yes':
    if 'click' in dic and dic['click'] == 'yes' and 'active' in dic and dic['active'] == 'yes':

        # if os_name not in dic_result:
        #     dic_result[os_name] =0
        dic_result[os_name] += 1
def deal(data):
    if data[1].strip() == "file1":
        dic['click'] = 'yes'
    if data[1].strip() == "file2":
        dic['active'] = 'yes'
def pre_deal():
    global dic
    dic = dict()
def main():
    # reducer
    # data_list = ['20170001_android    file1','20170002_ios    file1','20170001_android    file1','20170001_android    file1', '20170001_android   file2','20170001_android    file2',
    #              '20170002_ios    file1','20170002_ios    file2','20170003_android    file1', '20170003_android   file1']
    # for line in data_list:
    for line in sys.stdin:
        data = line.strip().split("\t")
        # print data

        key = data[0]
        global pre_key
        if key != pre_key:
            if pre_key != "":
                post_deal(pre_key)
            pre_deal()
            pre_key = key

        deal(data)

        if pre_key != "":
            post_deal(pre_key)

    print(json.dumps(dic_result))


#if __name__ == "__main__":
#    main()
main()