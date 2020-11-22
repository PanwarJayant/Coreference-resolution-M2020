from __future__ import unicode_literals
from isc_parser import Parser
import re

parser = Parser(lang='hin')
text = '''
जम्मू कश्मीर:पीपुल्स एलायंस फॉर गुपकर डिक्लरेशन लड़ेगी DDC का चुनाव; भाजपा ने कहा- ये लोग 'गप्पा-कार' हैं
जम्मू-कश्मीर में एक बार फिर से राजनीति हलचलें तेज हो गई हैं ।
28 नवंबर से शुरू होने वाले जिला विकास परिषद (DDC) चुनावों में पीपुल्स एलायंस फॉर गुपकार डिक्लरेशन (PAGD) भी अपने उम्मीदवार उतारेगी ।
एलायंस ने शनिवार को इसका ऐलान किया ।
PAGD की अगुवाई नेशनल कॉन्फ्रेंस के अध्यक्ष फारूख अब्दुल्ला कर रहे हैं ।
केंद्र सरकार के फैसले से जम्मू कश्मीर के लोगों में नाराजगी
एलायंस के सज्जाद लोन ने कहा, '' 5 अगस्त 2019 के फैसले को लेकर जम्मू कश्मीर की आवाम नाराज है । 
लोग गुस्से में हैं ।
पीपुल्स एलायंस फॉर गुपकार डिक्लेरेशन के गठन के बाद हम लोगों ने आम लोगों से मुलाकात की ।
सिविल सोसाइटी से सदस्यों, राजनीतिक पार्टियों, गुर्जर-बकरवाल समुदायों, एससी-एसटी का नेतृत्व करने वालों से मुलाकात की ।
सभी आगामी DDC और पंचायत चुनाव मिलकर लड़ने की बात कही है ।
भाजपा और केंद्र की सरकार से जम्मू कश्मीर का विशेष दर्जा वापस मिलने तक लड़ाई जारी रहेगा ।''
PAGD में ये राजनीतिक पार्टियां मिलकर लड़ेंगी चुनाव
PAGD को नेशनल कॉन्फ्रंस, PDP, CPI(M) और आवामी नेशनल कॉन्फ्रेंस का समर्थन है ।
इसलिए ये सभी पार्टियां आपस में मिलकर DDC और पंचायत का चुनाव लड़ेंगी ।
हालांकि अभी यह तय नहीं हो पाया है कि किस पार्टी से कितने उम्मीदवार मैदान में उतारे जाएंगे ।
वहीं, दूसरी ओर कांग्रेस ने भी DDC चुनाव लड़ने का फैसला लिया है ।
कांग्रेस प्रदेश अध्यक्ष जीए मीर ने कहा, "कांग्रेस जम्मू-कश्मीर की जनता को नाराज करने वाली भाजपा की गलत और असंवैधानिक नीतियों के खिलाफ लड़ाई के लिये आगामी DDC चुनाव में अपने अच्छे उम्मीदवार उतारेगी ।
भाजपा को सबक सिखाया जाएगा ।"
भाजपा के प्रत्याशी भी मैदान में होंगे, गुपकार को गप्पा-कार कहा
भारतीय जनता पार्टी (बीजेपी) ने भी DDC चुनाव लड़ने का फैसला किया है ।
पार्टी के राष्ट्रीय महासचिव तरुण चुग ने कहा कि हम सभी सीटों पर अपने प्रत्याशी उतारेंगे ।
चुग ने कहा कि इस चुनाव से जम्मू-कश्मीर में लोकतंत्र को मजबूती मिलेगी ।
लोग अपने प्रतिनिधि को चुन सकेंगे ।
आगे उन्होंने गुपकार समझौते को 'गप्पा-कार' करार दिया ।
कहा कि गुपकार 'गप्पा-कार' है ।
उनके मुंगेरी लाल के सपने कभी सच नहीं होने वाले हैं ।
अब्दुल्ला एंड संस और मुफ्ती एंड संस ने जम्मू-कश्मीर के संसाधनों को लूटा है ।
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

#MENTION-DETECTION SIEVE
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
            pronRefers.append([node[1], pronCandidates[0][0]])

for men in allmention:
    print(men)

# CLUSTERING-SIEVE
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
            

# EXACT-MATCH SIEVE      
print("\n------------EXACT MATCHES FOUND-----------\n")

for i in allmention:
    #tree = parser.parse(i.split())
    #for node in tree:
    if i in mention:
        print(i, "and", i, "have exact match")




# RELAXED STRING MATCH SIEVE                
print("\n------------RELAXED MATCHES FOUND-----------\n")

for men1 in mention:
    for men2 in mention:
        if men1 != men2 and men1 != "" and men2 != "":
            if men1.find(men2) != -1:
                print(men1, "and", men2, "have a match")

# PROPER-HEAD-WORD MATCH SIEVE
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


# RELAXED HEAD-WORD MATCH SIEVE
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


# PRONOUN SIEVE
print("\n------------PRONOUN MATCHES FOUND-----------\n")

for reference in pronRefers:
    print("Pronoun", reference[0], "refers to", reference[1])
