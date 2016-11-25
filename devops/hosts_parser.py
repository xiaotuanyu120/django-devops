class HostsParser(object):
    def __init__(self):
        self.cleaned_hosts_list = []

    def clean_hosts(self, file):
        filter_result = []
        with open(file, 'r') as f:
            for line in f.readlines():
                if not line.strip().startswith('#'):
                    if line.strip():
                        filter_result.append(line)
        self.cleaned_hosts_list = filter_result
        return filter_result

    def hosts_parser(self):
        group_of_groups = {}
        sub_groups = {}
        for li in self.cleaned_hosts_list:
            li = li.strip()
            if li.startswith('[') and li.endswith(']'):
                if ':children' in li:
                    group_name = li[1:-10]
                    group_content = group_of_groups[group_name] = {}
                else:
                    group_name = li[1:-1]
                    group_content = sub_groups[group_name] = []
            else:
                try:
                    content = type(group_content)
                except NameError as e:
                    print "hosts syntax error!(%s)" % e
                    return

                if content is list:
                    group_content.append(li)
                elif content is dict:
                    group_content[li] = {}
                else:
                    print "content type error!(should be list or dict, not %s)" % content
                    return

        result = group_of_groups
        for gog in group_of_groups:
            for sub_group in group_of_groups[gog]:
                try:
                    group_of_groups[gog][sub_group] = sub_groups[sub_group]
                except KeyError as e:
                    print "group_of_group's content error, no sub_group %s exist" % sub_group
                    return
                del sub_groups[sub_group]
        if sub_groups:
            for single_group in sub_groups:
                result[single_group] = sub_groups[single_group]
        return result

    def parser(self, file):
        self.clean_hosts(file)
        return self.hosts_parser()
