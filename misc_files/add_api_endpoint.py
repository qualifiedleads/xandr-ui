import re, ast, astor, itertools

main_re = re.compile(r"'(https://api.appnexus.com/[\w-]+)',\s*\{[^\}]*\},\s*(\w+)", re.MULTILINE)
# main_re = re.compile(r"'(https://api.appnexus.com/[\w-]+)'",re.MULTILINE)
file = ''
with open('cron.py')as f:
    file = f.read()

classes = re.findall(main_re, file)
class_names = {x[1]: x[0].split('/')[-1] for x in classes}

print class_names

with open('models.py')as f:
    file = f.read()
with open('models.py')as f:
    lines = f.readlines()

a = ast.parse(file)
ast_classes = [x for x in a.body if isinstance(x, ast.ClassDef) and x.name in class_names]
offset = 0
for i in ast_classes:
    print i.name
    txt = "    api_endpoint = '%s'\n" % class_names[i.name]
    meta_class = list(itertools.islice(itertools.ifilter(lambda x: isinstance(x, ast.ClassDef), i.body), 0, 1))
    if meta_class:
        line_num = min(itertools.imap(lambda x: x.__dict__.get('lineno', 1000000), ast.walk(meta_class[0])))
        print line_num
        line_num += offset - 1
        lines = lines[:line_num] + [txt] + lines[line_num:]
        offset += 1
    else:
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    print '-' * 79
# source = astor.to_source(a)

with open('models_copy.py', 'w')as f:
    f.writelines(lines)

c = {'Category': 'https://api.appnexus.com/category', 'DemographicArea': 'https://api.appnexus.com/dma',
     'AdQualityRule': 'https://api.appnexus.com/ad-quality-rule', 'Creative': 'https://api.appnexus.com/creative',
     'Member': 'https://api.appnexus.com/member', 'MobileAppInstance': 'https://api.appnexus.com/mobile-app-instance',
     'CteativeTemplate': 'https://api.appnexus.com/template',
     'PlatformMember': 'https://api.appnexus.com/platform-member', 'Profile': 'https://api.appnexus.com/profile',
     'PaymentRule': 'https://api.appnexus.com/payment-rule', 'Company': 'https://api.appnexus.com/brand-company',
     'OperatingSystemExtended': 'https://api.appnexus.com/operating-system-extended',
     'MediaSubType': 'https://api.appnexus.com/media-subtype', 'BuyerGroup': 'https://api.appnexus.com/buyer-group',
     'CreativeFolder': 'https://api.appnexus.com/creative-folder',
     'OptimizationZone': 'https://api.appnexus.com/optimization-zone',
     'Publisher': 'https://api.appnexus.com/publisher', 'AdProfile': 'https://api.appnexus.com/ad-profile',
     'Placement': 'https://api.appnexus.com/placement', 'Language': 'https://api.appnexus.com/language',
     'Country': 'https://api.appnexus.com/country', 'Region': 'https://api.appnexus.com/region',
     'InsertionOrder': 'https://api.appnexus.com/insertion-order', 'MediaType': 'https://api.appnexus.com/media-type',
     'LineItem': 'https://api.appnexus.com/line-item', 'ConversionPixel': 'https://api.appnexus.com/pixel',
     'CteativeFormat': 'https://api.appnexus.com/creative-format', 'Advertiser': 'https://api.appnexus.com/advertiser',
     'OSFamily': 'https://api.appnexus.com/operating-system-family', 'Campaign': 'https://api.appnexus.com/campaign',
     'Site': 'https://api.appnexus.com/site', 'Brand': 'https://api.appnexus.com/brand',
     'Developer': 'https://api.appnexus.com/developer'}
