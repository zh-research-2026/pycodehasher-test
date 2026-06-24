#!/usr/bin/python3

from hashlib import md5
import csv, sys, os

global __app, __author, __updated__, __current_revision__

__app__              = 'PyCodeHasher'
__author__           = 'Zubair Hossain'
__last_updated__     = '12/23/2024'
__current_revision__ = '1.0.0'

'''
    [x] Hash each function in a code section using sha256 & md5 & make sure the following rules are followed:

    [x] Classes & function parsing

            [x] Hash whole section based on previously computed hashes
                [x] Make final hash of class computed based on hashes computed
                        from individual function hashes
                    + Benefits of this approach as opposed to hashing whole code
                         base is that it is more reliable & faster

    [x] Save hashes as a database entries which can be used to manually verify section, 
            & identify whether sections has changed, more specifically which functions
             & what has been added or removed

    Future addons:

	[x] Change order of things:

            	[x] discard empty lines 
            	[x] discard docstrings
            	[x] discard comments

    [x] argument parsing functions with
          [x] + generate [output_hash.txt] [file1, file2, ..]
          [x] + verify [hash.txt] [file1, file2, ..]

    [ ] Implement conversion routines from csv for 

                [x] 3,   regular functions
                [x] 1,2  class & class functions
                [ ] file hash
                [ ] summary

    [ ] Inform if class functions are not found

    [ ] summary() function that will provide stats on class & functions present in a file

    [ ] Additional capabilities for function & classes

          1) Whitelist of built-in standard library functions
          2) Blacklist common data type operations so it doesn't mess with (1)
          3) Keep track of function calls not belonging to 1 & 2
          4) Information on input / output parameters

'''

'''
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃             Code Index              ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

      Help Text                        71
      Printing functions              121
      Core Functions                  302
      Utility Functions               579

'''


'''
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃   Help Text                                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
'''

def print_header():

    global __app__, __current_revision__

    txt_color = '\x1B[1;38;5;87m' 

    lines = '    ' + '\u2501' * 71

    print()
    print(lines)

    header = \
    """
                             %s%s %s%s%s
    """ % (txt_color, text_highlight(__app__), \
            txt_color, text_highlight(__current_revision__), color_reset())

    print(text_highlight(header))

    print(lines)


def print_help():

    print_header()

    txt_color = ''

    field_number_color = color_b('cyan')
    field_data_color   = color_b('green')

    print(
    '''

            %sgenerate %s[file] [hash.txt]%s

                Generates hashes of python code


            %sverify %s[file] [hash.txt]%s

                Reports on detected changes

    '''  % (color_b('orange'), color_b('green'), color_reset(), \
            color_b('orange'), color_b('green'), color_reset()))


'''
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃   Printing Functions                                               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
'''

def clear_screen():

    """
    Clears screen, command is compatible with different OS
    """
    # print('\033[2J')
    os.system('clear')


def bold():
    return "\x1B[1m"


def color_reset():
    """
    Reset bg & fg colors
    """
    return "\x1B[0m"


def text_highlight(text=''):
    return bold() + text + color_reset()


def color_b(c=''):

    """
    Bold colors
    """

    if (c == 'white'):
        return '\x1B[1;38;5;15m'
    elif (c == 'blue'):
        return '\x1B[1;38;5;27m' 
    elif (c == 'cyan'):
        return '\x1B[1;38;5;51m'
    elif (c == 'yellow'):
        return '\x1B[1;38;5;221m'
    elif (c == 'orange'):
        return '\x1B[1;38;5;214m'
    elif (c == 'red'):
        return '\x1B[1;38;5;196m'
    elif (c == 'green'):
        return '\x1B[1;38;5;118m'
    elif (c == 'black'):
        return '\x1B[1;38;5;232m'
    else:
        return ""


def text_error(text=''):
    text = '\n%s %s%s%s' % (color_symbol_error(), \
                               '\x1B[1;38;5;253m', \
                            text, color_reset())
    return text


def text_debug(text=''):
    text = '\n%s %s%s%s' % (color_symbol_debug(), \
                               '\x1B[1;38;5;253m', \
                            text, color_reset())
    return text


def text_info(text=''):

    text = '\n%s %s%s%s' % (color_symbol_info(), \
                               '\x1B[1;38;5;253m', \
                            text, color_reset())
    return text


def color_symbol_error():

    text = '%s-%s' % ('\x1B[1;38;5;198m', color_reset())

    text = '  %s[%s%s]%s' % ('\x1B[1;38;5;160m', \
                               text, \
                             '\x1B[1;38;5;160m', \
                               color_reset())
    return text


def color_symbol_debug():

    text = '%s+%s' % ('\x1B[1;38;5;45m', color_reset())

    text = '  %s[%s%s]%s' % ('\x1B[1;38;5;36m', \
                               text, \
                             '\x1B[1;38;5;36m', \
                               color_reset())
    return text


def color_symbol_info():

    text = '%s*%s' % ('\x1B[1;38;5;214m', color_reset())

    text = '  %s[%s%s]%s' % ('\x1B[1;38;5;11m', \
                               text, \
                             '\x1B[1;38;5;11m', \
                               color_reset())
    return text


def color_symbol_question():
    text = '  ' + '\x1B[1;38;5;214m' + '[?]' + color_reset()
    return text


def color_symbol_prompt():
    text = '  ' + color_b('cyan') + '[>]' + color_reset()
    return text


def color_theme_1():

    s = '\x1B[1;38;5;15m\x1B[1;48;5;25m'
    return s


"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃   Core Functions                                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

class FunctionObj(object):

    def __init__(self, src_l=[]):

        self.__src_l = src_l
        self.__name = ''

        ## We do not process code that are not functions
        try:
            tmp = src_l[0].strip().split('def')[1]
            self.__name = tmp[:tmp.index('(')].strip()
        except ValueError:
            print(text_error('Unable to process the code below:') + '\n')
            print('\n'.join(src_l) + '\n')
            raise InvalidParameterException('FunctionObj(): it is not a valid function')

        self.__hash_src = md5(bytes(''.join(self.__src_l), 'utf-8')).hexdigest()
        self.__loc  = len(src_l)

        '''
        TODO:
            1) Whitelist of built-in standard library functions
            2) Blacklist common data type operations so it doesn't mess with (1)
            3) Keep track of function calls not belonging to 1 & 2
            4) Information on input / output parameters
        '''

    def print_stats(self):
        print('%s(): ' % self.__name)
        print('    Hash:       %s' % self.__hash_src)
        print('    # of lines: %d' % self.__loc)


    def get_name(self):
        return self.__name


    def get_hash(self):
        return self.__hash_src


    def get_size(self):
        return self.__loc


    def get_src(self):
        return self.__src_l

    def compare(self, hash_str=''):

        if (self.__hash_src == hash_str):
            return True
        else:
            return False


class ClassObj(object):

    ## TODO: Upgrade with class functions detection  
    def __init__(self, src_l=[]):

        self.__src_l = src_l
        self.__hash_src = md5(bytes(''.join(self.__src_l), 'utf-8')).hexdigest()

        tmp = src_l[0].strip().split('class')[1]
        self.__name = tmp[:tmp.index('(')].strip()
        self.__hash_fn_l = {} # {fn name : hash}

        self.__function_count = 0
        self.__fn_obj_l = []

        index = 1
        end_index = 0
        fn_obj = None

        while (index < len(src_l)):

            #print('index = %d' % index)

            if (src_l[index].lstrip().startswith('def')):
                self.__function_count += 1
                fn_obj, end_index = self.parse_function(src_l, index)
                #print('end_index = %d' % end_index)
                index = end_index

                if (fn_obj != None):
                    self.__fn_obj_l.append(fn_obj)
                else:
                    print(text_error('Unable to process the code below:') + '\n')
                    print('\n'.join(src_l) + '\n')
            else:
                index += 1

        self.__loc  = len(src_l)


    def parse_function(self, str_l=[], start_index=0):
    
        end_index = start_index+1
    
        while (end_index < len(str_l) and str_l[end_index].startswith('        ')): 
            end_index += 1
    
        #print(str_l[start_index:end_index])
    
        try:
            fn_obj = FunctionObj(str_l[start_index:end_index])
            self.__hash_fn_l.update({fn_obj.get_name() : fn_obj.get_hash()})

        except InvalidParameterException:
            return None, end_index
        #fn_obj.print_stats()
    
        return fn_obj, end_index 

    def print_stats(self):
        print('class name')
        print('%s(): ' % self.__name)
        print('    Hash (src):          %s' % self.__hash_src)
        print('    Lines of code (src): %d' % self.__loc)
        print('    Number of functions: %d\n' % len(self.__fn_obj_l))

        for fn in self.__fn_obj_l:
            print('    %s(): ' % fn.get_name())
            print('         Hash:          %s' % fn.get_hash())
            print('         Lines of code: %d' % fn.get_size())
            

    def print_fn(self):
        for fn in self.__fn_obj_l:
            print('%s : %s' % (fn.get_name(), fn.get_hash()))

    def get_name(self):
        return self.__name


    def get_hash(self):
        return self.__hash_src


    def get_hash_fn(self):
        return self.__hash_fn_l


    def get_fn_l(self):
        return self.__fn_obj_l


    def get_size(self):
        return self.__loc


    def get_src(self):
        return self.__src_l


def compare_class_with_raw_data(class_1=None, raw_data=[]):

    ##raw_data = [] # [class_name, hash, loc, [[fn,hash,loc], ..]]

    if (type(class_1) != ClassObj):
        raise TypeError('compare_class(): input parameter 1 needs to be of type ClassObj')

    failed_data_l      = []
    expected_data_l    = []

    hash_fn_l = class_1.get_hash_fn()

    #print(len(hash_fn_l))
    #print(hash_fn_l)
    #sys.exit()

    failed_fn_l = []

    hash_mismatch = False
    
    #print('raw_data[3]: ', raw_data[3])
    #sys.exit()
    ##raw_data[3] = [] # [[fn,hash,loc], ..]]

    for data in raw_data[3]:
        ## item_hash = class hash function list
        item_hash = hash_fn_l.get(data[0])  

        #print('class fn_(%s) hash: %s' % (data[0], item_hash))
        #print('raw data (%s) hash: %s' % (data[0], data[1]))
        #sys.exit()

        if (item_hash == None or item_hash != data[1]):
            hash_mismatch = True
            ## [function name, data hash, src hash]
            failed_fn_l.append([data[0],data[1],item_hash])

    if (hash_mismatch):
        ## failed_data_l = [class_name, [function name, data hash, src hash]]
        failed_data_l = [raw_data[0], failed_fn_l]
        return (False, failed_data_l)
    else:
        return (True, [])


def parse_file(fp=''):

    data = ''

    try:
        with open(fp, 'r') as fh:
            data = fh.read()
    except FileNotFoundError:
        raise FileNotFoundError('parse_file(): unable to locate file %s' % fp)

    data = data.split('\n')

    index_to_remove_l = []

    r = 0
    s = 0

    while (r < len(data)):

        if (data[r].strip() == ''):
            index_to_remove_l.append(r)
        elif (data[r].lstrip().startswith('#')):
            index_to_remove_l.append(r)
        elif (data[r].lstrip().startswith("'''")):

            s = r+1
            #print("l = %d" % l)

            while (s < len(data)):
                if (data[s].lstrip().startswith("'''") or \
                    data[s].rstrip().endswith("'''")):
                    break
                else:
                    s += 1
                    #print("l = %d" % l)


            #print('i = %d' % i)
            for index in range(r, s+1):
                index_to_remove_l.append(index)
            
            #print("index to remove (%d,%d)" % (i,l))

            r = s

        elif (data[r].lstrip().startswith('"""')):

            s = r+1
            #print("l = %d" % l)

            while (s < len(data)):
                if (data[s].lstrip().startswith('"""') or \
                    data[s].rstrip().endswith('"""')):
                    break
                else:
                    s += 1
                    #print("l = %d" % l)


            #print('i = %d' % i)
            for index in range(r, s+1):
                index_to_remove_l.append(index)
            
            #print("index to remove (%d,%d)" % (i,l))

            r = s

        r += 1

    remove_indexes_from_list_in_place(data, index_to_remove_l)

    #print(data)

    ## Parsing classes & functions
    index = 0
    end_index = 0
    index_to_remove_l = []

    fn_l   =  []
    class_l = []
    
    while (index < len(data)):

        #print('index = %d' % index)

        if (data[index].lstrip().startswith('class')):
            class_obj, end_index = parse_class(data, index)
            index_to_remove_l += [x for x in range(index, end_index)]
            index = end_index
            class_l.append(class_obj)
        elif (data[index].lstrip().startswith('def')):
            fn_obj, end_index = parse_function(data, index)
            index_to_remove_l += [x for x in range(index, end_index)]
            index = end_index

            if (fn_obj != None):
                fn_l.append(fn_obj)
        else:
            index += 1

    remove_indexes_from_list_in_place(data, index_to_remove_l)
    
    return class_l, fn_l


def parse_function(str_l=[], start_index=0, debug=False):

    end_index = start_index+1

    while (end_index < len(str_l) and str_l[end_index].startswith('    ')): 
        end_index += 1

    if (debug):
        print(str_l[start_index:end_index])

    try:
        fn_obj = FunctionObj(str_l[start_index:end_index])
    except InvalidParameterException:
        return None, end_index

    if (debug):
        fn_obj.print_stats()

    return fn_obj, end_index 


def parse_class(str_l=[], start_index=0, debug=False):

    end_index = start_index+1

    while (end_index < len(str_l) and str_l[end_index].startswith('    ')): 
        end_index += 1

    if (debug):
        print(str_l[start_index:end_index])

    class_obj = ClassObj(str_l[start_index:end_index])

    if (debug):
        class_obj.print_stats()

    return class_obj, end_index 


"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃   Utility Functions                                               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

def read_csv_from_str(data=''):

    """
    Parses a csv formatted string & loads all
        information into database

    Args:    (str)
    
    Returns: True if the operation succeeds
             False if the operation fails
    """

    if (len(data) == 0):
        return ''

    data_list = data.splitlines()

    record_list = csv.reader(data_list, quotechar='"', delimiter=',', \
            quoting=csv.QUOTE_ALL, skipinitialspace=True)

    tmp = []

    for item in record_list:
        tmp.append(item)

    tmp = remove_all_elements_from_list(tmp, ['\n'])

    return tmp


def write_csv(data=[], fp=''):

    if (len(data) == 0 or fp == ''):
        raise InvalidParameterException('write_csv(): Input parameters ' + \
                'cannot be empty')

    try:

        with open(fp, 'w+') as fh:
            cw = csv.writer(fh, delimiter=',', \
                    quoting=csv.QUOTE_ALL, quotechar='"')

            for row in data:
                cw.writerow(row)

        return True

    except IOError:
        pass

    return False


def write_str_to_file(s='', fn=''):

    if (len(s) == 0 or fn == ''):
        return False

    try:

        with open(fn, 'w') as fh:
            fh.write(s)

    except (IOError, BaseException):
        return False

    return True


def remove_all_elements_from_list(l=[], element_l=[], \
        starts_with_l=[], ends_with_l=[]):

    _l = l

    for item in element_l:
        _l = [x for x in _l if x != item]

    for item in starts_with_l:
        _l = [x for x in _l if x.startswith(item) != True]

    for item in ends_with_l:
        _l = [x for x in _l if x.endswith(item) != True]

    return _l


def remove_indexes_from_list_in_place(data_l=[], index_l=[]):

    num_items_removed = 0

    for i in range(len(index_l)):

        index = index_l[i] - num_items_removed
        num_items_removed += 1

        try:
            data_l.pop(index)

        except IndexError:
            pass

    return data_l


def generate_code_hash(input_file='', output_file=''):

    class_l = []
    fn_l    = []

    fn = os.path.basename(input_file)

    class_l, fn_l = parse_file(input_file)

    csv_str = ''

    if (len(class_l) != 0):
        for item in class_l:
            csv_str = csv_str + '1,%s,%s,%s,%s\n' % (item.get_name(), fn, item.get_hash(), str(item.get_size()))
            item_fn_l = item.get_fn_l()

            for obj in item_fn_l:
                csv_str = csv_str + '2,%s,%s,%s,%s\n' % (item.get_name(), obj.get_name(), obj.get_hash(), str(obj.get_size()))

    if (len(fn_l) != 0):
        for item in fn_l:
            csv_str = csv_str + '3,%s,%s,%s,%s\n' % (item.get_name(), fn, item.get_hash(), str(item.get_size()))

    if (output_file == ''):
        print(csv_str)
    else:
        write_str_to_file(csv_str, output_file)


    sys.exit()


def verify_code_hash(input_file='', hash_file=''):

    data = ''

    with open(hash_file, 'r') as fh:
        data = fh.read()

    data_l = read_csv_from_str(data)

    #print(data_l)
    #sys.exit()

    received_class_l = [] # [class_name, hash, loc, [[fn,hash,loc], ..]]
    received_fn_l    = [] # [name, hash, loc]

    ## Loading hashes from csv file

    csv_data_error_l = []

    i = 0

    while (i < len(data_l)):

        #print(i)
        #print(data_l[i][0], data_l[i][1], data_l[i][2],data_l[i][3])

        if (data_l[i][0] == '3' ):

            if (len(data_l[i]) != 5):
                csv_data_error_l.append(data_l[i])
                continue

            try:
                received_fn_l.append([data_l[i][1], data_l[i][3], int(data_l[i][4])])
            except ValueError:
                pass

        elif (data[i][0] == '1'): 
            ## Processing both 1 & 2, as usually they are one after the other

            j = i+1

            class_fn_l = []

            ## 1,Record,database_pwmgr.py,4d9886e964ddabdc85b3f30d20657dfb,160
            ## 2,Record,__init__,d84a7e53176e838b267018e85f0bdfb7,29
            ## 2,Record,__test,asdkaj53176e838b267018e85f0bdfb7,29

            while (j < len(data_l) and data_l[j][0] == '2'):

                if (len(data_l[j]) != 5):
                    csv_data_error_l.append(data_l[i])
                    j += 1
                    continue

                if (data_l[j][1] == data_l[i][1]):
                    class_fn_l.append([data_l[j][2],data_l[j][3],data_l[j][4]])
                    j+= 1
                else:
                    break

            received_class_l.append([data_l[i][1], data_l[i][3], data_l[i][4], class_fn_l])
            #print([data_l[i][1], data_l[i][3], data_l[i][4], class_fn_l]) 

            i = j-1

        else:
            csv_data_error_l.append(data_l[i])

        i += 1

    ## Generating hashes out of code file 
    generated_class_l = []
    generated_fn_l    = []

    fn = os.path.basename(input_file)

    generated_class_l, generated_fn_l = parse_file(input_file)

    #for item in generated_class_l:
    #    item.print_stats()

    class_checksum_error_l = []
    class_added_src_l      = []
    class_not_found_src_l  = []
    fn_checksum_error_l    = []
    fn_not_found_l         = []

    ##received_class_l = [] # [class_name, hash, loc, [[fn,hash,loc], ..]]
    ##received_fn_l    = [] # [name, hash, loc]

    ## Classes which are found in src, but not in db
    for class_obj in generated_class_l:

        found = False
        name = class_obj.get_name()

        for class_l in received_class_l:
            if (class_l[0] == name):
                found = True
                break

        if (not found):
            class_added_src_l.append([name, class_obj.get_hash()])
        

    ##received_class_l = [] # [class_name, hash, loc, [[fn,hash,loc], ..]]
    for class_l in received_class_l:

        ##print('testing class: ', class_l)
        class_found = False

        for class_obj in generated_class_l:

            if (class_l[0] == class_obj.get_name()):
                class_found = True
                #class_obj.print_fn()
                ## compare_class..() = [class_name, expected hash, received hash [[function name, data hash, src hash]]
                #print(class_obj.print_fn())
                #print(class_l)

                output = compare_class_with_raw_data(class_obj, class_l)
                #print('compare_class_with_raw_data(): ', output)
                #sys.exit()

                if (output[0] == False):
                    class_checksum_error_l.append(output[1])
                else:
                    break

        if (not class_found):
            class_not_found_src_l.append(class_l[0])

    if (len(class_checksum_error_l) == 0 and len(class_not_found_src_l) == 0 and len(class_added_src_l) == 0):
        print(text_debug('No errors found in class objects'))
    else:

        if (len(class_checksum_error_l) != 0):
            print(text_error('The following classes have hash mismatch: \n'))
            for item in class_checksum_error_l:
                print('%s\t  Class %s:\n' % (color_b('orange'), item[0]))
                for fn in item[1]:
                    print('\t      %s%s:  %s%s%s' % (color_b('yellow'), fn[0], color_b('red'), fn[1], color_reset()))
                    print('\t             %s%s%s\n' % (color_b('green'), fn[2], color_reset()))

        if (len(class_not_found_src_l) != 0):
            print(text_error('The following classes are missing: \n'))
            print('\t  %s%s%s\n' % (color_b('yellow'), ' '.join(class_not_found_src_l), color_reset()))

        if (len(class_added_src_l) != 0):
            print(text_error('The following classes are not listed in database: \n'))
            print('\t  %s%s%s\n' % (color_b('yellow'), ' '.join([x[0] for x in class_added_src_l]), color_reset()))

    #print('generated_fn_l: ')
    #for item in generated_fn_l:
    #    item.print_stats()
    #    print('\n')

    if (len(received_fn_l) == 0):

        if (len(generate_code_hash) == 0):
            print(text_debug('No functions detected'))
        ##TODO show functions that are found here but not in database

    else:

        fn_failed_l    = []
        fn_not_found_l = []
        fn_new_added_l = []

        for fn in generated_fn_l:

            name = fn.get_name()

            found = False

            for item in received_fn_l:

                if (item[0] == name):
                    found = True
                    break

            if (found == False):
                fn_new_added_l.append((name, fn.get_hash(), fn.get_size()))

        ## received_fn_l    = [] # [name, hash, loc]
        for fn in received_fn_l:

            output = search_fn_name(generated_fn_l, fn[0])

            if (output[0]):
                #print('generated_fn_l: %s\n' % generated_fn_l[output[1]].get_hash())

                if (not generated_fn_l[output[1]].compare(fn[1])):
                    #print('appending fn %s to fn_not_found_l' % fn[0])
                    fn_failed_l.append(fn)
            else:
                fn_not_found_l.append(fn)

        #print('fn_failed_l (len)   : %d' % len(fn_failed_l))
        #print('fn_not_found_l (len): %d' % len(fn_not_found_l))
        #print('fn_new_added (len)  : %d' % len(fn_new_added_l)) 

        if (len(fn_failed_l) == 0 and len(fn_not_found_l) == 0 and len(fn_new_added_l) == 0):
            print(text_debug('No changes detected in functions'))

        else:

            if (len(fn_failed_l) != 0): 
                print(text_error('The following functions have been modified: \n'))
                for fn in fn_failed_l:
                    print('\t  %s%s:  %s%s%s' % (color_b('yellow'), fn[0], color_b('red'), fn[1], color_reset()))
                print()

            if (len(fn_not_found_l) != 0): 
                print(text_error('The following functions have not been found in source code: \n'))
                print('\t  %s%s%s' % (color_b('yellow'), ' '.join([x[0] for x in fn_not_found_l]), color_reset()))
                print()

            if (len(fn_new_added_l) != 0): 
                print(text_error('The following functions are not listed in database: \n'))
                for fn in fn_new_added_l:
                    print('\t  %s%s:  %s%s%s' % (color_b('yellow'), fn[0], color_b('red'), fn[1], color_reset()))


def search_fn_name(fn_l=[], fn=''):

    for i in range(len(fn_l)):

        if (fn_l[i].get_name() == fn):
            return (True, i)

    return (False, -1)


def save_data(class_l=[], fn_l=[], fp=''):
    csv_str = ''

    if (len(class_l) != 0):
        for item in class_l:
            csv_str = csv_str + '1,%s,%s,%s,%s\n' % (item.get_name(), fn, item.get_hash(), str(item.get_size()))
            item_fn_l = item.get_fn_l()

            for obj in item_fn_l:
                csv_str = csv_str + '2,%s,%s,%s,%s\n' % (item.get_name(), obj.get_name(), obj.get_hash(), str(obj.get_size()))

    if (len(fn_l) != 0):
        for item in fn_l:
            csv_str = csv_str + '3,%s,%s,%s,%s\n' % (item.get_name(), fn, item.get_hash(), str(item.get_size()))

    write_str_to_file(csv_str, fp)


def parse_args():

    """
    Parses commandline arguments & executes the desired functions
    """

    arg_len = len(sys.argv)

    if (arg_len == 4 or arg_len == 3):

        if (sys.argv[1] == 'generate'):

            if (arg_len == 4):

                fn = sys.argv[2]

                if (not os.path.isfile(fn)):
                    print(text_error('Code file not found'))
                    sys.exit(1)
                elif(fn[-3:] != '.py' ):
                    print(text_error('It is not a valid python file (.py)'))
                    sys.exit(1)
                generate_code_hash(sys.argv[2], sys.argv[3])

            else:
                generate_code_hash(sys.argv[2])

        elif (sys.argv[1] == 'verify' and arg_len == 4):

            fn = sys.argv[2]

            if (not os.path.isfile(fn)):
                print(text_error('Code file not found'))
                sys.exit(1)
            elif(fn[-3:] != '.py'):
                print(text_error('It is not a valid python file (.py)'))
                sys.exit(1)
            elif (not os.path.isfile(sys.argv[3])):
                print(text_error('Hash file not found'))
                sys.exit(1)

            verify_code_hash(sys.argv[2], sys.argv[3])
            sys.exit(0)
    
    print_help()
    sys.exit(0)


def main():
    ## Test compare_class_with_raw_data() 
    #class_l, fn_l = parse_file('test3.py')
    ##raw_data = [] # [class_name, hash, loc, [[fn,hash,loc], ..]]
    #data = ['CustomClass','f6ca3bb7c6de11c63673960c6bbb768d',8, \
    #        [['CustomClass','__init__','0a383e6c3fe5801cd37ed881f5d2c3b9',2], \
    #        ['CustomClass','test1','31420cb99ebff0bda361ef3a21e10f24',5]]]
    ##for item in class_l:
    ##    print(item.print_stats())
    ##print(data)
    #sys.exit()
    #output = compare_class_with_raw_data(class_l[0], data)
    ##print(output)
    #sys.exit()

    parse_args()
    sys.exit()

class InvalidParameterException(Exception):
    def __init__(self, msg="The input parameter is not valid"):
        super().__init__(msg)

if __name__ == '__main__':
    main()

