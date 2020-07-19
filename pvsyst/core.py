'''
@author: frederic rivollier

'''

import re, sys, os

import logging
logging.addLevelName(5,"VERBOSE")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('pvsyst')

#parse indented text and yield level, parent and value
def _parse_tree(lines):
    """
    Parse an indented outline into (level, name, parent) tuples.  Each level
    of indentation is 2 spaces.
    """
    regex = re.compile(r'^(?P<indent>(?: {2})*)(?P<name>\S.*)')
    stack = []
    for line in lines:
        match = regex.match(line)
        if not match:
            continue #skip last line or empty lines
            #raise ValueError('Indentation not a multiple of 2 spaces: "{0}"'.format(line))
        level = len(match.group('indent')) // 2
        if level > len(stack):
            raise ValueError('Indentation too deep: "{0}"'.format(line))
        stack[level:] = [match.group('name')]
        yield level, match.group('name'), (stack[level - 1] if level else None)

#for PVSYST files parsing to DICT. Takes list of group keys and return dict
def text_to_dict(m, sections):
    data = dict()
    levels_temp = [None]*10  # temporary array to store current keys tree

    # parse each line of m string (PAN file)
    for level, name, parent in _parse_tree(m.split('\n')):
        #try for line with no = sign i.e. End of we will continue
        try:
            key = re.split('=',name)[0]
            value = re.split('=',name)[1]
            logger.log(5, '{}{}:{} [l{},p{}]'.format(' ' * (2 * level), key, value, level, parent))
        except:
            continue

        # Create group keys for current level
        # check if key if in sections dict
        group = [v for k, v in sections.items() if key == k]
        if group:
            if level == 0:
                data[group[0]] = dict()
                levels_temp[0] = data[group[0]]
                logger.log(5, 'set levels_temp[0] to data[{}]'.format(name))

            else:
                levels_temp[level - 1][group[0]] = dict()
                levels_temp[level] = levels_temp[level - 1][group[0]]
                logger.log(5, 'set levels_temp[{}] to data[{}]'.format(level, group[0]))

        else:
            levels_temp[level-1][key] = value


    return data
