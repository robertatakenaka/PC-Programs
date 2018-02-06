# coding=utf-8


def normalize_number(number):
    if number is not None:
        if number.strip().isdigit():
            return str(int(number))
    return number


def get_number_suppl_compl(issue_element_content):
    number = None
    suppl = None
    compl = None
    if issue_element_content is not None:
        parts = issue_element_content.strip().lower().split(' ')
        if len(parts) == 1:
            # suppl or n
            if parts[0].startswith('sup'):
                suppl = parts[0]
            else:
                number = parts[0]
        elif len(parts) == 2:
            #n suppl or suppl s or n pr
            if parts[0].startswith('sup'):
                suppl = parts[1]
            elif parts[1].startswith('sup'):
                number, suppl = parts
            else:
                number, compl = parts
        elif len(parts) == 3:
            # n suppl s
            number, ign, suppl = parts
    if suppl is not None:
        if suppl.startswith('sup'):
            suppl = '0'
    return (number, suppl, compl)


def format_issue_label(year, volume, number, volume_suppl, number_suppl, compl):
    year = year if number == 'ahead' else ''
    v = 'v' + volume if volume is not None else None
    vs = 's' + volume_suppl if volume_suppl is not None else None
    n = 'n' + number if number is not None else None
    ns = 's' + number_suppl if number_suppl is not None else None
    return ''.join([i for i in [year, v, vs, n, ns, compl] if i is not None])


def display_pages(fpage, lpage):
    if fpage is not None and lpage is not None:
        n = lpage
        if len(fpage) == len(lpage):
            i = 0
            n = ''
            for i in range(0, len(fpage)):
                if fpage[i:i+1] != lpage[i:i+1]:
                    n = lpage[i:]
                    break
                i += 1
        lpage = n if n != '' else None
    r = []
    if fpage is not None:
        r.append(fpage)
    if lpage is not None:
        r.append(lpage)
    return '-'.join(r)
