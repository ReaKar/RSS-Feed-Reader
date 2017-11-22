# Ανάκτηση δεδομένων από τη diavgeia.gov.gr


import re
import urllib.request
import urllib.error

arxes = {}

def rss_feed(url): 
    '''
    Άνοιγμα του rss feed,
    :param url: η διεύθυνση του rss feed.
    Αυτή η συνάρτηση δημιουργεί ένα αρχείο
    με τα περιεχόμενα του rss_feed με όνομα?
    την διεύθυνση του rss feed.
    Καλεί την συνάρτηση process_feed
    η οποία επιλέγει και τυπώνει περιεχόμενο
    Προσπαθήστε να κάνετε try/except τα exceptions
    HTTPError και URLError.
    '''
    #σύμφωνα με την ανακοίνωση της διαύγειας τα rss feeds είναι στο ίδιο url/rss
    
    url += r"/rss" 
  
    
   
    try:
        req = urllib.request.Request(url)
      
        with urllib.request.urlopen(req) as response:
          
            char_set = response.headers.get_content_charset()
            rss = response.read().decode(char_set)
        
        filename =url.replace('/','_')+'.txt'
        
        
        with open(filename, "w", encoding=char_set) as p:
            p.write(rss)
    except urllib.error.HTTPError as e:
        print(e.code)
       
        print(e.readline())
       
    except urllib.error.URLError as e:
        print(e)
        if hasattr(e, 'reason'):  # χωρίς σύνδεση ιντερνετ
            print('Αποτυχία σύνδεσης στον server')
            print('Αιτία: ', e.reason)
    else:
        process_feed(filename)
    
    pass



def process_feed(filename): 
    '''
    συνάρτηση που ανοίγει το αρχείο με το rss feed και 
    τυπώνει την ημερομηνία και τους τίτλους των αναρτήσεων που περιέχει.
    Xρησιμοποιήστε regular expressions 
    '''
    with open(filename, 'r', encoding = 'utf-8') as f :
      rss = f.read().replace("\n", " ")

      day=re.findall(r"<lastBuildDate>(.*?)</lastBuildDate>",rss, re.MULTILINE | re.IGNORECASE)
    
      
      for d in day:
        print(" ","\t",d)
      
      n=0   
      
      title = re.findall(r"<title>(.*?)</title>",rss, re.MULTILINE | re.IGNORECASE)
      print("***",title[0],"***")
      for t in title[1:]:
          n=n+1
          print(n,"\t",t)
    pass

def search_arxes(arxh): 
    a=0
    a=int(a)
    list=[]
   
    for key in arxes:
    
      list.insert(a,key)
      a=a+1
    list = [s for s in list if arxh in s]
    
    return  list
    '''
    Αναζήτηση ονόματος Αρχής που ταιριάζει στα κριτήρια του χρήστη
    '''
    pass

def load_arxes():
    '''
    
    φορτώνει τις αρχές στο λεξικό arxes{}
    '''
    d=0
    d=int(d)
    with open('500_arxes.csv', 'r', encoding = 'utf-8') as f :
      for line in f.readlines() :
        
         key, value = line.rstrip('\n').split(';')
         arxes[key] = (value)
         
    
     
    
       
    pass
######### main ###############
'''
το κυρίως πρόγραμμα διαχειρίζεται την αλληλεπίδραση με τον χρήστη
'''
load_arxes()
while True :
    arxh = input(50*"^"+"\nΟΝΟΜΑ ΑΡΧΗΣ:(τουλάχιστον 3 χαρακτήρες), ? για λίστα:")
    if arxh == '':
        break
    elif arxh == "?": # παρουσιάζει τα ονόματα των αρχών
        for k,v in arxes.items():
            print (k,v)
           
    elif len(arxh) >= 3 :
        # αναζητάει όνομα αρχής που ταιριάζει στα κριτήρια του χρήστη
        result = search_arxes(arxh) 
        for r in result:
            print (result.index(r)+1, r, arxes[r])
        while result:
            epilogh = input("ΕΠΙΛΟΓΗ....")
            if epilogh == "": break
            elif epilogh.isdigit() and 0<int(epilogh)<len(result)+1:
                epilogh = int(epilogh)
                url = arxes[result[epilogh-1]]
                print(url)
                # καλεί τη συνάρτηση που φορτώνει το αρχείο rss:
                rss_feed(url)
            else: continue
    else :
        continue