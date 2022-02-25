with open("FBres") as f:
    raw = f.read()

res = raw.split("\\' \\'")

lst = []

for i, r in enumerate(res):

    if i == 0 or i == len(res) - 1:
        r = r.replace("\\'", "")

    if i % 2 == 0:

        dic = {}

        if r != "_separator_":

            resx, resy, aspect = r.split()
            resx, resy, aspect = int(resx), int(resy), float(aspect)

            dic["resx"] = resx
            dic["resy"] = resy
            dic["aspect"] = aspect

        else:
            dic["resx"] = None
            dic["resy"] = None
            dic["aspect"] = None

    else:

        if r != "---------":
            dic["name"] = r
            dic["isSeparator"] = False

        else:
            dic["name"] = None
            dic["isSeparator"] = True

        lst.append(dic)
