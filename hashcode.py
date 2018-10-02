def hash_function(happy_list,sad_list,fear_list,love_list,angry_list):
     
    happy_hash={}
    sad_hash={}
    angry_hash={}
    love_hash={}
    fear_hash={}    

    for item in happy_list:
        if item not in happy_hash:
            happy_hash[item]=1

        else:
             happy_hash[item]+=1

        
    for item in sad_list:
        if item not in sad_hash:
            sad_hash[item]=1
        else:
            sad_hash[item]+=1

        
        
    for item in angry_list:
        if item not in angry_hash:
            angry_hash[item]=1
        else:
             angry_hash[item]+=1
   

    for item in love_list:
        if item not in love_hash:
            love_hash[item]=1
        else:
             love_hash[item]+=1

        
    for item in fear_list:
        if item not in fear_hash:
            fear_hash[item]=1
        else:
             fear_hash[item]+=1

    return happy_hash,sad_hash,fear_hash,angry_hash,love_hash



def get_final_result(city):
    temp1=happy_hash[city]
    temp2=sad_hash[city]
    temp3=angry_hash[city]
    temp4=love_hash[city]
    temp5=fear_hash[city]
    query=max(temp1,temp2,temp3,temp4,temp5)
    if temp1==query:
       return 0;

    elif temp2==query:
       return 1;

    elif temp3==query:
       return 2;

    elif temp4==query:
       return 3;
    elif temp4==query:
       return 4;



