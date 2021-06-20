from flask import Flask, render_template
from flask_socketio import SocketIO
from flask import url_for,request
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
# from sklearn.externals import joblib
from Pre2 import Preprocessing
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request
from svm import svm
import json

ratee = pd.read_csv('../User Rating/Rating.csv')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

from flask_socketio import send, emit

@app.route('/')
def home():
	return render_template('chat.html')

@app.route('/predict',methods=['POST'])
def predict():
    # teks = "Membalas : Saham mana yg arb berhari2 IKAN mungkin wkwk" #Negatif
    # teks = "Doid masih aman kalo belinya pas april 2020" #Positif
    teks = "Ati2 bank uda kena brp x suspend... Buangan nya banyak tuh barusan.jgn dikejar"

    svm = SVC(kernel='rbf')
    cv = TfidfVectorizer(use_idf=True)

    df = pd.read_csv('readytfidf3.csv')
    df = df.sample(frac = 1)
    df['Status'] = df['Status'].replace(['Negatif', 'Positif'], ['0','1'])
    y = df['Status']
    X = df['Normal']
    X = cv.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    svm.fit(X_train,y_train)
    print("accuracy score: " + str(svm.score(X_test, y_test)))
    if request.method == 'POST':
        tekss = request.form['message']
        tekss = Preprocessing(tekss)
        print(tekss)
        vect = cv.transform([tekss])
        my_prediction = svm.predict(vect)
        my_prediction = int(my_prediction[0])
        print("accuracy score: " + str(svm.score(X_test, y_test)))
        print(my_prediction)
    return render_template('result.html',prediction = my_prediction)

@socketio.on('my event')
def handle_my_custom_event(json):
    def formatJam(teks):
        print('Jam nya adalah : '+teks)
        formm = teks.split()
        satuan = formm[1]
        jamm = formm[0]
        jamm = jamm.split(':')
        jam2 = jamm[0]
        menit = jamm[1]
        detik = jamm[2]
        formatt = jam2+menit+detik
        return int(formatt)

    nama = 'Aku adalah agias'

    myprofile = webdriver.FirefoxProfile(r'C:\Users\Aloysius\AppData\Roaming\Mozilla\Firefox\Profiles\fcbei8vp.teleScrape')
    PATH = "C:\Program Files (x86)\geckodriver.exe"
    driver = webdriver.Firefox(firefox_profile=myprofile ,executable_path=PATH)

    target = 3
    Saham = ['AALI', 'ABBA', 'ABDA', 'ABMM', 'ACES', 'ACST', 'ADES', 'ADHI', 'ADMF', 'ADMG', 'ADRO', 'AGAR', 'AGII', 'AGRO', 'AGRS', 'AHAP', 'AIMS', 'AISA', 'AKKU', 'AKPI', 'AKRA', 'AKSI', 'ALDO', 'ALKA', 'ALMI', 'ALTO', 'AMAG', 'AMAN', 'AMAR', 'AMFG', 'AMIN', 'AMOR', 'AMRT', 'ANDI', 'ANJT', 'ANTM', 'APEX', 'APIC', 'APII', 'APLI', 'APLN', 'ARGO', 'ARII', 'ARKA', 'ARMY', 'ARNA', 'ARTA', 'ARTI', 'ARTO', 'ASBI', 'ASDM', 'ASGR', 'ASII', 'ASJT', 'ASMI', 'ASPI', 'ASRI', 'ASRM', 'ASSA', 'ATAP', 'ATIC', 'AUTO', 'AYLS', 'BABP', 'BACA', 'BAJA', 'BALI', 'BANK', 'BAPA', 'BAPI', 'BATA', 'BAYU', 'BBCA', 'BBHI', 'BBKP', 'BBLD', 'BBMD', 'BBNI', 'BBRI', 'BBRM', 'BBSI', 'BBSS', 'BBTN', 'BBYB', 'BCAP', 'BCIC', 'BCIP', 'BDMN', 'BEBS', 'BEEF', 'BEKS', 'BELL', 'BESS', 'BEST', 'BFIN', 'BGTG', 'BHAT', 'BHIT', 'BIKA', 'BIMA', 'BINA', 'BIPI', 'BIPP', 'BIRD', 'BISI', 'BJBR', 'BJTM', 'BKDP', 'BKSL', 'BKSW', 'BLTA', 'BLTZ', 'BLUE', 'BMAS', 'BMRI', 'BMSR', 'BMTR', 'BNBA', 'BNBR', 'BNGA', 'BNII', 'BNLI', 'BOGA', 'BOLA', 'BOLT', 'BOSS', 'BPFI', 'BPII', 'BPTR', 'BRAM', 'BRIS', 'BRMS', 'BRNA', 'BRPT', 'BSDE', 'BSIM', 'BSSR', 'BSWD', 'BTEK', 'BTEL', 'BTON', 'BTPN', 'BTPS', 'BUDI', 'BUKK', 'BULL', 'BUMI', 'BUVA', 'BVIC', 'BWPT', 'BYAN', 'CAKK', 'CAMP', 'CANI', 'CARE', 'CARS', 'CASA', 'CASH', 'CASS', 'CBMF', 'CCSI', 'CEKA', 'CENT', 'CFIN', 'CINT', 'CITA', 'CITY', 'CLAY', 'CLEO', 'CLPI', 'CMNP', 'CMPP', 'CNKO', 'CNTX', 'COCO', 'COWL', 'CPIN', 'CPRI', 'CPRO', 'CSAP', 'CSIS', 'CSMI', 'CSRA', 'CTBN', 'CTRA', 'CTTH', 'DADA', 'DART', 'DAYA', 'DCII', 'DEAL', 'DEFI', 'DEWA', 'DFAM', 'DGIK', 'DGNS', 'DIGI', 'DILD', 'DIVA', 'DKFT', 'DLTA', 'DMAS', 'DMMX', 'DMND', 'DNAR', 'DNET', 'DOID', 'DPNS', 'DPUM', 'DSFI', 'DSNG', 'DSSA', 'DUCK', 'DUTI', 'DVLA', 'DWGL', 'DYAN', 'EAST', 'ECII', 'EDGE', 'EKAD', 'ELSA', 'ELTY', 'EMDE', 'EMTK', 'ENRG', 'ENVY', 'ENZO', 'EPAC', 'EPMT', 'ERAA', 'ERTX', 'ESIP', 'ESSA', 'ESTA', 'ESTI', 'ETWA', 'EXCL', 'FAPA', 'FAST', 'FASW', 'FILM', 'FINN', 'FIRE', 'FISH', 'FITT', 'FMII', 'FOOD', 'FORU', 'FORZ', 'FPNI', 'FREN', 'FUJI', 'GAMA', 'GDST', 'GDYR', 'GEMA', 'GEMS', 'GGRM', 'GGRP', 'GHON', 'GIAA', 'GJTL', 'GLOB', 'GLVA', 'GMFI', 'GMTD', 'GOLD', 'GOLL', 'GOOD', 'GPRA', 'GSMF', 'GTBO', 'GWSA', 'GZCO', 'HADE', 'HDFA', 'HDIT', 'HDTX', 'HEAL', 'HELI', 'HERO', 'HEXA', 'HITS', 'HKMU', 'HMSP', 'HOKI', 'HOME', 'HOMI', 'HOTL', 'HRME', 'HRTA', 'HRUM', 'IATA', 'IBFN', 'IBST', 'ICBP', 'ICON', 'IDPR', 'IFII', 'IFSH', 'IGAR', 'IIKP', 'IKAI', 'IKAN', 'IKBI', 'IMAS', 'IMJS', 'IMPC', 'INAF', 'INAI', 'INCF', 'INCI', 'INCO', 'INDF', 'INDO', 'INDR', 'INDS', 'INDX', 'INDY', 'INKP', 'INOV', 'INPC', 'INPP', 'INPS', 'INRU', 'INTA', 'INTD', 'INTP', 'IPCC', 'IPCM', 'IPOL', 'IPTV', 'IRRA', 'ISAT', 'ISSP', 'ITIC', 'ITMA', 'ITMG', 'JAST', 'JAWA', 'JAYA', 'JECC', 'JGLE', 'JIHD', 'JKON', 'JKSW', 'JMAS', 'JPFA', 'JRPT', 'JSKY', 'JSMR', 'JSPT', 'JTPE', 'KAEF', 'KARW', 'KAYU', 'KBAG', 'KBLI', 'KBLM', 'KBLV', 'KBRI', 'KDSI', 'KEEN', 'KEJU', 'KIAS', 'KICI', 'KIJA', 'KINO', 'KIOS', 'KJEN', 'KKGI', 'KLBF', 'KMDS', 'KMTR', 'KOBX', 'KOIN', 'KONI', 'KOPI', 'KOTA', 'KPAL', 'KPAS', 'KPIG', 'KRAH', 'KRAS', 'KREN', 'LAND', 'LAPD', 'LCGP', 'LCKM', 'LEAD', 'LIFE', 'LINK', 'LION', 'LMAS', 'LMPI', 'LMSH', 'LPCK', 'LPGI', 'LPIN', 'LPKR', 'LPLI', 'LPPF', 'LPPS', 'LRNA', 'LSIP', 'LTLS', 'LUCK', 'MABA', 'MAGP', 'MAIN', 'MAMI', 'MAPA', 'MAPB', 'MAPI', 'MARI', 'MARK', 'MASA', 'MAYA', 'MBAP', 'MBSS', 'MBTO', 'MCAS', 'MCOR', 'MDIA', 'MDKA', 'MDKI', 'MDLN', 'MDRN', 'MEDC', 'MEGA', 'MERK', 'META', 'MFIN', 'MFMI', 'MGNA', 'MGRO', 'MICE', 'MIDI', 'MIKA', 'MINA', 'MIRA', 'MITI', 'MKNT', 'MKPI', 'MLBI', 'MLIA', 'MLPL', 'MLPT', 'MMLP', 'MNCN', 'MOLI', 'MPMX', 'MPOW', 'MPPA', 'MPRO', 'MRAT', 'MREI', 'MSIN', 'MSKY', 'MTDL', 'MTFN', 'MTLA', 'MTPS', 'MTRA', 'MTSM', 'MTWI', 'MYOH', 'MYOR', 'MYRX', 'MYTX', 'NASA', 'NATO', 'NELY', 'NFCX', 'NICK', 'NIKL', 'NIPS', 'NIRO', 'NISP', 'NOBU', 'NRCA', 'NUSA', 'NZIA', 'OASA', 'OCAP', 'OKAS', 'OMRE', 'OPMS', 'PADI', 'PALM', 'PAMG', 'PANI', 'PANR', 'PANS', 'PBID', 'PBRX', 'PBSA', 'PCAR', 'PDES', 'PEGE', 'PEHA', 'PGAS', 'PGJO', 'PGLI', 'PGUN', 'PICO', 'PJAA', 'PKPK', 'PLAN', 'PLAS', 'PLIN', 'PMJS', 'PMMP', 'PNBN', 'PNBS', 'PNGO', 'PNIN', 'PNLF', 'PNSE', 'POLA', 'POLI', 'POLL', 'POLU', 'POLY', 'POOL', 'PORT', 'POSA', 'POWR', 'PPGL', 'PPRE', 'PPRO', 'PRAS', 'PRDA', 'PRIM', 'PSAB', 'PSDN', 'PSGO', 'PSKT', 'PSSI', 'PTBA', 'PTDU', 'PTIS', 'PTPP', 'PTPW', 'PTRO', 'PTSN', 'PTSP', 'PUDP', 'PURA', 'PURE', 'PURI', 'PWON', 'PYFA', 'PZZA', 'RAJA', 'RALS', 'RANC', 'RBMS', 'RDTX', 'REAL', 'RELI', 'RICY', 'RIGS', 'RIMO', 'RISE', 'RMBA', 'ROCK', 'RODA', 'RONY', 'ROTI', 'RUIS', 'SAFE', 'SAME', 'SAMF', 'SAPX', 'SATU', 'SBAT', 'SCCO', 'SCMA', 'SCNP', 'SCPI', 'SDMU', 'SDPC', 'SDRA', 'SFAN', 'SGER', 'SGRO', 'SHID', 'SHIP', 'SIDO', 'SILO', 'SIMA', 'SIMP', 'SINI', 'SIPD', 'SKBM', 'SKLT', 'SKRN', 'SKYB', 'SLIS', 'SMAR', 'SMBR', 'SMCB', 'SMDM', 'SMDR', 'SMGR', 'SMKL', 'SMMA', 'SMMT', 'SMRA', 'SMRU', 'SMSM', 'SOCI', 'SOFA', 'SOHO', 'SONA', 'SOSS', 'SOTS', 'SPMA', 'SPTO', 'SQMI', 'SRAJ', 'SRIL', 'SRSN', 'SRTG', 'SSIA', 'SSMS', 'SSTM', 'STAR', 'STTP', 'SUGI', 'SULI', 'SUPR', 'SURE', 'SWAT', 'TALF', 'TAMA', 'TAMU', 'TARA', 'TAXI', 'TBIG', 'TBLA', 'TBMS', 'TCID', 'TCPI', 'TDPM', 'TEBE', 'TECH', 'TELE', 'TFAS', 'TFCO', 'TGKA', 'TGRA', 'TIFA', 'TINS', 'TIRA', 'TIRT', 'TKIM', 'TLKM', 'TMAS', 'TMPO', 'TNCA', 'TOBA', 'TOPS', 'TOTL', 'TOTO', 'TOWR', 'TOYS', 'TPIA', 'TPMA', 'TRAM', 'TRIL', 'TRIM', 'TRIN', 'TRIO', 'TRIS', 'TRJA', 'TRST', 'TRUK', 'TRUS', 'TSPC', 'TUGU', 'TURI', 'UANG', 'UCID', 'UFOE', 'ULTJ', 'UNIC', 'UNIQ', 'UNIT', 'UNSP', 'UNTR', 'UNVR', 'URBN', 'VICI', 'VICO', 'VINS', 'VIVA', 'VOKS', 'VRNA', 'WAPO', 'WEGE', 'WEHA', 'WICO', 'WIFI', 'WIIM', 'WIKA', 'WINS', 'WMUU', 'WOMF', 'WOOD', 'WOWS', 'WSBP', 'WSKT', 'WTON', 'YELO', 'YPAS', 'YULE', 'ZBRA', 'ZINC', 'ZONE']
    hari = 0
    tanggal2 = []
    tanggal = []
    itemss=[]
    percakapan = []
    # driver.get('https://web.telegram.org/#/im?p=@TheTradersGroup')
    driver.get('https://web.telegram.org/#/im?p=g579054022')
    time.sleep(20)
    temp = ''
    temp2 = ''
    first = True
    ptemp = ''
    wrapper = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]')
    chat = wrapper.find_elements_by_xpath(".//div[contains(@class, 'im_history_message_wrap')]")
    psn = len(chat)
    Stoped = False
    while True:
        joinn = False
        balas = ''
        penulis = ''
        last = penulis
        pesan2 = [""]
        jam = ''
        pesan2 = []
        pesan = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div["+str(psn)+"]")
        driver.execute_script("arguments[0].scrollIntoView(true);", pesan)
        psn -= 1
        if (len(pesan.find_elements_by_xpath(".//a[@class='im_message_photo_thumb']")) > 0) :
            # print('ini adalah foto')
            penulis = penulis + pesan.find_element_by_xpath(".//a[contains(@class, 'im_message_author user_color_')]").text
            gambar = pesan.find_element_by_xpath(".//img[@class='im_message_photo_thumb']").get_attribute('src')
            pesan4 = "photo"
            pesan2.insert(0, pesan4)
            if (len(pesan.find_elements_by_xpath(".//div[@class='im_message_photo_caption']")) > 0):
                last = pesan.find_element_by_xpath(".//div[@class='im_message_photo_caption']").text
                emo = pesan.find_elements_by_xpath(".//span[@class='emoji  emoji-spritesheet-0']")
                for x in emo :
                    if(x.text.strip()!=''):
                        last = last.replace(x.text.strip(), ' ')
                pesan4 = pesan4 + last
                pesan2.insert(0, last)
            jam = jam + pesan.find_element_by_xpath(".//span[@ng-bind='::historyMessage.date | time']").text
        elif (len(pesan.find_elements_by_xpath(".//span[@ng-switch-when='messageActionChatJoined']")) > 0):
            print('seseorang join')
            penulis = ''
            last = penulis
            pesan2 = [""]
            jam = ''
            joinn = True
            # print('Masuk2')
        elif (len(pesan.find_elements_by_xpath(".//span[@class='im_message_date_split_text']")) > 0):
            if((len(pesan.find_elements_by_xpath(".//div[@class='im_message_date_split im_service_message_wrap' and @style='display: none;']")) > 0)):
                if(len(pesan.find_elements_by_xpath(".//div[@class='im_message_text']"))>0):
                    print('Ini juga sebenernya pesan biasa')
                    penulis = penulis + pesan.find_element_by_xpath(".//a[contains(@class, 'im_message_author user_color_')]").text
                    last = pesan.find_element_by_xpath(".//div[@class='im_message_text']").text
                    emo = pesan.find_elements_by_xpath(".//span[@class='emoji  emoji-spritesheet-0']")
                    for x in emo :
                        if(x.text.strip()!=''):
                            last = last.replace(x.text.strip(), ' ')
                    pesan4 = last
                    pesan2.insert(0, pesan4)
                    try :
                        print('Masuk kesini kali2')
                        jam = jam + pesan.find_element_by_xpath(".//span[@ng-bind='::historyMessage.date | time']").text
                        if (jam == ''):
                            jamm2 = pesan.find_element_by_xpath(".//span[@class='im_message_date_text nocopy']")
                            jam = jam + jamm2.get_attribute('data-content')
                    except : 
                        print('Seperti nya masuk ke sini2')
                        jamm2 = pesan.find_element_by_xpath(".//span[@class='im_message_date_text nocopy']")
                        jam = jam + jamm2.get_attribute('data-content')
                    if(len(pesan.find_elements_by_xpath(".//span[@my-short-message='replyMessage']"))>0):
                        balas = pesan.find_element_by_xpath(".//span[@my-short-message='replyMessage']").text
                        emo = pesan.find_elements_by_xpath(".//span[@class='emoji  emoji-spritesheet-0']")
                        for x in emo :
                            if(x.text.strip()!=''):
                                balas = balas.replace(x.text.strip(), ' ')
                        pesan2.insert(0,"Membalas : " + balas)
            else :
                jamm2 = pesan.find_element_by_xpath(".//span[@class='im_message_date_text nocopy']")
                jam = jam + jamm2.get_attribute('data-content')
                print("ini adalah tanggal")
                tgl = pesan.find_element_by_xpath(".//span[@class='im_message_date_split_text']").text
                tgl = tgl.replace(",","")
                print(tgl)
                for k in range(len(tanggal2)):
                    tanggal2[k]['Tanggal'] = tgl
                tanggal.extend(tanggal2)
                hari +=1
                belum = (hari!=target)
                print(len(tanggal))
                tanggal2 = []
        else :
            print('ini adalah pesan biasa')
            penulis = penulis + pesan.find_element_by_xpath(".//a[contains(@class, 'im_message_author user_color_')]").text
            try :
                print('Masuk kesini kali')
                jam = jam + pesan.find_element_by_xpath(".//span[@ng-bind='::historyMessage.date | time']").text
                if (jam == ''):
                    jamm2 = pesan.find_element_by_xpath(".//span[@class='im_message_date_text nocopy']")
                    jam = jam + jamm2.get_attribute('data-content')
            except : 
                try:
                    print('Seperti nya masuk ke sini')
                    jamm2 = pesan.find_element_by_xpath(".//span[@class='im_message_date_text nocopy']")
                    jam = jam + jamm2.get_attribute('data-content')
                except :
                    print('seseorang join')
                    penulis = ''
                    last = penulis
                    pesan2 = [""]
                    jam = ''
                    joinn = True
            if(not joinn):
                last = pesan.find_element_by_xpath(".//div[@class='im_message_text']").text
                emo = pesan.find_elements_by_xpath(".//span[@class='emoji  emoji-spritesheet-0']")
                for x in emo :
                    if(x.text.strip()!=''):
                        last = last.replace(x.text.strip(), ' ')
                pesan4 = last
                pesan2.insert(0, pesan4)
                if(len(pesan.find_elements_by_xpath(".//span[@my-short-message='replyMessage']"))>0):
                    balas = pesan.find_element_by_xpath(".//span[@my-short-message='replyMessage']").text
                    emo = pesan.find_elements_by_xpath(".//span[@class='emoji  emoji-spritesheet-0']")
                    for x in emo :
                        if(x.text.strip()!=''):
                            balas = balas.replace(x.text.strip(), ' ')
                    pesan2.insert(0,"Membalas : " + balas)
        pesan3 = "\n".join(pesan2)
        masuk = False
        stop = [",", ".", "#", "?", "*", "-"]
        cek = pesan3
        bahas = []
        for x in stop:
            cek = cek.replace(x, " ")
        for x in pesan3:
            b = x.isascii()
            if not b:
                pesan3 = pesan3.replace(x, ' ')
        print('Jam sebelum berubah : ','|'+str(jam)+'|')
        if('M' not in str(jam)):
            jam2 = 0
        elif(jam!=0) :
            jam2 = formatJam(jam)
        else : 
            jam2 = 0
        print('Temp sebelum berubah : ',temp)
        if(temp == '' and not first):
            temp = 0
        elif(isinstance(temp,str) and temp != '') :
            temp = formatJam(jam)
        elif(not isinstance(temp,int)) :
            temp = 0
        print('banding = ',temp,'<', jam2)
        print(joinn)
        if((temp < jam2 or first) and not joinn):
            if (first):
                temp = jam2
                temp2 = jam2
            elif (temp2 == ''):
                temp2 = jam2
            if any(word in cek.upper().split() for word in Saham):
                masuk = True
            if(penulis != ""):
                ptemp = penulis
            else :
                penulis = ptemp
            if(True):
                if(True):
                    bahas = [word for word in Saham if word in cek.upper().split()]
                    for x in penulis:
                        c = x.isascii()
                        if not c:
                            penulis = penulis.replace(x, ' ')
                    bahas = ",".join(bahas)
                    print("Data : "+str(psn))
                    print("user : "+penulis)
                    print("Pesan : ",pesan3)
                    print("Saham : "+bahas)
                    predict = svm(pesan3)
                    print("Label : ",predict)
                    print("jam : " + jam)
                    print('=======================================================')
                    ada = False
                    print('Balas =',balas)
                    print('Percakapan =',percakapan)
                    # counttt = 0
                    if(not percakapan):
                        print('Cakap1')
                        percakapan.append([pesan4])
                        perindex = 1
                        ada = True
                    elif(balas!='') :
                        for a in percakapan:
                            print('Sub percakapan =',a)
                            perindex2 = percakapan.index(a)
                            for b in a:
                                # if(counttt==30):
                                #     print('############Batas#####################')
                                #     time.sleep(99)
                                # counttt+=1
                                print('Sub a =',b+'||')
                                if(balas in b and balas!=''):
                                    print('Cakap2')
                                    percakapan[perindex2].append(pesan4)
                                    perindex = perindex2 + 1
                                    ada = True
                    if(not ada):
                        print('Cakap3')
                        percakapan.append([pesan4])
                        perindex = percakapan.index([pesan4]) + 1
                    exist = penulis in ratee.User.values
                    if(exist):
                        df1 = ratee[ratee['User']==penulis]
                        hit = df1.iloc[0]['Hit']
                        miss = df1.iloc[0]['Miss']
                        rate = df1.iloc[0]['Rate']
                        # print(exist)
                    else :
                        hit = 'No Record'
                        miss = 'No Record'
                        rate = 'No Record'
                    item = {
                        'User' : penulis,
                        'Pesan' : pesan3,
                        'Saham' : bahas,
                        'Label' : predict,
                        'Jam' : jam,
                        'Hit' : str(hit),
                        'Miss' : str(miss),
                        'Rate' : str(rate),
                        'Percakapan' : str(perindex)
                    }
                    itemss.append(item)
                    # if(not pesan3==''):
                    #     emit('my response', item)
                    tanggal2.append(item)
                penulis = ""
                pesan2 = []
            jam = ""
            print('$$$$$$$$$$$$$$$$$$$$$$$$END OF FOR$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            if (first == True):
                Stoped = True
        else :
            Stoped = True
        if(Stoped) :
            if(itemss):
                itemss.reverse()
                for it in itemss:
                    emit('my response', it)
            itemss=[]
            # time.sleep(10)
            print('Temp sebelum masuk stop : ',temp)
            if (not first):
                if (temp2 != ''):
                    temp = temp2
            temp2 = ''
            # time.sleep(300)
            driver.execute_script("location.reload()")
            time.sleep(10)
            psn=0
            while psn==0:
                wrapper = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]')
                chat = wrapper.find_elements_by_xpath(".//div[contains(@class, 'im_history_message_wrap')]")
                psn = len(chat)
            Stoped = False
            temp3 = 0
            while temp3 != psn:
                temp3 = psn
                pesan = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div["+str(psn)+"]")
                driver.execute_script("arguments[0].scrollIntoView(true);", pesan)
                print("************************************SCROLL***********************************************8")
                time.sleep(2)
                wrapper = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]')
                chat = wrapper.find_elements_by_xpath(".//div[contains(@class, 'im_history_message_wrap')]")
                psn = len(chat)
        print('Jam di akhir = ',jam)
        print('Temp di akhir = ',temp)
        first = False
if __name__ == '__main__':
    socketio.run(app)