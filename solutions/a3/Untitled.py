
# coding: utf-8

# In[ ]:


import re
import json


# In[ ]:


data = open("A3F2018_marking.txt").read()

pattern = r"\n*(\w+[ \d]*: \[\/\d+\])\n*"# r"(\w+( \d)*: \[\/\d*\])\n"
re.findall(pattern, data)


# In[276]:


def parse_contents(contents):
    contents = re.sub(r"(\n*)(\t+)\s*-\s*", "; ", contents)
    c = contents.split("\n") if contents else None
    
    if c:
        new_contents = []
        for part in c:
            spl = re.split(r"\s*\bmarks?\b\s*-\s*", part) # (?:\/)(\d+(?:\.\d+)?)  # (?:\/)(\d+(?:\.\d+)?)
            if len(spl) != 2:
                new_contents.append(dict(description=contents))
                continue

            mark = re.search(r"(?:\/)(\d+(?:\.\d+)?)", spl[0]).group()
            desc = spl[1]
            
            if mark: 
                mark = int(mark.replace("/",""))
                
            new_contents.append(dict(mark=mark, description=desc))
        
        return new_contents
    return contents

questions = {}

for r in re.split("\n\n", data):
    spl = [x for x in re.split(pattern, r) if x]
    if "Total: " in spl[0]:
        # questions[spl[0]] = ""
        continue
    
    name, components = spl
    
    total = int(re.search(r"(?:\/)(\d+(?:\.\d+)?)", name).group().replace("/", ""))
    name = name.strip().split(":")[0]
    
    questions[name] = dict(
        total=total,
        contents=parse_contents(components)    
    )

questions['Total'] = int(re.search(r"\d+", re.search(r"Total: \[\/(\d+)\]", data).group()).group())


# In[277]:


with open("marking.json", "w") as f:
    out = json.dumps(questions, indent=2)
    print(out)
    f.write(out)


# In[266]:


with open("marking.json", "r") as f:
    a = json.load(f)

[f"a{2}_p{i+1}.py" if "Problem" in p else p
 for i, p in enumerate(a.keys())]

