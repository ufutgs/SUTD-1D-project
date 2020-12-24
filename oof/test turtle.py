import tkinter,time ,math,os,sys
path_list = [] # player path list
player_positon = [19,19]
killer_position = [19,19]
next_position = [19,19]# player next position 
killer_path=[]
root = tkinter.Tk()
canvas = tkinter.Canvas(root,width=600,height=600) #canvas creation
canvas.configure(bg="black")
canvas.pack() #update canvas
block =[] # sight radius 
story_list=[] # story list
item_list=[] # item list 
study_book_list=[]
library_book_list=[]
extra_room_book_list=[] 
door_list={}
table_list={}
altar_list=[]
player_inventory_list=[{1:"small diary","small diary":"a small diary along with you ."}] #init the player inventory
bookstory_list=[]
locker_position=[]
faker_locker_position=[]
heading=[0,0] #heading of player 
testtime = True # boolean to check if movement is conplete
action_block=True # boolean to check if there is conservation going on 
killer_move = False
killer_rage = False
player_progess=[0,0,0,0]
altar_count=0
extra_door=[]
end_door=[]
locker_state=False
#init the map and item position
def map_reader():
    global end_door, locker_position,faker_locker_position, table_list,canvas,path_list,item_list,door_list,study_book_list,extra_room_book_list,library_book_list,extra_door
    f = open(os.path.join(os.path.dirname(__file__),"myfile.txt"),"r")
    inital_map=f.read()
    row_list = inital_map.split("\n")
    for i in range(len(row_list)):
        point_map = row_list[i].split(" ")
        for a in range(len(point_map)):
            if point_map[a] == "1":
                path_list.append([a,i])
                canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#ab9b84" , outline="#ab9b84")

            elif point_map[a] == "2":
                door_list[str(a)+","+str(i)]=canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#703e23" , outline="#703e23")
            elif point_map[a] == "3":
                locker_position.append([a,i])
                locker_position.append(canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#999997" , outline="black"))
            elif point_map[a]=="4":
                faker_locker_position.append([a,i])
                canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#999997" , outline="black")
            elif point_map[a]=="5":
                t=canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#611543" , outline="#611543")
                extra_door = [a,i]
            elif point_map[a]=="6":
                if a<19 and i<19:
                    canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#6e3100" , outline="#6e3100")
                    t=canvas.create_rectangle(303+(a-19)*10,303+(i-19)*10,307+(a-19)*10,307+(i-19)*10,fill="#ab891b" , outline="#ab891b")
                    library_book_list.append({str(a)+","+str(i):t})
                elif a>19 and i<19:
                    canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#6e3100" , outline="#6e3100")
                    t=canvas.create_rectangle(303+(a-19)*10,303+(i-19)*10,307+(a-19)*10,307+(i-19)*10,fill="#ab891b" , outline="#ab891b")
                    study_book_list.append({str(a)+","+str(i):t})
                else :
                    canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#6e3100" , outline="#6e3100")
                    t=canvas.create_rectangle(303+(a-19)*10,303+(i-19)*10,307+(a-19)*10,307+(i-19)*10,fill="#ab891b" , outline="#ab891b")
                    extra_room_book_list.append({str(a)+","+str(i):t})
            elif point_map[a]=="7":
                canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#850026" , outline="black")

                # item list
            elif point_map[a]=="8":
                canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#ab9b84" , outline="#ab9b84")
                t=canvas.create_rectangle(303+(a-19)*10,303+(i-19)*10,307+(a-19)*10,307+(i-19)*10,fill="yellow" , outline="#ab9b84")
                item_list=[{"lantern":[a,i],"position":t}]+item_list
            elif point_map[a]=="9":
                canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#6e3100" , outline="#6e3100")
                item_list.append({"old_book":[a,i],"position":canvas.create_rectangle(303+(a-19)*10,303+(i-19)*10,307+(a-19)*10,307+(i-19)*10,fill="#ab891b" , outline="#ab891b")})
            elif point_map[a]=="10":
                canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#850026" , outline="#850026")
                canvas.create_rectangle(301+(a-19)*10,301+(i-19)*10,309+(a-19)*10,309+(i-19)*10,fill="#ed2f2f" , outline="#ed2f2f")
                t=canvas.create_rectangle(302+(a-19)*10,303+(i-19)*10,304+(a-19)*10,306+(i-19)*10,fill="white" , outline="white")
                canvas.itemconfig(t,state="hidden")
                item_list.append({"silver spoon":[a,i],"position":t })
            elif point_map[a]=="11":
                canvas.create_rectangle(302+(a-19)*10,303+(i-19)*10,304+(a-19)*10,306+(i-19)*10,fill="#7a0f05" , outline="#7a0f05")
                t=canvas.create_rectangle(303+(a-19)*10,303+(i-19)*10,307+(a-19)*10,307+(i-19)*10,fill="yellow" , outline="#ab9b84")
                item_list.append({"old key":[a,i],"position":t})
            elif point_map[a]=="12":
                canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#850026" , outline="#850026")
                t=canvas.create_rectangle(303+(a-19)*10,302+(i-19)*10,307+(a-19)*10,308+(i-19)*10,fill="white" , outline="white")
                item_list.append({"scalpel":[a,i],"position":t})
            
            elif point_map[a]=="13":
                canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#6e3100" , outline="#6e3100")
                t=canvas.create_rectangle(303+(a-19)*10,303+(i-19)*10,307+(a-19)*10,307+(i-19)*10,fill="#ab891b" , outline="#ab891b")
                canvas.itemconfig(t,state="hidden")
                table_list[str(a)+","+str(i)]=t
            elif point_map[a]=="14":  
                canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#d1883f" , outline="#d1883f")
                altar_list.append({str(a)+","+str(i):0})
            elif point_map[a]=="15":
                canvas.create_rectangle(300+(a-19)*10,300+(i-19)*10,310+(a-19)*10,310+(i-19)*10,fill="#696865" , outline="#696865")
                end_door=[a,i]
                
#read the whole story.txt into story_list , bookstory.txt into bookstory_list
def story_read_file():
    global story_list,bookstory_list
    f = open(os.path.join(os.path.dirname(__file__),"story.txt"),"r", encoding='utf-8')
    story=f.read()
    story_list = story.split("@\n")
    f = open(os.path.join(os.path.dirname(__file__),"bookstory.txt"),"r", encoding='utf-8')
    story=f.read()
    bookstory_list = story.split("@\n")

#read the book (now is only the small diary sad)
def bookreader(n,b):
    global bookstory_list
    linelist = bookstory_list[n].split("#")
    a=0
    if n==0:
        for k in linelist:
            print(k+"\n")
            checkinput=False
            if a==len(linelist)-1:
                while checkinput ==False:
                    choose = input("1.end reading\nconsole:")
                    if choose =="1":
                        checkinput=True
                    else:
                        print("invalid input\n")
                checkinput=False
            else:
                while checkinput ==False:
                    choose = input("1.next page\n2.end reading\nconsole:")
                    if choose =="2":
                        return
                    elif choose=="1":
                        checkinput=True
                    else:
                        print("\ninvalid input\n")
            a+=1
    else:
        print(linelist[b])

# action when player interact with the specific item or book                   
def action(n):
    global path_list,canvas,player_inventory_list
    if n ==1:
        path_list.append(item_list[0]["lantern"])
        canvas.itemconfig(item_list[0]["position"],fill="#ab9b84")
        tmplist = {2:"lantern","lantern":"An old lantern with some ancient symbols on it."}
        player_inventory_list.append(tmplist)
    elif n==2:
        tmplist={3:"old book","old book":"A leather book. There is a note at the back of the book :'Oh boy! I was kept forgetting to bring this book back to my study, although it is just in front of the library...' "}
        player_inventory_list.append(tmplist)
    elif n==3:
        tmplist={4:"silver spoon","silver spoon":"a silver spoon with a symbol on it.It looks like royal seal."}
        player_inventory_list.append(tmplist)
    elif n==4:
        tmplist={5:"old key","old key":"An old key. It seem to be the key for the exit."}
        player_inventory_list.append(tmplist)
    elif n==5:
            tmplist={6:"scalpel","scalpel":"A brand new scalpel. You felt very fimillar, you forgot when you buy this ."}
            player_inventory_list.append(tmplist)

def killer_movement(n,k):
    global killer_rage, killer_path,killer_move,canvas,killer,player,action_block,root,killer_position,player_positon,locker_position,root,player_progess,door_list
    if n!=2 and killer_move==False:
        return
    elif n==2 and killer_move==False:
        killer_move=True
        if player_positon!=locker_position[0]:
            killer_rage=True
            calculate_path(2,0)
            root.after(10,killer_movement,0,0)
            return
    action_block=True
    x,y,x1,y1 = canvas.coords(killer)
    if k ==0:
        if n==3:
            if [killer_position[0]-1,killer_position[1]] ==[20,25]:
                killer_move=False
                killer_rage=False
                killer_path=[]
                canvas.itemconfig(killer,state="hidden")
                storyreader(8)
                return
        killer_position=[killer_position[0]+killer_path[0][0],killer_position[1]+killer_path[0][1]]
    if k<=9:
        if killer_move and len(killer_path)!=0 and player not in canvas.find_overlapping(x+0.5,y+0.5,x1-0.5,y1-0.5):
            canvas.move(killer,killer_path[0][0],killer_path[0][1])
            canvas.update()
            if player in canvas.find_overlapping(x+0.5,y+0.5,x1-0.5,y1-0.5):
                action_block=False
                killer_move=False
                root.destroy()
                print("GAME OVER")
                time.sleep(10)
                sys.exit()
            if k==9:
                root.after(1,killer_movement,n,k+1)   
            else:root.after(40,killer_movement,n,k+1)
        elif player in canvas.find_overlapping(x+0.5,y+0.5,x1-0.5,y1-0.5):
            action_block=False
            killer_move=False
            root.destroy()
            print("GAME OVER")
            time.sleep(10)
            sys.exit()
    else:
        killer_path = killer_path[1:]
        if len(killer_path)==0 and killer_rage!=True:
            canvas.itemconfig(killer,state="hidden")
            killer_move=False
            if n==1 or n==2:
                storyreader(2)
            if n==2:
                player_progess[1]=1
                return
        root.after(10,killer_movement,n,0)

def calculate_path(n, killer_next_position):
    global killer_position , player_positon,path_list,killer_path,canvas,killer,killer_rage
    if  killer_rage==False:
        canvas.move(killer,(killer_next_position[0]-killer_position[0])*10 , (killer_next_position[1]-killer_position[1])*10)
        killer_position=killer_next_position[:]
        canvas.itemconfig(killer,state="normal")
    if n==1:  
        killer_path=[[0,0]]*4
        for i in range(4):
            killer_path = [[0,1]]+killer_path
            killer_path += [[0,-1]]
        return
    elif n==2 and killer_move==False:
        killer_path+=[[0,2]]
        killer_path+=[[0,1]]
        killer_path+=[[0,0]]*4
        killer_path+=[[0,-1]]
        killer_path+=[[0,-2]]
        return
    elif n==2 and killer_move==True:
        killer_path=killer_path[:1]
    else:killer_path=killer_path[:1]
    x_diff = player_positon[0]-killer_position[0]
    y_diff = player_positon[1]-killer_position[1]  
    killer_check_position=killer_position[:]
    killer_rage=True
    while True:
        a,b=0,0
        if y_diff!=0:
            if [killer_check_position[0],killer_check_position[1]+y_diff/abs(y_diff)] in path_list :
                killer_path.append([0,y_diff/abs(y_diff)])
                killer_check_position[1]+=y_diff/abs(y_diff)
                y_diff=y_diff*((abs(y_diff)-1)/abs(y_diff))
                a=1
        elif x_diff!=0:
            if [killer_check_position[0]+x_diff/abs(x_diff),killer_check_position[1]] in path_list:
                killer_path.append([x_diff/abs(x_diff),0])
                killer_check_position[0]+=x_diff/abs(x_diff)
                x_diff=x_diff*((abs(x_diff)-1)/abs(x_diff))
                b=1
        if a==0 and b==0:
            return
#print and listen input during the story cutscene
def dead_scene(string):
    print("You put it on the {}..\n".format(string))
    time.sleep(0.5)
    print("Suddenly you realise that a blade cut through your body\n")
    print("GAME OVER")
    time.sleep(10)
    sys.exit()

def storyreader(n):
    global story_list,action_block,killer_position,killer_move,root
    action_block=False
    k = story_list[n].split("#")
    for q in k:
        if q[0]=="*":
            while True:
                userinput = input(q[1:]+"\n")
                if n==4:
                    if userinput=="2":break
                    else: dead_scene("altar")
                elif n==5:
                    if userinput=="1":break
                    else: dead_scene("table")
                elif n==6:
                    if userinput=="3":break
                    else: dead_scene("chair")
                if userinput=="y":
                    action(n)
                    break
                elif userinput=="n":return
                else:print("invalid input\n")
        elif q[0]=="&":
            tmp = q[1:].split(".")
            tmp_2 = []
            for tmp_1 in tmp[1].split(","):
                tmp_2.append(int(tmp_1))
            calculate_path(int(tmp[0]),tmp_2)
            if tmp[0]=="2":
                root.after(4500,killer_movement,2,0)
                action_block=True
                return
            else:
                killer_move=True
                killer_movement(int(tmp[0]),0)
        else:
            print(q+"\n")
        time.sleep(1)
    action_block=True

#create the pattern of light srouce
def lightblock_creation():
    color = "black"
    tmp = canvas.create_rectangle(0,0,600,290,fill=color,outline=color)
    block.append(tmp)
    tmp = canvas.create_rectangle(0,290,290,320,fill=color,outline=color)
    block.append(tmp)
    tmp = canvas.create_rectangle(0,600,600,320,fill=color,outline=color)
    block.append(tmp)
    tmp = canvas.create_rectangle(600,290,320,320,fill=color,outline=color)
    block.append(tmp)

# changing lightblock position to fit in the right place 
def lightblock_movement(x,y):
    for i in range(4):
        tmp = block[i]
        x0,y0,x1,y1 = canvas.coords(tmp)
        if i%2==0:
            if i==0:
                canvas.coords(tmp,x0,y0,x1,y1+y)
            else:
                canvas.coords(tmp,x0,y0+y,x1,y1)
        else:
            if i==1:
                canvas.coords(tmp,x0,y0+y,x1+x,y1+y)
            else:
                canvas.coords(tmp,x0+x,y0+y,x1,y1+y)

#changing player position and lightblock position 
def playermovement(x,y,n):
    global canvas,player,killer_path,killer_move,root,testtime,player_positon,next_position,killer_rage,action_block
    canvas.move(player,x,y)
    lightblock_movement(x,y)
    canvas.update()
    if n==0:
        if killer_move and killer_rage:
            killer_path.append([x,y])
    if n==9:
        player_positon = next_position[:]
        if killer_move and killer_rage==False:
            killer_rage=True
            calculate_path(0,0)
        testtime=True
        action_block=True
        return
    else:
        root.after(20,playermovement,x,y,n+1)


#check if next block player want to go is accessible or not 
def player_wall_mechanism(x,y):
    global  path_list , player_positon , next_position , testtime,killer_path ,killer_move,killer_rage
    if next_position not in path_list :
        next_position = player_positon[:]
        testtime=True
    else :
        playermovement(x,y,0)  

def Up(): 
    global testtime , next_position,heading
    heading=[0,-1]
    if testtime:
        testtime = False
        next_position[1] = next_position[1]-1
        player_wall_mechanism(0,-1)

def Down():
    global testtime , next_position,heading
    heading=[0,1]
    if testtime:
        testtime = False
        next_position[1] = next_position[1]+1
        player_wall_mechanism(0,1)

def Left():
    global testtime , next_position,heading
    heading=[-1,0]
    if testtime:
        testtime = False
        next_position[0] = next_position[0]-1
        player_wall_mechanism(-1,0)

def Right():
    global testtime , next_position,heading
    heading=[1,0]
    if testtime:
        testtime = False
        next_position[0] = next_position[0]+1
        player_wall_mechanism(1,0)



#print the inventory and listen the input 
def inventory():
    global action_block,player_inventory_list
    a=1
    action_block=False
    oof = False
    while oof == False:
        for i in player_inventory_list: 
            print(str(a)+"."+i[a])
            a+=1
        print(str(a)+".back\n")
        choose=input("console:")
        try:
            choose= int(choose)
            if choose>0 and choose<a:
                print("\n"+player_inventory_list[choose-1][player_inventory_list[choose-1][choose]]+"\n")
                if player_inventory_list[choose-1][choose]=="small diary":
                    checkinput_1 = False
                    while checkinput_1==False:
                        tmp =input("1.read it\n2.don not read it\nconsole:")
                        if tmp=="1":
                            bookreader(0,0)
                            inventory()
                            checkinput_1=True
                            oof =True
                        elif tmp=="2":
                            inventory()
                            checkinput_1=True
                            oof = True
                        else:
                            print("invalid input\n")

                else:
                    tmp =input("1.back\nconsole:")
                    if tmp == "1":
                        print("\n")
                        user=inventory()
                        if user:
                            return
            elif choose==a:
                oof=True
                action_block=True
                return True
            else:
                print("\ninvalid input !\n")
        except:
             print("\ninvalid input !\n")
        a=1

# check the position ahead the heading of player is in the itemlist or book list or other stuff . If yes, give the option , or describe wall or corridor , 
# depends on the position and heading of player      
def interact():
    global locker_state,end_door, killer_path,altar_count,altar_list,player_inventory_list,testtime,killer_rage,killer_move,player_positon,path_list,door_list,canvas,next_position,player_progess,library_book_list,study_book_list,extra_room_book_list,action_block,root,locker_position,faker_locker_position,table_list
    player_face = [player_positon[0]+heading[0],player_positon[1]+heading[1]]
    action_block=False
    #lantern
    if player_face==item_list[0]["lantern"]: 
        storyreader(1)
        player_progess[0]=1
        return
    #end door
    if player_face==end_door:
        if player_progess[3]==1:
            killer_move=False
            killer_rage=False
            action_block=False
            print("You unlock the door , with the old key ...\n")
            time.sleep(0.5)
            for i in range(len(player_inventory_list)):
                if "scalpel" in list(player_inventory_list[i].keys()):
                    storyreader(9)
                    time.sleep(1)
                    print("The end..?")
                    time.sleep(10)
                    sys.exit()
                else :
                    storyreader(10)
                    print("The end")
                    time.sleep(10)
                    sys.exit()
        else:
            print("A big door. I think this is the exit.\n")
            action_block=True
            return
    if player_face==item_list[2]["old key"]:
        player_progess[3]=1
        storyreader(9)
        return
    # scalpel
    if player_face==item_list[4]["scalpel"]:
        action(5)
        print("You take the scalpel.\n")
        action_block=True
        canvas.itemconfig(item_list[4]["scalpel"],state="hidden")
        return
        #spoon
    if player_face==item_list[3]["silver spoon"]:
        if player_progess[2]==0:
            print("A pumpkin soup. Weirdly enough, they don't serve with spoon.\n")
            action_block=True
            return
        elif player_progess[2]==1:
            print("A pumpkin soup with a silver spoon.\n")
            action_block=True
            return
        else:
            storyreader(7)
            return

    if player_face==extra_door:
        print("You see a dark red door in front of you.")
        for i in player_inventory_list:
            if "old book" in list(i.keys()):
                print("You take out the old book you took from the library.\n")
                time.sleep(0.5)
                print("the door open automatically, just like it is alive.\n")
                next_position = [player_face[0]+heading[0],player_face[1]+heading[1]]
                playermovement(heading[0]*2,heading[1]*2,0)
                return

    # if player is facing locker
    if player_face==locker_position[0] and locker_state==False:
        locker_state=True
        print("Trying to open the Locker...\n")
        canvas.tag_raise(locker_position[1])
        root.after(400,playermovement,heading[0],heading[1],0)
        next_position = player_face[:]
        action_block=True
        locker_state=False
        return
    elif player_face in faker_locker_position:
        print("You can't open this locker..\n")
        action_block=True
        return
    #altar
    for i in range(len(altar_list)):
        if str(player_face[0])+","+str(player_face[1]) in list(altar_list[i].keys()):
            if player_progess[1]==1 and player_progess[2]==0:
                if altar_list[i][str(player_face[0])+","+str(player_face[1])]==0:
                    storyreader(4+i)
                    altar_list[i][str(player_face[0])+","+str(player_face[1])]=1
                    altar_count+=1
                    if altar_count==3:
                        print("You get a silver spoon\n")
                        player_progess[2]=0.5
                        action(3)
                    return
            elif player_progess[2]>=0.5: 
                print("A table with a human skeleton.Looks very creepy.\n")
                action_block=True
                return
            else:
                print("An empty long table\n")
                action_block=True
                return

    #if player is facing interactable table
    if str(player_face[0])+","+str(player_face[1]) in list(table_list.keys()):
        if player_progess[1]==0.5:
            print("There is a table with an empty book frame\n")
            time.sleep(1)
            while True:
                user = input("Do you want to put the book on it? (y for Yes, n for No)\n")
                if user=="y":
                    if list(table_list.keys()).index(str(player_face[0])+","+str(player_face[1]))==0:
                        canvas.itemconfig(table_list[str(player_face[0])+","+str(player_face[1])],state = "normal")
                        calculate_path(0,[31,7])
                        killer_move=True
                        killer_rage=True
                        canvas.itemconfig(killer,state="normal")
                        print("....")
                        time.sleep(1)
                        print("you PUT THE WRONG PLACE \n")
                        player_inventory_list = player_inventory_list[:len(player_inventory_list)-1]
                        killer_movement(0,0)
                        action_block=True
                        player_progess[0]=0
                        return
                    else:
                        canvas.itemconfig(table_list[str(player_face[0])+","+str(player_face[1])],state = "normal")
                        player_inventory_list = player_inventory_list[:len(player_inventory_list)-1]
                        storyreader(3)
                        return
                elif user =="n":
                    print("You decide not to put the book.\n")
                    action_block=True
                    return
                else:print("invalid input! \n")
        # you survive and you go interact with the table
        elif player_progess[1]==1:
            if list(table_list.keys()).index(str(player_face[0])+","+str(player_face[1]))==1:
                print("There is the book you put\n")
                time.sleep(1)
                while True:
                    user = input("Do you want to take the book on it? (y for Yes, n for No)\n")
                    if user=="y":
                        canvas.itemconfig(table_list[str(player_face[0])+","+str(player_face[1])],state = "hidden")
                        print("You take the book \n")
                        action(2)
                        action_block=True
                        return
                    elif user =="n":
                        print("You decide not to take the book.\n")
                        action_block=True
                        return
                    else:print("invalid input! \n")
            else:
                print("An empty desk...\n")
                action_block=True
                return

    #check if this is book 
    if player_positon[0]<9 and player_positon[1]<16:
        if player_face==item_list[1]["old_book"]:
            bookreader(1,11)
            time.sleep(1)
            while True:
                user=input("Do you want to take it ? (y for Yes , n for No)\n")
                if user == "y":
                    canvas.itemconfig(item_list[1]["position"],state="hidden")
                    time.sleep(0.5)
                    print("You take the book\n")
                    action(2)
                    player_progess[1]=0.5
                    action_block=True
                    return
                elif user=="n":
                    print("You decide not to take the book\n")
                    action_block=True
                    return
                else:print("Invalid Input!")     
        for i in range(len(library_book_list)):
            if list(library_book_list[i].keys())[0]==str(player_face[0])+","+str(player_face[1]):
                if i>=11:bookreader(1,i+1)
                else:bookreader(1,i)
                if i!=9:
                    time.sleep(1)
                    while True:
                        user=input("Do you want to take it ? (y for Yes , n for No)\n")
                        if user == "y":
                            print("You take the book\n")
                            canvas.itemconfig(library_book_list[i][list(library_book_list[i].keys())[0]],state="hidden")
                            time.sleep(0.5)
                            print("You notice that the book is warping.You felt dizzy,and suddenly,you saw a unknown creature you holding,and eat your face.....")
                            time.sleep(0.5)
                            print("GAME OVER")
                            time.sleep(10)
                            sys.exit()
                        elif user=="n":
                            print("You decide not to take the book\n")
                            action_block=True
                            return
                        else:print("Invalid Input!")
                action_block=True
                return
    # study room book 
    elif player_positon[0]>19 and player_positon[1]<19:    
        for i in range(len(study_book_list)):
            if list(study_book_list[i].keys())[0]==str(player_face[0])+","+str(player_face[1]):
                if i==2 or i==3:print("An emtpy book ...\n")
                else:bookreader(2,i)
                action_block=True
                return
    elif player_positon[0]<19 and player_positon[1]>19:    
        for i in range(len(extra_room_book_list)):
            if list(study_book_list[i].keys())[0]==str(player_face[0])+","+str(player_face[1]):
                bookreader(3+i,0)
                action_block=True
                return
                  
    #check if is door 
    for i in door_list.keys():
        if i == str(player_face[0])+","+str(player_face[1]):
            if player_progess[0]==1:
                print("Opening door ...\n")
                canvas.itemconfig(door_list[i],fill="#ab9b84" ,outline="#ab9b84")
                killer_path = killer_path[:len(killer_path)-1]
                killer_path += [[0,0],[heading[0],heading[1]]*2]
                playermovement(heading[0]*2,heading[1]*2,0)
                player_positon[0]=player_positon[0]+heading[0]*2
                player_positon[1]=player_positon[1]+heading[1]*2
                next_position = player_positon[:]
                canvas.itemconfig(door_list[i],fill="#703e23" ,outline="#703e23")
            else : print("The door is locked...\n")
            action_block=True
            return
    if player_face not in path_list :print("An ancient wall , with a lot of cracks , and also smelly.\n")
    else:print("There still have space in front of me.\n")
    action_block=True
#function to bind input and function
def move(event):
    global action_block,player_inventory_list
    if action_block==False :
        pass
    elif event.char == "a":Left()
    elif event.char =="d":Right()     
    elif event.char == "w":Up()
    elif event.char =="s":Down()
    elif event.char=="e":inventory()
    elif event.char=="f":interact()


#init
map_reader()
story_read_file()
killer = canvas.create_rectangle(300,300,310,310,fill="red")
canvas.itemconfig(killer,state="hidden")
lightblock_creation()
player = canvas.create_rectangle(300,300,310,310,fill="white")
root.bind("<Key>",move)
storyreader(0)
root.mainloop()
