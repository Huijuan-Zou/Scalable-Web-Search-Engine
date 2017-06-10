#!/usr/bin/env python3
from argparse import ArgumentParser
import xml.etree.ElementTree as ET
import os

def remove_namespace(text, namespace):
    namespace = u'{%s}' % namespace
    length = len(namespace)
    for elem in text.getiterator():
        if elem.tag.startswith(namespace):
            elem.tag = elem.tag[length:]

def main():
    parser = ArgumentParser(description = "Starting the Coordinator...")
    parser.add_argument("filename")
    parser.add_argument("--job_path", dest = "job_path")
    parser.add_argument("--num_partitions", dest = "num_partitions")
    args = parser.parse_args()
    context = ET.iterparse(args.filename)
    files = []
    leng = len([name for name in os.listdir(args.job_path) if name.endswith('.in')])
    print(leng)
    for i in range(int (leng)):
        file_name = args.job_path + str(i) + ".in"
        print(file_name)
        if os.path.isfile(file_name):
            os.remove(file_name)
    newroot_list = []
    for i in range(int (args.num_partitions)):
        file_name = args.job_path + str(i) + ".in"
        filea = open(file_name, 'ab')
        files.append(filea)
        newroot_list.append(ET.Element('mediawiki'))
    index = 0
    for events, elem in context:
        remove_namespace(elem, u'http://www.mediawiki.org/xml/export-0.10/')
        if elem.tag == 'siteinfo':
            for i in range(int (args.num_partitions)):
                newroot_list[i].append(elem)
        if elem.tag == 'page':
            newroot_list[index % int (args.num_partitions)].append(elem)
        index += 1
    for i in range(int(args.num_partitions)):
        stra = ET.tostring(newroot_list[i],encoding='utf8', method='xml')
        files[i].write(str.encode(stra.decode()))
        files[i].flush()
        files[i].close()
        
if __name__ == "__main__":
    main()
