import re

def search_quantity_tablet(text):
    
    regex = r"([№Nn]\s+\d+\s+)|([nN№]\d+\s+?[-]\s?\d)|([nN№]\d+)|([№Nn]\s+\d+)"
    regex_num = r"\d+"

    raw_matches = re.search(regex, text)
    try:
        raw_result = raw_matches.group(0)
        if "-" in raw_result:
            num_matches = re.findall(regex_num, raw_result)
            return(int(num_matches[0]) * int(num_matches[1]))
        else:    
            num_matches = re.search(regex_num, raw_result)
            try:
                return (int(num_matches.group(0)))
            except AttributeError:
                return ('no_data')
    except AttributeError:
        return('no_data')


print(search_quantity_tablet('необутин таб 100мг № 10'))