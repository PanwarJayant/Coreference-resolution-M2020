from __future__ import unicode_literals
from isc_parser import Parser
import re

parser = Parser(lang='hin')
text = '''
पढ़ाई के साथ खर्च भी:ITI की इंजीनियरिंग ट्रेड में एडमिशन लेने वाली लड़कियों को मिलेंगे 500 रुपये प्रतिमाह
सरकार ने औद्योगिक प्रशिक्षण संस्थान (ITI) में बेटी बचाओ-बेटी पढ़ाओ मुहिम के तहत नई योजना लागू की है।
शैक्षिक सत्र 2020-21 में सरकारी ITI की इंजीनियरिंग ट्रेड में एडमिशन लेने वाली लड़कियों को पांच सौ रुपये प्रतिमाह मिलेंगे।
जिले की सरकारी ITI में छठीं काउंसिलिंग से एडमिशन प्रोसेस जारी है। नए स्टूडेंट 28 नवंबर तक एडमिशन के लिए ऑनलाइन आवेदन कर सकते हैं।
बेटियों को कुशल और रोजगार प्रदान करने के लिए सरकार ने ITI में पढ़ने वाली लड़कियों के लिए प्रोत्साहन राशि जारी प्रदान करने का फैसला किया है।
सरकारी ITI के प्राचार्य डॉ. कृष्ण कुमार ने बताया कि शैक्षिक सत्र 2020-21 में सरकारी ITI की इंजीनियरिंग ट्रेड में पढ़ने वाली लड़कियों को पांच सौ रुपये प्रतिमाह प्रदान किए जाएंगे। वर्तमान में सभी ITI में प्रवेश प्रक्रिया जारी है।
नए स्टूडेंट भी प्रवेश के लिए आवेदन कर सकते हैं।
इसके साथ लड़कियों को पहले से ही काफी सुविधाएं प्रदान की जा रही है। ITI में लड़कियों की एडमिशन फीस 545 और लड़कों की 590 रुपये है। इसके अलावा सरकारी ITI में लड़कियों के लिए प्रतिमाह किसी तरह की फीस का प्रावधान नहीं है।
जबकि लड़कों की प्रतिमाह की ट्यूशन फीस 45 रुपये है। अब लड़कियों की निशुल्क पढ़ाई के लिए उन्हें पांच सौ रुपये प्रतिमाह प्रदान किए जाएंगे।
'''

origText = text
text = re.split("।|\n", text)
for t in range(len(text)):
    text[t] = text[t].replace(":", " : ").replace(",", " , ")

text = [i for i in text if i!='' and i!=" "]


mention = []
allmention = []
headwd = []
pronCandidates = []
pron = []
pronRefers = []
print("┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┐")
print("| Coreference Resolution Program |")
print("└ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┘")

#MENTION-DETECTION STEP
print("\n------------MENTIONS FOUND-----------\n")

for i in text:
    tree = parser.parse(i.split())
    #print('\n'.join(['\t'.join(node) for node in tree]))
    for node in tree:
        newmention = ''
        if (node[4]=='NN' or node[4]=='NNP' or node[4]=='NNPC' or node[4]=='NST') and (tree[int(node[6])-2][4]=='NST' or tree[int(node[6])-2][4]=='NNP' or tree[int(node[6])-2][4]=='NNPC' or tree[int(node[6])-2][4]=='NP'):
            for x in range(int(node[0])-1, int(tree[int(node[6])][0])-1):
                newmention += (tree[x][1].replace(')', '').replace('(', "") + ' ')
            if newmention != "":
                score=0
                if (tree[int(node[6])-1][7].find("k1") != -1):
                    score+=100
                elif (tree[int(node[6])-1][7].find("k2") != -1):
                    score+=80
                elif (tree[int(node[6])-1][7].find("k3") != -1):
                    score+=60
                elif (tree[int(node[6])-1][7].find("k4") != -1):
                    score+=50
                elif (tree[int(node[6])-1][7].find("k5") != -1):
                    score+=50
                elif (tree[int(node[6])-1][7].find("k7") != -1):
                    score+=50
                sentment = text.index(i)
                pronCandidates.append([newmention, score, sentment])
                mention.append(newmention)
                allmention.append(newmention)
                headwd.append([tree[int(node[6])-1][1], newmention, tree[int(node[6])-1][4]])
        elif (node[4]=='NN' or node[4]=='NNP' or node[4]=='NNPC' or node[4]=='NST'):
            b=False
            for m in mention:
                if (node[1]== m):
                    b = True
                    break
            if(not b) and node[1] != "":
                mention.append(node[1])
            if node[1] != "":
                score=0
                if (node[7].find("k1") != -1):
                    score+=100
                elif (node[7].find("k2") != -1):
                    score+=80
                elif (node[7].find("k3") != -1):
                    score+=60
                elif (node[7].find("k4") != -1):
                    score+=50
                elif (node[7].find("k5") != -1):
                    score+=50
                elif (node[7].find("k7") != -1):
                    score+=50
                sentment = text.index(i)
                pronCandidates.append([node[1], score, sentment])
                allmention.append(node[1])
                headwd.append([node[1], node[1], node[4]])
        if (node[4].find('PR') == 0):
            pronment = text.index(i)
            pron.append([node[1], pronment])
            for x in range(0,pronment+1):
                for y in pronCandidates:
                    if y[2] <= x:
                        diff = - y[2] + x
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

cluster=[]
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
            

# EXACT STRING MATCH STEP      
print("\n------------EXACT MATCHES FOUND-----------\n")

for i in allmention:
    #tree = parser.parse(i.split())
    #for node in tree:
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

        if i[0] == j[0] and ([i[1], j[1]] not in properHeadMatches) and ([j[1], i[1]] not in properHeadMatches) and (i[2] == "NNP"):
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

        if i[0] == j[0] and ([i[1], j[1]] not in headMatches) and ([j[1], i[1]] not in headMatches) and (i[2] != "NNP") and (i[2] != "NNPC"):
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
