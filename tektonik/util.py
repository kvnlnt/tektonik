def remove_empty_values(obj):
    return dict((key, val) for (key, val) in obj.iteritems() if val != '')
