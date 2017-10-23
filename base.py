import os
import xml.etree.ElementTree


class Base:

    debug = True
    conf_file_name = ''
    cur_dir = ''

    def __init__(self):
        self.debug = True
        self.cur_dir = os.path.dirname(os.path.realpath(__file__)) + '/'
        self.conf_file_name = self.cur_dir + "config.xml"

    def set_param_to_xml(self, tag_name, new_val):
        et = xml.etree.ElementTree.parse(self.conf_file_name)
        for child_of_root in et.getroot():
            if child_of_root.tag == tag_name:
                child_of_root.text = new_val
                et.write(self.conf_file_name)
                return True
        return False

    def get_param_from_xml(self, param):
        """
        Get configuration parameters from the config.xml
        :param param: parameter name
        :return: if not exists, return None
        """
        root = xml.etree.ElementTree.parse(self.conf_file_name).getroot()
        tmp = None
        for child_of_root in root:
            if child_of_root.tag == param:
                tmp = child_of_root.text
                if not self.debug and child_of_root.get('type') == 'file':
                    tmp = self.cur_dir + tmp
                break

        return tmp

if __name__ == '__main__':
    inst = Base()
    print(inst)

