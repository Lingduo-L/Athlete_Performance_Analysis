import os
import sublime
import sublime_plugin
from .tree import Tree


class SidebarMakeTreeCommand(sublime_plugin.WindowCommand):
    def get_tree_settings(self):
        settings = sublime.load_settings(
            'SublimeDirectoryTree.sublime-settings')
        tree_settings = settings.get('args', { "dir_tail_character": "/" })
        tree_settings['dtail'] = tree_settings.pop("dir_tail_character")
        return tree_settings

    def is_visible(self, paths):
        return len(paths) == 1 and os.path.isdir(paths[0])

    def run(self, paths):
        tree_settings = self.get_tree_settings()
        tree = Tree(paths[0], **tree_settings)
        text = "mode: %s\n\n" % tree.mode
        text += tree.tree

        view = self.window.new_file()
        view.assign_syntax("tree.sublime-syntax")
        view.set_name("%s.tr" % os.path.basename(paths[0]))
        view.settings().set("font_face", "Lucida Console")
        view.settings().set("word_wrap", False)
        view.run_command("append", {"characters": text})
        view.set_scratch(True)
        view.set_read_only(True)


class SidebarCopyTreeCommand(SidebarMakeTreeCommand):
    def run(self, paths):
        tree_settings = self.get_tree_settings()
        tree = Tree(paths[0], **tree_settings)

        sublime.set_clipboard(tree.tree)

SidebarMakeTreeCommand.get_tree_settings()
# [
# 	{"caption": "-", "id": "folder_menus"},
# 	{
# 		"caption": "Copy Directory Tree",
# 		"command": "sidebar_copy_tree",
# 		"args": {"paths": []}
# 	},
# 	{
# 		"caption": "View Directory Tree",
# 		"command": "sidebar_make_tree",
# 		"args": {"paths": []}
# 	},
# ]
