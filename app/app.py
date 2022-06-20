import PySimpleGUI as sg
import os

sg.theme('SystemDefaultForReal')


def convert_bytes(size):
    """ Convert bytes to KB, or MB or GB"""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0


treedata = sg.TreeData()
tree_element = sg.Tree(data=treedata,
                       headings=['Ext', 'Size'],
                       expand_x=True,
                       auto_size_columns=True,
                       show_expanded=True)

layout = [
    [sg.Text('Select a folder'), sg.InputText(), sg.FolderBrowse(key='-FOLDER-BROWSE-')],
    [tree_element],
    [sg.Button('Go'), sg.Exit()]
]

window = sg.Window('Data Catalog Version 1.0', layout)

while True:
    event, values = window.read()
    if event in ('Exit', sg.WIN_CLOSED):
        break
    elif event == 'Go':
        folder_path = values['-FOLDER-BROWSE-']
        for root, dirs, files in os.walk(folder_path):
            treedata.insert('', root, root, [])
            for file in files:
                treedata.insert(root, file, file, [
                    os.path.splitext(file)[1],
                    convert_bytes(os.path.getsize(os.path.join(root, file)))
                ])
        tree_element.update(values=treedata)
window.close()
