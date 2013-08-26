
def grep(target, string_list, options=''):
    '''
    target : a string
    string_list : a list of strings
    options : in 'vinq'.  Same meanings as grep
        v : invert
        i : ignore case
        n : line numbers
        q : quiet (return tf)
    
    >>> string_list = 'AA bb cc ab ac xy'.split()
    >>> string_list = ['AA', 'bb', 'cc', 'ab', 'ac', 'xy']
    >>> grep('a', string_list)
    ['ab', 'ac']
    >>> grep('a', string_list, 'i')
    ['AA', 'ab', 'ac']
    >>> grep('a', string_list, 'iv')
    ['bb', 'cc', 'xy']
    >>> grep('a', string_list, 'v')
    ['AA', 'bb', 'cc', 'xy']
    >>> grep('b', string_list, 'n')
    [(1, 'bb'), (3, 'ab')]
    >>> grep('foo', string_list, 'q')
    False
    '''
    f = lambda s: target in s
    v = lambda tf: tf
    i = lambda s: s
    if 'v' in options:
        v = lambda tf: not tf
    if 'i' in options:
        target = target.lower()
        i = lambda s: s.lower()
    fn = lambda s: v(f(i(s)))
    if 'q' in options:
        return any(s for s in string_list if fn(s))
    if 'n' in options:
        return [(n,s) for (n,s) in enumerate(string_list) if fn(s)]
    return [s for s in string_list if fn(s)]



def object_multigrep(target_list, ob_list, transform, options=''):
    '''
    '''
    def any_target_in(ob): 
        return any(grep(t,transform(ob),options) for t in target_list)
    return [ob for ob in ob_list if any_target_in(ob) ]


def multigrep_func(transform, andor='or'):
    f = {'or':any, 'and':all}[andor]
    def object_multigrep(target_list, ob_list, options=''):
        def any_target_in(ob): 
            return f(grep(t,transform(ob),options) for t in target_list)
        return [ob for ob in ob_list if any_target_in(ob) ]
    return object_multigrep


multi_grep_and = multigrep_func(lambda s:[s], 'and')
multi_grep = multigrep_func(lambda s:[s])
multi_grep.__doc__ = '''
>>> string_list = ['AA', 'bb', 'cc', 'ab', 'ba'] 
>>> target_list = ['a', 'b'] 
>>> multi_grep(target_list , string_list, 'i')
['AA', 'bb', 'ab', 'ba']
>>> multi_grep_and(target_list , string_list, 'i')
['ab', 'ba']
'''



fredob_multi_grep = multigrep_func(lambda pair:[pair[0]])
fredob_multi_grep.__doc__ = '''
>>> city_list = fredob_multi_grep(target_list, hpi_info)
>>> denver_id = city_list[-1][1]
>>> denver_obs = fred_observations(denver_id)
>>> denver_obs = fredobs2table(denver_obs)
'''







target_list = 'Denver Yakima Seattle Tucson Detroit'.split()
target_list = 'New Denver Detroit Dallas Phoenix Vegas Diego Seattle Kansas'.split()

def fredobs2table(fredobs):
    f = lambda dct: (dct['date'], dct['value'])
    return [f(dct) for dct in fredobs]



def fn(n):
    i = 0
    while i<n:
        yield i
        i+=1



from fred import Fred


def titles(ob_list):
    return [ob_list[i]['title'] for i in range(len(ob_list))]
     
def fred_search(target):
    return Fred().series('search', search_text=target)['seriess']['series']


def fred_search(**k):
    return Fred().series('search', **k)['seriess']['series']



def fred_search(**k):
    off = 0
    step = 1000
    result = []
    f = Fred().series
    s = lambda off: f('search', offset=off, limit=step,  **k)
    while True:
        try:
            result += s(off)['seriess']['series']
            off += step
        except KeyError:
            return result


def fred_observations(sid):
    return Fred().api('series', 'observations', series_id=sid)['observations']['observation']


def fred_release(**k):
    return Fred().release('series', **k)['seriess']['series']



def big():
    # Example from the source code.  How one finds the correct id is
    # mysterious.
    r51 = fred_release(release_id=51, limit=21)
    r51_titles = titles(r51)

    # First 1000 results with House Price Index #
    target = 'House Price Index'
    shouse = fred_search(search_text=target)
    dct = shouse[44]
    den = grep('Denver', grep(target, titles(shouse)))

    f = lambda dct: (dct['title'][39:], 
    #    dct['seasonal_adjustment_short'], 
    #    dct['frequency_short'], 
        dct['id'])

    g = lambda target, dct: target in dct['title'] 

    hpi_info = [f(dct) for dct in shouse if g(target, dct)]

    h = lambda target_list, tup: any(target in tup[0] for target in target_list)
    hpi_red = [t for t in hpi_info if h(target_list, t)]


    boo = fred_observations('NVSTHPI')
    boo = fred_observations('ATNHPIUS49420Q')
    obn = boo[4]


    f = lambda dct: (dct['date'], float(dct['value'])) 
    f = lambda dct: (dct['date'], dct['value']) 

    parsed = [f(dct) for dct in boo]


    foo = [(name,code) for (name,code) in hpi_info if grep('MSAD', [name])]
    bar = [(name,code) for (name,code) in hpi_info if multi_grep(target_list, [name])]
    oops = multi_grep(['MSAD'], hpi_info) # good result accidentally.
    globals().update(locals())


