import csv
import ipAddress as ipA
import domain as dm
import hash as ha
from docx import Document

filename = input("Enter name of file: ")
#with open('Reto Programacion - GS - Automatizacion de IOCs -AA20-099A_WHITE.csv', newline='\n') as csvfile:
try:
    with open(filename, newline='\n') as csvfile:
        rows = csv.reader(csvfile)
        lst_url, lst_ip, lst_hash = [], [], []
        for row in rows:
            row[0] = row[0].replace("[","").replace("]","")
            if row[0].isalnum():
                lst_hash.append(row[0])
            elif row[0].upper() == row[0].lower():
                lst_ip.append(row[0])
            elif row[0].find(" ") == -1 and row[0].find(".") != -1:
                lst_url.append(row[0])
except:
    print("Incorrect file name or it doesn't exists")
    exit(-1)

numOfURLs = len(lst_url)
neutralURLS, poorURLS, goodURLS, unknownURLSRep = 0, 0, 0, 0

numOfIPs = len(lst_ip)
neutralEmailRep, poorEmailRep, goodEmailRep, unknownEmailRep = 0, 0, 0, 0
neutralWebRep, poorWebRep, goodWebRep, unknownWebRep = 0, 0, 0, 0

numOfHASHES = len(lst_hash)
undetectedHASHES = 0

document = Document()

document.add_heading('Reporte Automatización de IoCs', 0)
d = document.add_paragraph("", style="List Bullet")
d.add_run("DETALLE").bold = True
urlText = document.add_paragraph("", style="List Bullet 2")
urlText.add_run("URLs").bold = True

urlCounter = 1
for url in lst_url:
    objUrlDomain = dm.domain(url)
    print(objUrlDomain.urlToDict())
    document.add_paragraph("\t" + str(urlCounter) + ". " + objUrlDomain.url)
    geo = document.add_paragraph('\t\ta. Geolocalización: ')
    geo.add_run(objUrlDomain.location)
    ip = document.add_paragraph('\t\tb. IP: ')
    ip.add_run(objUrlDomain.ip if objUrlDomain.ip != "Unknown" else "Desconocida")
    repu = document.add_paragraph('\t\tc. Reputación: ')
    if objUrlDomain.reputation[1] == 'Poor':
        repu.add_run("Mala")
        poorURLS += 1
    elif objUrlDomain.reputation[1] == 'Neutral':
        repu.add_run("Neutral")
        neutralURLS += 1
    elif objUrlDomain.reputation[1] == 'Good':
        repu.add_run("Buena")
        goodURLS += 1
    else:
        repu.add_run("Desconocida")
        unknownURLSRep += 1
    category = document.add_paragraph('\t\td. Categoría: ')
    category.add_run(objUrlDomain.category if objUrlDomain.category != [] else "Sin Categorizar")

    urlCounter += 1

###IPs
ipText = document.add_paragraph("", style="List Bullet 2")
ipText.add_run("IPs").bold = True

ip_counter = 1
for ip in lst_ip:
    objIp = ipA.ipAddress(ip)
    print(objIp.ipToDict())
    document.add_paragraph("\t" + str(ip_counter) + ". " + objIp.ip)
    geo = document.add_paragraph('\t\ta. Geolocalización: ')
    geo.add_run(objIp.location)
    eR = document.add_paragraph('\t\tb. Reputación Email: ')
    if objIp.emailReputation == 'Poor':
        eR.add_run("Mala")
        poorEmailRep += 1
    elif objIp.emailReputation == 'Neutral':
        eR.add_run(objIp.emailReputation)
        neutralEmailRep += 1
    elif objIp.emailReputation == 'Good':
        eR.add_run("Buena")
        goodEmailRep += 1
    else:
        unknownEmailRep += 1
        eR.add_run("Desconocida")

    wR = document.add_paragraph('\t\tc. Reputación Web: ')
    if objIp.webReputation == 'Poor':
        wR.add_run("Mala")
        poorWebRep += 1
    elif objIp.webReputation == 'Neutral':
        wR.add_run(objIp.webReputation)
        neutralWebRep += 1
    elif objIp.webReputation == 'Good':
        wR.add_run("Buena")
        goodWebRep += 1
    else:
        unknownWebRep += 1
        wR.add_run("Desconocida")
    ip_counter += 1

h = document.add_paragraph("", style="List Bullet 2")
h.add_run("HASHES").bold = True

i = 1
for hashCode in lst_hash:
    objHash = ha.hash(hashCode)
    print(objHash.hashToDict())
    document.add_paragraph("\t"+ str(i) + ". " + objHash.hashCode)
    a1 = document.add_paragraph('\t\ta. Lo detecta McAfee? ')
    a1.add_run("No" if objHash.antiVDict['McAfee']=="undetected" else "Si")
    a2 = document.add_paragraph('\t\tb. Lo detecta ESET-NOD32? ')
    a2.add_run("No" if objHash.antiVDict['ESET-NOD32'] == "undetected" else "Si")
    a3 = document.add_paragraph('\t\tc. Lo detecta F-Secure? ')
    a3.add_run("No" if objHash.antiVDict['F-Secure'] == "undetected" else "Si")
    a4 = document.add_paragraph('\t\td. Lo detecta Kaspersky? ')
    a4.add_run("No" if objHash.antiVDict['Kaspersky'] == "undetected" else "Si")
    if 'malicious' in objHash.antiVDict.values():
        pass
    else:
        undetectedHASHES += 1
    #print(undetectedHASHES)
    i += 1

##RESUMEN
resumen = d.insert_paragraph_before('',style="List Bullet")
resumen.add_run("RESUMEN").bold = True

def addToResumen(detalle, text, result, style):
    r_1 = detalle.insert_paragraph_before('', style=style)
    r_1.add_run(text).bold = True
    r_1.add_run(result)

print("Number of URLs: ", numOfURLs)
print("Poor URLs: ", poorURLS)
print("Neutral URLs: ", neutralURLS)
print("Good URLs", goodURLS)
print("Unknown URLs", unknownURLSRep)

print("Number of IPs: ", numOfIPs)
print("Poor Email Reputation, Poor Web Reputation: ", poorEmailRep, poorWebRep)
print("Neutral Email Reputation, Neutral Web Reputation: ", neutralEmailRep, neutralWebRep)
print("Good Email Reputation, Good Web Reputation: ", goodEmailRep, goodWebRep)
print("Unknown Email Reputation, Unknown Web Reputation: ", unknownEmailRep, unknownWebRep)


print("Number of Hashes: ",numOfHASHES)
print("Undetected Hashes: ", undetectedHASHES)


addToResumen(d, "Cantidad de URLs: ", str(numOfURLs), "List Bullet 2")
addToResumen(d, "No maliciosas: ", str(goodURLS), "List Bullet 3")
addToResumen(d, "Neutrales: ", str(neutralURLS), "List Bullet 3")
addToResumen(d, "Maliciosas: ", str(poorURLS), "List Bullet 3")
addToResumen(d, "Desconocidas: ", str(unknownURLSRep), "List Bullet 3")

addToResumen(d, "Cantidad de IPs: ", str(numOfIPs), "List Bullet 2")
addToResumen(d, "Buena Reputación Email: ", str(goodEmailRep), "List Bullet 3")
addToResumen(d, "Reputación Email Neutral: ", str(neutralEmailRep), "List Bullet 3")
addToResumen(d, "Mala Reputación Email: ", str(poorEmailRep), "List Bullet 3")
addToResumen(d, "Reputación Email Desconocida: ", str(unknownEmailRep), "List Bullet 3")
addToResumen(d, "Buena Reputación Web: ", str(goodWebRep), "List Bullet 3")
addToResumen(d, "Reputación Web Neutral: ", str(neutralWebRep), "List Bullet 3")
addToResumen(d, "Mala Reputación Web: ", str(poorWebRep), "List Bullet 3")
addToResumen(d, "Reputación Web Desconocida: ", str(unknownWebRep), "List Bullet 3")

addToResumen(d, "Cantidad de HASHES: ", str(numOfHASHES), "List Bullet 2")
addToResumen(d, "No detectado por ninguno de los 4 antivirus: ", str(undetectedHASHES), "List Bullet 3")

document.save('Reporte.docx')
