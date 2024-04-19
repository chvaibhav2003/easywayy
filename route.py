def find(initial,final,arr):
    if((initial in arr) and (final in arr)):
        if (arr.index(final)<arr.index(initial)):
            return (arr[arr.index(final)+1:arr.index(initial)])[::-1]
        else:
            return (arr[arr.index(initial)+1:arr.index(final)])
    return []




def locator(initial,final):
    a = [["MASURI,Ghaziabad","SunderDeep Group of Institutions,Ghaziabad","Dasna,Ghaziabad","IMS Engineering College,Ghaziabad","Mishal Garhi,Ghaziabad"
      ,"Harsaon Kamla Nehru Nagar,Ghaziabad","Panchsheel Primrose,Ghaziabad","GovindPuram,Ghaziabad","Chiranjeev Vihar,Ghaziabad",
      "Police_Line,Ghaziabad","Shastri Nagar D-Block,Ghaziabad","Hapur Chungi,Ghaziabad","Kavi Nagar,Ghaziabad","District Court and Session Court,Ghaziabad","RDC,Ghaziabad"],["Bamheta,Ghaziabad","PandavNagar,Ghaziabad","Kavi Nagar Industrial Area,Ghaziabad","Agrasen_Tiraha(diamond Tiraha),Ghaziabad","Kavi Nagar,Ghaziabad","Hapur_Chungi,Ghaziabad"
     ,"District Court and Session Court,Ghaziabad","RDC,Ghaziabad"],["MASURI,Ghaziabad","SunderDeep Group of Institutions,Ghaziabad","Dasna,Ghaziabad","IMS Engineering College,Ghaziabad","WaveCity,Ghaziabad","Aditya World City,Ghaziabad","Bamheta,Ghaziabad","ManipalHospital,Ghaziabad",
      "Lal Kuan,Ghaziabad","ABES Crossing,Ghaziabad","Vijay nagar,Ghaziabad","Chipyana Khrud Urf Tigri,Ghaziabad","Sector 62,Noida"]]

    for i in a :
        if (find(initial,final,i)):
            ww = find(initial,final,i)
    try:
        return ww
    except UnboundLocalError:
        return []
if __name__ == "__main__":
    print(locator("MASURI,Ghaziabad","Vijay nagar,Ghaziabad"))