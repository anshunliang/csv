import sys,csv
rows=[]
p=0
with open('C:\\Users\\lh\Desktop\\1.csv','r') as f:
    for i in f:
        p=p+1
        rows.append(i.split(','))
        if p>10000:
            print(sys.getsizeof(rows))
            with open("C:\\Users\\lh\Desktop\\22.csv","a+",newline='') as csvfile:
                writer = csv.writer(csvfile)
                #写入多行用writerows
                for i in range(len(rows)):
                    if i%3==0:
                        writer.writerows([rows[i]])
                rows.clear()
                p=0
    with open("C:\\Users\\lh\Desktop\\22.csv","a+",newline='') as csvfile:
            writer = csv.writer(csvfile)
            for i in range(len(rows)):
                    if i%3==0:
                        writer.writerows([rows[i]])
        
    rows.clear()
        
        



