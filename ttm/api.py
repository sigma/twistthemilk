# API spec

API = {
   'auth': {
       'checkToken':
           [('auth_token',), 
            ()],
       'getFrob':
           [(), 
            ()],
       'getToken':
           [('frob',), 
            ()]
       },
    'contacts': {
        'add':
            [('timeline', 'contact'), 
             ()],
        'delete':
            [('timeline', 'contact_id'), 
             ()],
        'getList':
            [(), 
             ()]
        },
    'groups': {
        'add':
            [('timeline', 'group'), 
             ()],
        'addContact':
            [('timeline', 'group_id', 'contact_id'), 
             ()],
        'delete':
            [('timeline', 'group_id'), 
             ()],
        'getList':
            [(), 
             ()],
        'removeContact':
            [('timeline', 'group_id', 'contact_id'), 
             ()],
        },
    'lists': {
        'add':
            [('timeline', 'name'), 
             ('filter',)],
        'archive':
            [('timeline', 'list_id'), 
             ()],
        'delete':
            [('timeline', 'list_id'), 
             ()],
        'getList':
            [(),
             ()],
        'setDefaultList':
            [('timeline',),
             ('list_id',)],
        'setName':
            [('timeline', 'list_id', 'name'),
             ()],
        'unarchive':
            [('timeline',),
             ('list_id',)],
        },
    'locations': {
        'getList':
            [(),
             ()]
        },
    'reflection': {
        'getMethodInfo':
            [('methodName',),
             ()],
        'getMethods':
            [(),
             ()]
        },
    'settings': {
        'getList':
            [(),
             ()]
        },
    'tasks': {
        'add':
            [('timeline', 'name',),
             ('list_id', 'parse',)],
        'addTags':
            [('timeline', 'list_id', 'taskseries_id', 'task_id', 'tags'),
             ()],
        'complete':
            [('timeline', 'list_id', 'taskseries_id', 'task_id',),
             ()],
        'delete':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ()],
        'getList':
            [(),
             ('list_id', 'filter', 'last_sync')],
        'movePriority':
            [('timeline', 'list_id', 'taskseries_id', 'task_id', 'direction'),
             ()],
        'moveTo':
            [('timeline', 'from_list_id', 'to_list_id', 'taskseries_id', 'task_id'),
             ()],
        'postpone':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ()],
        'removeTags':
            [('timeline', 'list_id', 'taskseries_id', 'task_id', 'tags'),
             ()],
        'setDueDate':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('due', 'has_due_time', 'parse')],
        'setEstimate':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('estimate',)],
        'setLocation':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('location_id',)],
        'setName':
            [('timeline', 'list_id', 'taskseries_id', 'task_id', 'name'),
             ()],
        'setPriority':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('priority',)],
        'setRecurrence':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('repeat',)],
        'setTags':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('tags',)],
        'setURL':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ('url',)],
        'uncomplete':
            [('timeline', 'list_id', 'taskseries_id', 'task_id'),
             ()],
        'notes': {
            'add':
                [('timeline', 'list_id', 'taskseries_id', 'task_id', 'note_title', 'note_text'),
                 ()],
            'delete':
                [('timeline', 'note_id'),
                 ()],
            'edit':
                [('timeline', 'note_id', 'note_title', 'note_text'),
                 ()]
            },
        },
    'test': {
        'echo':
            [(),
             ()],
        'login':
            [(),
             ()]
        },
    'time': {
        'convert':
            [('to_timezone',),
             ('from_timezone', 'time')],
        'parse':
            [('text',),
             ('timezone', 'dateformat')]
        },
    'timelines': {
        'create':
            [(),
             ()]
        },
    'timezones': {
        'getList':
            [(),
             ()]
        },
    'transactions': {
        'undo':
            [('timeline', 'transaction_id'),
             ()]
        },
    }
