import csv,re,sys,urllib.request as u
def g(s,p):return re.sub(p,'\\1',u.urlopen(u.urljoin('https://www.fedramp.gov',s)).read().decode(),flags=24)
csv.writer(sys.stdout).writerows([['topic','score','clue','response']]+[[x[0],y[0],y[1],y[2]]for x in re.findall(r'{name:["\'](.+?)["\'],description:"(.+?)",clues:\[(.+?)\]}',g(g('/trivia/',r'^.+<link href="(([^"]+)/104\.([^"]+))" rel="modulepreload">.+$'),r'^.+,qe=(.+?),Ee.+$'),24)for y in re.findall(r'{value:(\d{3,4}),clue:["\'](.+?)["\'],response:["\'](.+?)["\']}',x[2],24)])
