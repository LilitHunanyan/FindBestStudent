#! /usr/bin/env python

"""The purpose of this module is parse and print the best student information"""

import os
import sys
import argparse


def parse_args():
    """Parsing command line arguments"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-input', dest='input', required=True,
                        help="entry files directory")
    args = parser.parse_args()
    return args


def get_average(line):
    """Calculate and return the average point of subjects"""
    points = [int(item.split(':')[1].strip()) for item in line.split(',')]
    return sum(points)/len(points)


def parse_student_file(input_dir):
    """Parse information about students"""
    student_dict = {} # or dict()
    for file_name in os.listdir(input_dir):
        file_path = f'{input_dir}/{file_name}'
        if not os.path.isfile(file_path):
            continue
        with open(file_path) as file_:
            lines = file_.readlines()
        student_dict[file_name] = {}
        for line in lines:
            if '-' not in line:
                continue
            key, value = line.split('-')
            if key.strip().lower() == 'point':
                student_dict[file_name]['point'] = get_average(value.strip())
            else:
                student_dict[file_name][key.strip()] = value.strip()
    return student_dict


def get_best_students(student_dict):
    """Detect the best students and print information"""
    for item in sorted(student_dict.items(), key=lambda x: x[1]['points'],
                       reverse=True)[:3]:
        print(f"Student {item[0]}")
        for key, value in item[1].items():
            print(f'{key} -> {value}')
        print('-'*20)


def main(args):
    """The main function"""
    status = 0
    if not os.path.exists(args.input):
        print(f"No such directory {args.input}")
        return 1
    student_dict = parse_student_file(args.input)
    if student_dict:
        get_best_students(student_dict)
    else:
        print("Not found any valid file to parse")
        status += 1
    return status


if __name__ == '__main__':
    ARGS = parse_args()
    sys.exit(main(ARGS))
