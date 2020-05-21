def tree2list(node, step=0, ret=[]):
    if len(node['children']) > 0:
        # Recursion Implementation, Safe when children is less than max recursion limit
        for child in node['children']:
            tree2list(child, step=step+1, ret=ret)

    node['depth'] = step
    node.pop('children')
    ret.append(node)
    return ret
