from pytesseract import image_to_string
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import re
import dateutil.parser as dparser

#I have used some basic heuristics after going through the images to get some features. It's not guaranteed to be optimal.

#Majority of the US receipts have the state code and the '$' sign

#US date format is different from other countries.
def find_if_us(string):
    all_states = ['al','ak','az','ar','ca','co','ct','dc','de','fl','ga','hi','id',
          'il','in','ia','ks','ky','la','me','md','ma','mi','mn','ms','mo',
          'mt','ne','nv','nh','nj','nm','ny','nc','nd','oh','ok','or','pa',
          'ri','sc','sd','tn','tx','ut','vt','va','wa','wv','wi','wy']
    matches = 0
    allTexts = string.split("\n")
    for entry in allTexts:
        
        storedMatches = []
    
    #for each entry:
        allWords = entry.split(' ')
        for words in allWords:

        #remove punctuation that will interfere with matching
            words = words.replace(',', '')
            words = words.replace('.', '')
            words = words.replace(';', '')


        #if a keyword match is found, store the result.
            if words in all_states:
                if words in storedMatches:
                    continue
                else:
                    storedMatches.append(words)
                
                matches += 1
        
        #if there is a match
        if matches == 0:
            us_state = False
            
        
        
        else:

            us_state = True
            
    return(us_state)


def get_date(string,country):  #country=True ==>US 
    
    if(string==0):
        date = 0
    
    else:
        search = []
        for i in string:
            if(i.isalnum()==True or i=='/' or i =='-'):
                search.append(i)    

        search = "".join(search)
        #return location_based(search,country)
        if country == True:         #country True indicating that it's the US
            try:
                date = dparser.parse(search,fuzzy=True).timetuple()
                date = str(date[0])+"-"+"{0:0=2d}".format(date[1])+"-"+"{0:0=2d}".format(date[2])

            except:
                try:
                    date = dparser.parse(search,fuzzy=True, dayfirst=True)
                    date = str(date[0])+"-"+"{0:0=2d}".format(date[1])+"-"+"{0:0=2d}".format(date[2])
                except:    
                    date = 0
        if country == False:
            try:

                date = dparser.parse(search,fuzzy=True, dayfirst=True)
                date = str(date[0])+"-"+"{0:0=2d}".format(date[1])+"-"+"{0:0=2d}".format(date[2])

            except:
                date = 0
    
    return date

def heur(string,country):
    

    d1 = re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", string)    #12/12/2019
    d2 = re.findall(r"[\d]{1,2}-[\d]{1,2}-[\d]{2}", string)    #12-12-19
    d3 = re.findall(r"(\d{1,2} (?:jan|feb|mar|apr|may|jun|jul|aug|sept|oct|nov|dec) \d{4})", string) #5 mar 2018  
    d4 = re.findall(r"[\d]{1,2}-[\d]{1,2}-[\d]{4}", string)  #02-10-2018
    d5 = re.findall(r"[\d]{4}-[\d]{1,2}-[\d]{1,2}", string)  #2018-10-05
    d6 = re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{2}", string)  #05/01/2018
    
    date = max(d1,d2,d3,d4,d5,d6)
    
    
    if date!=[]:
        if(len(date)>1):
            del date[-1]
        date = ''.join(date)

        if(country == True):
            try:
                
                date = dparser.parse(date,fuzzy=True).timetuple()
                date = str(date[0])+"-"+"{0:0=2d}".format(date[1])+"-"+"{0:0=2d}".format(date[2])
            except:
                try:
                    date = dparser.parse(date,fuzzy=True,dayfirst=True).timetuple()
                    date = str(date[0])+"-"+"{0:0=2d}".format(date[1])+"-"+"{0:0=2d}".format(date[2])
                except:
                    date = 0
                    
        if(country == False):
            try:
                
                date = dparser.parse(date,fuzzy=True,dayfirst=True).timetuple()
                date = str(date[0])+"-"+"{0:0=2d}".format(date[1])+"-"+"{0:0=2d}".format(date[2])
            except:
                date = 0
            
    else:
        date = 0
    return date

def to_find(string):
    #searching for comma,slash,dot,hyphen or anything that might indicate the presence of a date
    
        
    try:
            
        ix = [m.start() for m in re.finditer(r'{}'.format(re.escape("/")), string)][-1]
        
        
        
        
    except:
        try:
            
            ix = [m.start() for m in re.finditer(r'{}'.format(re.escape(".")), string)][-1]
            
            
        except:
            try:
                
                ix = [m.start() for m in re.finditer(r'{}'.format(re.escape("'")), string)][-1]
            except:
                try:
                    
                    ix = [m.start() for m in re.finditer(r'{}'.format(re.escape(",")), string)][-1]
                except:
                    try:
                        ix = [m.start() for m in re.finditer(r'{}'.format(re.escape("-")), string)][-1]
                        
                    except:
                        
                        ix = 0
               
                
    return ix        

def found_date(string,country):
    #find position of 'date' 
    dix = string.find('date')
    q = string[dix:dix+23]
    q = re.sub('[:\n|&?,‘]', ' ', q)
    
    try:
        if(country == False):   
            
            date = dparser.parse(q,fuzzy=True,dayfirst=True).timetuple()
        if(country == True):
            date = dparser.parse(q,fuzzy=True).timetuple()
            
        date = str(date[0])+"-"+"{0:0=2d}".format(date[1])+"-"+"{0:0=2d}".format(date[2])
    except:
        try:

            if(q[to_find(q)+3]!= ' '):
                z = q[0:to_find(q)+6]
                if(country==False):
                    
                    date = dparser.parse(z,fuzzy=True,dayfirst=True).timetuple()
                if(country == True):
                    date = dparser.parse(z,fuzzy=True).timetuple()
                
                date = str(date[0])+"-"+"{0:0=2d}".format(date[1])+"-"+"{0:0=2d}".format(date[2])

            else:
                z = q[0:to_find(q)+3]
                if(country==False):
                    date = dparser.parse(z,fuzzy=True,dayfirst=True).timetuple()
                if(country == True):
                    date = dparser.parse(z,fuzzy=True).timetuple()
                
                date = str(date[0])+"-"+"{0:0=2d}".format(date[1])+"-"+"{0:0=2d}".format(date[2])

        except:
            date = 0
    
        
        
    return date  

def extract_date(receipt):             #here is where you pass the image to get the date
    
    
    img = Image.open(receipt)

    all_text = image_to_string(img)
    all_text = all_text.lower()
    check = []
        
    
    if(find_if_us(all_text)==True or '$' in all_text):
        location = True

    else:
        location = False

    check.append(get_date(all_text,location))

    check.append(heur(all_text,location))

    check.append(found_date(all_text,location)) 
    
    if([num for num in check if (num and type(num)!=bool)] != []):  #if date is present
        response_date = [num for num in check if (num and type(num)!=bool)]
    else:             
        response_date =  None             #if date is not present
    
           
    return response_date 
