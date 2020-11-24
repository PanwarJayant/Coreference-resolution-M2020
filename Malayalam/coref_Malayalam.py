def parseConvert(sentence):
    """
    Convert SSF to ISC parser format
    """
    tree = []
    count = 1
    for line in sentence:
        if len(line) > 1:
            if line[1] == "((":
                name = ""
                drel = ""
                for i in line:
                    if i.split("=")[0].lower() == "name":
                        name = i.split("=")[1].strip("'>").strip('">')
                    if i.split("=")[0].lower() == "drel":
                        drel = i.split("=")[1].strip("'>").strip('">')
            else:
                tree.append(
                    [count, line[1], line[1], line[2], line[2], "_", name, drel]
                )
                count = count + 1
    for node in tree:
        if node[-1] == "":
            node.insert(-2, 0)
            node.insert(-2, "main")
            continue
        rel = node[-1].split(":")[0]
        parent = node[-1].split(":")[1]
        parentNode = 0
        for i in range(len(tree)):
            if tree[i][-2] == parent:
                parentNode = i + 1
                break
        node.insert(-2, parentNode)
        node.insert(-2, rel)
    for node in tree:
        node.pop()
        node.pop()
    return tree


# Initializations
filepath = "./Data/test1.ssf"
data = open(filepath)

sentenceCount = -1
mention = []
allmention = []
headwd = []
pronCandidates = []
pron = []
pronRefers = []

print("┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┐")
print("| Coreference Resolution Program |")
print("└ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┘")

# MENTION-DETECTION STEP
print("\n------------MENTIONS FOUND-----------\n")
sentence = []
for line in data:
    if len(line.split()):
        if line.split()[0] == "<Sentence":
            sentence = []
            continue
    if line.strip() != "</Sentence>":
        sentence.append(line.split())
        continue
    tree = parseConvert(sentence)
    sentenceCount = sentenceCount + 1
    for node in tree:
        newmention = ""
        if (node[4] == "N_NN" or node[4] == "N_NNP" or node[4] == "N_NST") and (
            tree[int(node[6]) - 2][4] == "N_NST"
            or tree[int(node[6]) - 2][4] == "N_NNP"
            or tree[int(node[6]) - 2][4] == "N_NN"
        ):
            for x in range(int(node[0]) - 1, int(tree[int(node[6])][0]) - 1):
                newmention += tree[x][1].replace(")", "").replace("(", "") + " "
            if newmention != "":
                score = 0
                if tree[int(node[6]) - 1][7].find("k1") != -1:
                    score += 100
                elif tree[int(node[6]) - 1][7].find("k2") != -1:
                    score += 80
                elif tree[int(node[6]) - 1][7].find("k3") != -1:
                    score += 60
                elif tree[int(node[6]) - 1][7].find("k4") != -1:
                    score += 50
                elif tree[int(node[6]) - 1][7].find("k5") != -1:
                    score += 50
                elif tree[int(node[6]) - 1][7].find("k7") != -1:
                    score += 50
                sentment = sentenceCount
                pronCandidates.append([newmention, score, sentment])
                mention.append(newmention)
                allmention.append(newmention)
                headwd.append(
                    [tree[int(node[6]) - 1][1], newmention, tree[int(node[6]) - 1][4]]
                )
        elif node[4] == "N_NN" or node[4] == "N_NNP" or node[4] == "N_NST":
            b = False
            for m in mention:
                if node[1] == m:
                    b = True
                    break
            if (not b) and node[1] != "":
                mention.append(node[1])
            if node[1] != "":
                score = 0
                if node[7].find("k1") != -1:
                    score += 100
                elif node[7].find("k2") != -1:
                    score += 80
                elif node[7].find("k3") != -1:
                    score += 60
                elif node[7].find("k4") != -1:
                    score += 50
                elif node[7].find("k5") != -1:
                    score += 50
                elif node[7].find("k7") != -1:
                    score += 50
                sentment = sentenceCount
                pronCandidates.append([node[1], score, sentment])
                allmention.append(node[1])
                headwd.append([node[1], node[1], node[4]])
        if node[4].find("PR") == 0:
            pronment = sentenceCount
            pron.append([node[1], pronment])
            for x in range(0, pronment + 1):
                for y in pronCandidates:
                    if y[2] <= x:
                        diff = -y[2] + x
                        y[1] = (y[1]) * pow(0.9, diff)
            pronCandidates = sorted(pronCandidates, key=lambda sub: sub[1])
            pronCandidates.reverse()
            topPronCandidates = []
            for candidate in pronCandidates:
                if candidate[1] == pronCandidates[0][1]:
                    topPronCandidates.append(candidate[0])
            pronRefers.append([node[1], topPronCandidates])

for men in allmention:
    print(men)

# CLUSTERING-STEP
print("\n------------CLUSTERS FOUND-----------\n")

cluster = []
for m1 in mention:
    for m2 in mention:
        if m1 != m2 and m1 != "" and m2 != "":
            if m1.find(m2) != -1:
                clusterExists = False
                for i in cluster:
                    if m1 in i or m2 in i:
                        i.add(m1)
                        i.add(m2)
                        clusterExists = True
                        break
                if not clusterExists:
                    cluster.append(set({m1, m2}))
for i in cluster:
    print(i)


# EXACT-MATCH STEP
print("\n------------EXACT MATCHES FOUND-----------\n")

for i in allmention:
    # tree = parser.parse(i.split())
    # for node in tree:
    if i in mention:
        print(i, "and", i, "have exact match")


# RELAXED STRING MATCH STEP
print("\n------------RELAXED MATCHES FOUND-----------\n")

for men1 in mention:
    for men2 in mention:
        if men1 != men2 and men1 != "" and men2 != "":
            if men1.find(men2) != -1:
                print(men1, "and", men2, "have a match")

# PROPER-HEAD-WORD MATCH STEP
print("\n------------PROPER HEAD-WORD MATCHES FOUND-----------\n")

properHeadMatches = []

for i in headwd:
    for j in headwd:
        if i == j:
            continue

        if (
            i[0] == j[0]
            and ([i[1], j[1]] not in properHeadMatches)
            and ([j[1], i[1]] not in properHeadMatches)
            and (i[2] == "N_NNP")
        ):
            properHeadMatches.append([i[1], j[1]])

for i in properHeadMatches:
    print(i[0], "matches with", i[1])


# RELAXED HEAD-WORD MATCH STEP
print("\n------------RELAXED HEAD-WORD MATCHES FOUND-----------\n")

headMatches = []

for i in headwd:
    for j in headwd:
        if i == j:
            continue

        if (
            i[0] == j[0]
            and ([i[1], j[1]] not in headMatches)
            and ([j[1], i[1]] not in headMatches)
            and (i[2] != "N_NNP")
        ):
            headMatches.append([i[1], j[1]])

for i in headMatches:
    print(i[0], "matches with", i[1])


# PRONOUN MATCH STEP
print("\n------------PRONOUN MATCHES FOUND-----------\n")

for reference in pronRefers:
    if len(reference[1]) == 1:
        print("Pronoun", reference[0], "refers to", reference[1][0])
    else:
        print("Pronoun", reference[0], "can refer to", reference[1])


data.close()
