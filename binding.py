#!/user/bin/python
# vim: set fileencoding=utf-8
import clang.cindex
import asciitree
import sys

from mako.template import Template

def node_children(node):
    return (c for c in node.get_children() if c.location.file.name == sys.argv[1])

def print_node(node):
    text = node.spelling or node.displayname
    kind = str(node.kind)[str(node.kind).index('.')+1:]
    return '{} {}'.format(kind, text)


def get_annotations(node):
    return [c.displayname for c in node.get_children()
            if c.kind == clang.cindex.CursorKind.ANNOTATE_ATTR]


class MemberVariable(object):
    def __init__(self, cursor):
        self.name = cursor.spelling
        self.annotations = get_annotations(cursor)

class Function(object):
    def __init__(self, cursor):
        self.name = cursor.spelling
        self.annotations = get_annotations(cursor)

class Class(object):
    def __init__(self, cursor):
        self.name = cursor.spelling
        self.functions = []
        self.member_variables = []
        self.annotations = get_annotations(cursor)
        self.brief_comment = cursor.brief_comment

        for c in cursor.get_children():
            if (c.kind == clang.cindex.CursorKind.CXX_METHOD and
                c.access_specifier == clang.cindex.AccessSpecifier.PUBLIC):
                f = Function(c)
                self.functions.append(f)
            elif (c.kind == clang.cindex.CursorKind.FIELD_DECL) :
                v = MemberVariable(c)
                self.member_variables.append(v)
def build_classes(cursor):
    result = []
    for c in cursor.get_children():
        if (c.kind == clang.cindex.CursorKind.CLASS_DECL and c.location.file.name == sys.argv[1]):
            a_class = Class(c)
            result.append(a_class)
        elif c.kind == clang.cindex.CursorKind.NAMESPACE:
            child_classes = build_classes(c)
            result.extend(child_classes)

    return result

index = clang.cindex.Index.create()
translation_unit = index.parse(sys.argv[1], ['-x', 'c++', '-std=c++11', '-D__CODE_GENERATOR__'])
classes = build_classes(translation_unit.cursor)
tpl = Template(filename='bind.mako')
print(asciitree.draw_tree(translation_unit.cursor, node_children, print_node))
print tpl.render(classes=classes)
