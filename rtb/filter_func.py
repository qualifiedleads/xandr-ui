import decimal,re, itertools,ast,operator

all_accepted_operators={
    #"AND":operator.mul,
    #"OR":operator.add,
    "=":operator.eq,
    "<>": operator.ne,
    ">":operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "contains": operator.contains, #lambda a, b: b in a,
    "notcontains": lambda a, b: b not in a,
    "startswith": lambda a, b: a.startswith(b),
    "endswith": lambda a, b: a.endswith(b),
}
def clause_evaluator(clause):
    oper=all_accepted_operators[clause[1]]
    field_name = clause[0].strip()
    const = clause[2].strip()
    if const[:1]=="\"":
        if const[-1]!="\"": raise ValueError("Quotes must be paired!")
        const = const[1:-1].decode("string_escape")
    def calc(obj):
        left = obj.get(field_name,None)
        if left is None: return False
        left_type = type(left)
        try:
            right = left_type(const)
        except:
            left = repr(left)
            right = repr(const)
        if isinstance(left, (float, decimal.Decimal)):
            left = round(left,4)
            right = round(right, 4)
        if isinstance(left, (str, unicode)):
            left = left.strip()
        try:
            r = oper(left,right)
            return r
        except:
            return False
    return calc

def func_evaluator(s, func_list):
    #node = ast.parse(s.strip(), mode='eval')
    s=s.strip().replace(',',' ').replace('"','').replace('[','(').replace(']',')')
    node = compile(s, filename='<unknown>', mode='eval')
    variable_names = ['a%d'%num for num in xrange(1,len(func_list)+1)]
    def calc(obj):
        local_vars = {name:f(obj) for name,f in itertools.izip(variable_names, func_list)}
        try:
            c=eval(node, local_vars)
            return c
        except Exception as e:
            print e
            return False
    return calc

def get_filter_function(filter_clause):
    cnt = [0]

    def replace_func(m):
        cnt[0] += 1
        return ' a%d ' % cnt[0]

    clause = re.compile(r'\s*\[\s*"([^"]*)",\s*"([^"]*)",\s*(\w+|(?:"(?:[^"]|\\\S)*"))\s*\]')
    find_result = re.findall(clause, filter_clause)
    clause_list = map(clause_evaluator, find_result)
    compile_string = re.sub(clause, replace_func, filter_clause)
    if clause_list:
        filter_function = func_evaluator(compile_string, clause_list)
    else:
        # simple clause
        clause = re.compile(r"^(.*?)(>|<|=|<>|>=|<=|\bcontains\b|\bnotcontains\b|\bstartswith\b|\bendswith\b)(.*)$")
        m = re.match(clause, filter_clause)
        filter_function = clause_evaluator(m.groups()) if m else None
    return filter_function
