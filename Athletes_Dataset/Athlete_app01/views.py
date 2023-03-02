from django.shortcuts import render
import pymysql
from django.shortcuts import render,HttpResponse
from Athlete_app01 import models
from pymysql import cursors
import numpy as np
import matplotlib.pyplot as plt
import os
from pyrebase import pyrebase
import requests
# from pyspark import SparkContext,SparkConf,SQLContext
# import pyrebase
module_dir = os.path.dirname(__file__)
img_folder = os.path.join(module_dir, './static/img')
config = {
        'apiKey': "AIzaSyD9czrjBtKsISm3Aq4GDhPQNFos9kIkeHY",
        'authDomain': "group-47a89.firebaseapp.com",
        'databaseURL': "https://group-47a89-default-rtdb.firebaseio.com",
        'projectId': "group-47a89",
        'storageBucket': "group-47a89.appspot.com",
        'messagingSenderId': "96044158076",
        'appId': "1:96044158076:web:60adf913dd198cd8a60df9",
        'measurementId': "G-4EZGB1NCPS"
    }
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

# Create your views here.
def index(request):
    return HttpResponse('Welcome')
    # return redirect('https://wwww.baidu.com')
def tryexample01(request):
    name = 'Mardy'
    job = [['Mardy','Group30','Django'],['Jamie','Group31','MySQL']]

    #app=>templates=>html 根据app注册顺序找html
    if request.method == "GET":
        return render(request, "tryexample01.html", {'n1': name, 'n2': job})
    else:
        # selection = request.GET# getm method传过来的参数
        selection = request.POST  # ?????如何接收??????
        return render(request,"tryexample01.html", {'n1': name, 'n2': job, 'n3': selection})
def orm(request):
    # 1.insert data:
    #models.userInfo.objects.create(name='Mardy',password='123',age=24)
    #models.Soccer_club.objects.create(Club_ID = 0,Club = "Free Agents",Club_alias = "FA")
    #models.Soccer_athlete.objects.create(Athlete_ID=389,Name="Cristiano Ronaldo",Nationality="Portugal",Continent="Europe",Birthday="1985-02-05",National_Position="LS",National_Kit=7.0,Rating=94,Continent_num=3.0)


    # 2.delete:
    #models.SoccerClub.objects.filter(id=3).delete()
    #models.SoccerClub.objects.all().delete() # delete all

    # 3.select:
    #data_list = models.Soccer_club.objects.all() #queryset type

    # 4.update:
    #models.Soccer_affiliation.objects.filter(Player_ID=9999999999).update(Club_ID=11111111111)

    # test:
    #data_list = models.Soccer_affiliation.objects.all()
    data_list = models.Soccer_club.objects.all()#.first()
    for obj in data_list:
        print(obj.Club_ID)
    return HttpResponse('successful!')

# pages for project:
def mainpage_soccer(request):
    table_content = models.Soccer_club.objects.all()
    connect = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset='utf8', db='athletes_new')
    cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)
    table_col = ['Name', 'Nationality', 'Continent', 'Birthday', 'National_Position', 'National_Kit',
                 'Rating']
    sql = "select * from Athlete_app01_Soccer_athlete"
    cursor.execute(sql)
    data_list = cursor.fetchall()
    rows = [[i,
             data_list[i]['Name'],
             data_list[i]['Nationality'],
             data_list[i]['Continent'],
             data_list[i]['Birthday'],
             data_list[i]['National_Position'],
             data_list[i]['National_Kit'],
             data_list[i]['Rating']] for i in range(len(data_list))]

    if request.method == "GET":
        pass
        #return render(request, 'mainpage_soccer.html',{'table_col':table_col, 'table_body':rows})
    else:
        post_receive = request.POST
        table_name = post_receive['SoccerTable_selection']
        if table_name == 'Soccer_club':
            table_col = ['Club','Club_alias']
            sql = "select * from Athlete_app01_Soccer_club"
            cursor.execute(sql)
            data_list = cursor.fetchall()
            rows = [[data_list[i]['Club_ID'],
                     data_list[i]['Club'],
                     data_list[i]['Club_alias']] for i in range(len(data_list))]
        if table_name == 'Soccer_contract':
            table_col = ['Club_Joining','Contract_Expiry']
            sql = "select * from Athlete_app01_Soccer_contract"
            cursor.execute(sql)
            data_list = cursor.fetchall()
            rows = [[i,
                     data_list[i]['Club_Joining'],
                     data_list[i]['Contract_Expiry']] for i in range(len(data_list))]
        if table_name == 'Soccer_affiliation':
            table_col = ['Athlete_ID','Club_ID','Contract_ID','Club_Position','Club_Kit']
            sql = "select * from Athlete_app01_Soccer_affiliation"
            cursor.execute(sql)
            data_list = cursor.fetchall()
            rows = [[i, data_list[i]['pl_id'],
                     data_list[i]['cl_id'],
                     data_list[i]['co_id'],
                     data_list[i]['Club_Position'],
                     data_list[i]['Club_Kit']] for i in range(len(data_list))]
        print(post_receive)
    rows = rows[:30]
    return render(request,'mainpage_soccer.html',{'table_col':table_col, 'table_body':rows})

def tennis_page(request):
    table_col = ['PlayerID', 'Name', 'Gender', 'ELO', 'Peak Match', 'Peak Age', 'Peak ELO','Rank']
    tennisplayersdata = models.Tennis_athlete.objects.all()
    rows = []
    i = 0
    for row in tennisplayersdata:
        PlayerID = row.TennisPlayer_ID
        Name = row.Player
        Gender = row.Gender
        ELO = row.Elo
        Peak_Match = row.Peak_Match
        Peak_Age = row.Peak_Age
        Peak_ELO = row.Peak_Elo
        Rank = row.Tennis_rank
        rows.append([i,PlayerID,Name,Gender,ELO,Peak_Match,Peak_Age,Peak_ELO,Rank])
        i+=1
    if request.method == 'GET':
        return render(request,'tennis_page.html',{'table_col':table_col, 'table_body':rows})
    else:
        TennisTable_selection = request.POST['TennisTable_selection']
        if TennisTable_selection == 'Tennis_Hard':
            table_col = ['PlayerID','HardRaw','Hard_Court_ELO_Rating']
            tennisplayersdata = models.Tennis_hard.objects.all()
            i = 0
            rows = []
            for row in tennisplayersdata:
                PlayerID = row.t_id
                Hard_Raw = row.HardRaw
                Hard_Court_ELO_Rating = row.Hard_Court_Elo_Rating
                rows.append([i, PlayerID, Hard_Raw, Hard_Court_ELO_Rating])
                i+=1
        if TennisTable_selection == 'Tennis_Grass':
            table_col = ['PlayerID','GrassRaw','Grass_Court_ELO_Rating']
            tennisplayersdata = models.Tennis_grass.objects.all()
            i = 0
            rows=[]
            for row in tennisplayersdata:
                PlayerID = row.t_id
                Grass_Raw = row.GrassRaw
                Grass_Court_ELO_Rating = row.Grass_Court_Elo_Rating
                rows.append([i, PlayerID, Grass_Raw, Grass_Court_ELO_Rating])
                i+=1
        if TennisTable_selection == 'Tennis_Clay':
            table_col = ['PlayerID','ClayRaw','Clay_Court_ELO_Rating']
            tennisplayersdata = models.Tennis_clay.objects.all()
            i = 0
            rows = []
            for row in tennisplayersdata:
                PlayerID = row.t_id
                Clay_Raw = row.ClayRaw
                Clay_Court_ELO_Rating = row.Clay_Court_Elo_Rating
                rows.append([i, PlayerID, Clay_Raw, Clay_Court_ELO_Rating])
                i+=1
        return render(request, 'tennis_page.html', {'table_col': table_col, 'table_body': rows})

    #
    # tableSelection = request.POST['tableSelection']
    # data_dict = {'Name__contains': searchByName}  # Name__contains = 'input athlete's name'
    # allSelectedAthletes = models.Soccer_athlete.objects.filter(**data_dict)
    # search_row = []
    # # rows = [[i,
    # #          data_list[i]['Name'],
    # #          data_list[i]['Nationality'],
    # #          data_list[i]['Continent'],
    # #          data_list[i]['Birthday'],
    # #          data_list[i]['National_Position'],
    # #          data_list[i]['National_Kit'],
    # #          data_list[i]['Rating']] for i in range(len(data_list))]
    #
    # return render(request,'tennis_page.html')

def nba_page(request):
    # if request == 'GET':
    rows = []
    table_col = ['Name', 'Age', 'Team', 'Games', 'Rank']
    for i in range(30):#2728
        rowID = database.child('NBA').child(i).child('ID').get().val()
        rowAge = database.child('NBA').child(i).child('Age').get().val()
        # row2pfg = database.child('NBA').child(i).child('2-points Field Goal').get().val()
        # row2pfga = database.child('NBA').child(i).child('2-points Field Goal Attempted').get().val()
        # row3pfg = database.child('NBA').child(i).child('3-points Field Goal').get().val()
        # row3pfga = database.child('NBA').child(i).child('3-points Field Goal Attempted').get().val()
        # rowAssists = database.child('NBA').child(i).child('Assists').get().val()
        # rowBlock = database.child('NBA').child(i).child('Block').get().val()
        # rowDR = database.child('NBA').child(i).child('Defensive Rebounds').get().val()
        # rowFG = database.child('NBA').child(i).child('Fields Goal').get().val()
        # rowFGA = database.child('NBA').child(i).child('Fields Goal Attempted').get().val()
        # rowFT = database.child('NBA').child(i).child('Free Throws').get().val()
        # rowFTA = database.child('NBA').child(i).child('Free Throws Attempted').get().val()
        rowGames = database.child('NBA').child(i).child('Games').get().val()
        # rowMP = database.child('NBA').child(i).child('Minutes Played').get().val()
        # rowOR = database.child('NBA').child(i).child('Offensive Rebounds').get().val()
        # rowPF = database.child('NBA').child(i).child('Personal Fouls').get().val()
        rowPlayer = database.child('NBA').child(i).child('Player').get().val()
        # rowPoints = database.child('NBA').child(i).child('Points').get().val()
        # rowPos = database.child('NBA').child(i).child('Pos').get().val()
        rowRank = database.child('NBA').child(i).child('Rank').get().val()
        # rowSteals = database.child('NBA').child(i).child('Steals').get().val()
        rowTeam = database.child('NBA').child(i).child('Team').get().val()
        # rowTR = database.child('NBA').child(i).child('Total Rebounds').get().val()
        # rowTurnovers = database.child('NBA').child(i).child('Turnovers').get().val()
        # rowYear = database.child('NBA').child(i).child('Year').get().val()
        rows.append([rowID, rowPlayer, rowAge, rowTeam, rowGames, rowRank])
    return render(request,'nba_page.html',{'table_col':table_col,'table_body':rows[:30]})

def nfl_page(request):
    return render(request,'nfl_page.html')
def search_soccer_page(request):
    table_col = ['Name', 'Club', 'Contract_ID', 'Reactions', 'Composure', 'Short Pass', 'Vision', 'Longpass', 'Rating']
    rows = []
    returnprint =''
    dplayerid = np.nan
    if request.method == 'GET':
        return render(request, 'search_soccer_page.html')
    else:
        post_receive = request.POST
        searchByName = post_receive['searchByName']
        searchByClub = post_receive['searchByClub']
        checkDistribution = post_receive['checkDistribution']
        # print('####',checkDistribution)
        if searchByName:
            if searchByClub:
                print('no')
            else:
                data_dict = {'Name__contains': searchByName}  # Name__contains = 'input athlete's name'
                allSelectedAthletes = models.Soccer_athlete.objects.filter(**data_dict)
                search_row = []
                i = 0
                allSelectedPlayerid = []
                print(allSelectedAthletes)
                for player in allSelectedAthletes:
                    # print(player.Name)
                    playerid = player.id
                    allSelectedPlayerid.append(playerid)
                    playername = player.Name
                    if models.Soccer_affiliation.objects.filter(pl_id=int(playerid)):
                        affiliation_res = models.Soccer_affiliation.objects.filter(pl_id=int(playerid))[0]
                        clubid = affiliation_res.cl_id
                        contractid = affiliation_res.co_id
                        reactions = affiliation_res.Reactions#round(affiliation_res.Reactions - 61.769545687155286, 2)
                        composure = affiliation_res.Composure#round(affiliation_res.Composure - 55.85176550861432, 2)
                        shortpass = affiliation_res.Short_Pass#round(affiliation_res.Short_Pass - 58.119690680616365, 2)
                        vision = affiliation_res.Vision#round(affiliation_res.Vision - 52.706544606811846, 2)
                        longpass = affiliation_res.Long_Pass#round(affiliation_res.Long_Pass - 52.39563313811338, 2)
                        rating = models.Soccer_athlete.objects.filter(id = playerid)[0].Rating

                        if models.Soccer_club.objects.filter(Club_ID=clubid):
                            clubname = models.Soccer_club.objects.filter(Club_ID=clubid)[0].Club
                        else:
                            clubname = np.nan
                        scoresForPlayer = models.Soccer_affiliation.objects.filter(pl_id=int(playerid))[0]
                    else:
                        clubname = np.nan
                        contractid = np.nan
                        scoresForPlayer = np.nan
                        reactions = 0
                        composure = 0
                        shortpass =0
                        vision = 0
                        longpass = 0
                        rating = models.Soccer_athlete.objects.filter(id=playerid)[0].Rating
                    # important features for soccer are ['Reactions', 'Composure', 'Short_Pass', 'Vision', 'Long_Pass']

                    search_row.append([playerid, playername, clubname, contractid, reactions, composure, shortpass, vision, longpass,rating])
                    i += 1
                rows = search_row
        else:
            if searchByClub:
                data_dict = {'Club__contains': searchByClub}  # Name__contains = 'input athlete's name'
                allSelectedClubs = models.Soccer_club.objects.filter(**data_dict)
                search_row = []
                i = 0
                # print(allSelectedClubs[0].Club_ID)
                for club in allSelectedClubs:
                    clubid = club.Club_ID
                    allSelectedPlayersInClub = models.Soccer_affiliation.objects.filter(cl_id=clubid)
                    for player in allSelectedPlayersInClub:
                        playerid = player.pl_id
                        playername = models.Soccer_athlete.objects.filter(id=playerid)[0].Name
                        if models.Soccer_affiliation.objects.filter(pl_id=int(playerid)):
                            affiliation_res = models.Soccer_affiliation.objects.filter(pl_id=int(playerid))[0]
                            contractid = affiliation_res.co_id
                            reactions = affiliation_res.Reactions  # round(affiliation_res.Reactions - 61.769545687155286, 2)
                            composure = affiliation_res.Composure  # round(affiliation_res.Composure - 55.85176550861432, 2)
                            shortpass = affiliation_res.Short_Pass  # round(affiliation_res.Short_Pass - 58.119690680616365, 2)
                            vision = affiliation_res.Vision  # round(affiliation_res.Vision - 52.706544606811846, 2)
                            longpass = affiliation_res.Long_Pass  # round(affiliation_res.Long_Pass - 52.39563313811338, 2)
                            rating = models.Soccer_athlete.objects.filter(id=playerid)[0].Rating

                            if models.Soccer_club.objects.filter(Club_ID=clubid):
                                clubname = models.Soccer_club.objects.filter(Club_ID=clubid)[0].Club
                            else:
                                clubname = np.nan
                            scoresForPlayer = models.Soccer_affiliation.objects.filter(pl_id=int(playerid))[0]
                        else:
                            clubname = np.nan
                            contractid = np.nan
                            scoresForPlayer = np.nan
                            reactions = np.nan
                            composure = np.nan
                            shortpass = np.nan
                            vision = np.nan
                            longpass = np.nan
                            rating = models.Soccer_athlete.objects.filter(id=playerid)[0].Rating
                        # important features for soccer are ['Reactions', 'Composure', 'Short_Pass', 'Vision', 'Long_Pass']

                        search_row.append(
                            [playerid, playername, clubname, contractid, reactions, composure, shortpass, vision, longpass, rating])
                        i += 1
                    rows = search_row
        if checkDistribution:
            dplayerid = checkDistribution
            dplayername = models.Soccer_athlete.objects.filter(id=checkDistribution)[0].Name
            if models.Soccer_affiliation.objects.filter(pl_id=int(dplayerid)):
                affiliation_res = models.Soccer_affiliation.objects.filter(pl_id=int(dplayerid))[0]
                reactions = affiliation_res.Reactions  # round(affiliation_res.Reactions - 61.769545687155286, 2)
                composure = affiliation_res.Composure  # round(affiliation_res.Composure - 55.85176550861432, 2)
                shortpass = affiliation_res.Short_Pass  # round(affiliation_res.Short_Pass - 58.119690680616365, 2)
                vision = affiliation_res.Vision  # round(affiliation_res.Vision - 52.706544606811846, 2)
                longpass = affiliation_res.Long_Pass  # round(affiliation_res.Long_Pass - 52.39563313811338, 2)

            else:
                reactions = np.nan
                composure = np.nan
                shortpass = np.nan
                vision = np.nan
                longpass = np.nan

            yReactions = [i.Reactions for i in models.Soccer_affiliation.objects.all()]
            yComposure = [i.Composure for i in models.Soccer_affiliation.objects.all()]
            yShortpass = [i.Short_Pass for i in models.Soccer_affiliation.objects.all()]
            yVision = [i.Vision for i in models.Soccer_affiliation.objects.all()]
            yLongpass = [i.Long_Pass for i in models.Soccer_affiliation.objects.all()]
            fig = plt.figure(figsize=(15, 10))
            ax1 = fig.add_subplot(2, 3, 1)
            ax2 = fig.add_subplot(2, 3, 2)
            ax3 = fig.add_subplot(2, 3, 3)
            ax4 = fig.add_subplot(2, 3, 4)
            ax5 = fig.add_subplot(2, 3, 5)
            axlst = [ax1,ax2,ax3,ax4,ax5]
            colorlst=['coral','darkorange','limegreen','dodgerblue','darkviolet']
            allvaluelst = [yReactions,yComposure,yShortpass,yVision,yLongpass]
            valuelst = [reactions,composure,shortpass,vision,longpass]
            valuenamelst = ['Reactions','Composure','Short pass','Vision','Long pass']
            for aa in range(5):
                axlst[aa].hist(allvaluelst[aa], color=colorlst[aa])
                axlst[aa].axvline(valuelst[aa])
                axlst[aa].grid(True)
                axlst[aa].legend(loc=0)
                axlst[aa].set_xlabel('Value')
                axlst[aa].set_ylabel(valuenamelst[aa])
                axlst[aa].set_title(f'{dplayername}')
            plt.savefig(f'{img_folder}/soccer_{dplayerid}.png')
            returnprint = 'pictures'

        return render(request, 'search_soccer_page.html', {'table_col':table_col, 'table_body':rows, 'returnprint':returnprint, 'returnpicture':f"img/soccer_{dplayerid}.png"})
        # return HttpResponse('Welcome')

def search_tennis_page(request):
    import os
    module_dir = os.path.dirname(__file__)
    img_folder = os.path.join(module_dir, './static/img')
    if request.method == 'GET':
        return render(request,'search_tennis_page.html')
    else:
        post_receive = request.POST
        searchByName = post_receive['searchByName']
        searchByPlayerID = post_receive['searchByPlayerID']
        if searchByName:
            if searchByPlayerID:
                return HttpResponse('Only allowed to search by one search box')
            else:
                allnames = models.Tennis_athlete.objects.filter(Player__contains = searchByName)
                n = 0
                for i in allnames:
                    n+=1
                if n != 0:
                    returnprint = 'Need to type correct name!'
                    return render(request,'search_tennis_page.html',{'returnprint':returnprint})

                else:
                    player = models.Tennis_athlete.objects.filter(Player = searchByName)[0]
                    playerid = player.TennisPlayer_ID
                    HardELORating = models.Tennis_hard.objects.filter(id=playerid)[0].Hard_Court_Elo_Rating
                    GrassELORating = models.Tennis_grass.objects.filter(id=playerid)[0].Grass_Court_Elo_Rating
                    ClayELORating = models.Tennis_clay.objects.filter(id=playerid)[0].Clay_Court_Elo_Rating
                    yHard = [i.Hard_Court_Elo_Rating for i in models.Tennis_hard.objects.all()]
                    yGrass = [i.Grass_Court_Elo_Rating for i in models.Tennis_grass.objects.all()]
                    yClay = [i.Clay_Court_Elo_Rating for i in models.Tennis_clay.objects.all()]
                    fig = plt.figure(figsize=(15,6))
                    ax1 = fig.add_subplot(1, 3, 1)
                    ax2 = fig.add_subplot(1, 3, 2)
                    ax3 = fig.add_subplot(1, 3, 3)
                    ax1.hist(yHard, color = 'coral')
                    ax1.axvline(HardELORating)
                    ax1.grid(True)
                    ax1.legend(loc=0)
                    ax1.set_xlabel('Value')
                    ax1.set_ylabel('ELO')
                    ax1.set_title('Hard Raw')
                    # ax1.savefig(f'{img_folder}/{playerid}_hard.png')

                    ax2.hist(yGrass, color = 'limegreen')
                    ax2.axvline(GrassELORating)
                    ax2.grid(True)
                    ax2.legend(loc=0)
                    ax2.set_xlabel('Value')
                    ax2.set_ylabel('ELO')
                    ax2.set_title('Grass Raw')
                    # ax2.savefig(f'{img_folder}/{playerid}_grass.png')

                    ax3.hist(yClay, color = 'cornflowerblue')
                    ax3.axvline(ClayELORating)
                    ax3.grid(True)
                    ax3.legend(loc=0)
                    ax3.set_xlabel('Value')
                    ax3.set_ylabel('ELO')
                    ax3.set_title('Clay Raw')
                    # ax3.savefig(f'{img_folder}/{playerid}_clay.png')
                    plt.savefig(f'{img_folder}/{playerid}.png')

                    returnprint = 'pictures'
                    return render(request,'search_tennis_page.html',{'returnprint':returnprint,'returnpicture':f"img/{playerid}.png"})
                    # return HttpResponse('Welcome')
        else:
            if not searchByPlayerID:
                return HttpResponse('Search box should not be empty')
            else:
                if not models.Tennis_athlete.objects.filter(TennisPlayer_ID=searchByPlayerID):
                    returnprint = 'id need to be less than 783!'
                    return render(request, 'search_tennis_page.html', {'returnprint': returnprint})
                else:
                    playerid = models.Tennis_athlete.objects.filter(TennisPlayer_ID=searchByPlayerID)[0].TennisPlayer_ID
                    returnprint = 'pictures'
                    HardELORating = models.Tennis_hard.objects.filter(id=playerid)[0].Hard_Court_Elo_Rating
                    GrassELORating = models.Tennis_grass.objects.filter(id=playerid)[0].Grass_Court_Elo_Rating
                    ClayELORating = models.Tennis_clay.objects.filter(id=playerid)[0].Clay_Court_Elo_Rating
                    yHard = [i.Hard_Court_Elo_Rating for i in models.Tennis_hard.objects.all()]
                    yGrass = [i.Grass_Court_Elo_Rating for i in models.Tennis_grass.objects.all()]
                    yClay = [i.Clay_Court_Elo_Rating for i in models.Tennis_clay.objects.all()]
                    fig = plt.figure(figsize=(15, 6))
                    ax1 = fig.add_subplot(1, 3, 1)
                    ax2 = fig.add_subplot(1, 3, 2)
                    ax3 = fig.add_subplot(1, 3, 3)
                    ax1.hist(yHard, color='coral')
                    ax1.axvline(HardELORating)
                    ax1.grid(True)
                    ax1.legend(loc=0)
                    ax1.set_xlabel('Value')
                    ax1.set_ylabel('ELO')
                    ax1.set_title('Hard Raw')
                    import os
                    module_dir = os.path.dirname(__file__)
                    img_folder = os.path.join(module_dir, './static/img')
                    # ax1.savefig(f'{img_folder}/{playerid}_hard.png')

                    ax2.hist(yGrass, color='limegreen')
                    ax2.axvline(GrassELORating)
                    ax2.grid(True)
                    ax2.legend(loc=0)
                    ax2.set_xlabel('Value')
                    ax2.set_ylabel('ELO')
                    ax2.set_title('Grass Raw')
                    # ax2.savefig(f'{img_folder}/{playerid}_grass.png')

                    ax3.hist(yClay, color='cornflowerblue')
                    ax3.axvline(ClayELORating)
                    ax3.grid(True)
                    ax3.legend(loc=0)
                    ax3.set_xlabel('Value')
                    ax3.set_ylabel('ELO')
                    ax3.set_title('Clay Raw')
                    # ax3.savefig(f'{img_folder}/{playerid}_clay.png')
                    plt.savefig(f'{img_folder}/{playerid}.png')

                    return render(request,'search_tennis_page.html',{'returnprint':returnprint,'returnpicture':f"img/{playerid}.png"})

def search_nba_page(request):
    if request.method =='POST':
        requestres = request.POST
        searchByName = requestres['searchByName']
        searchByTeam = requestres['searchByTeam']
        searchByCode = requestres['searchByCode']
        returnprint = ''
        print(requestres)
        if searchByTeam and (not searchByName and not searchByCode):
            r = requests.get(
                f'https://group-47a89-default-rtdb.firebaseio.com/NBA.json?orderBy="Team"&equalTo="{searchByTeam}"')
            rows = []
            table_col = ['Name', 'Age', 'Team', 'Games', 'Rank']
            for i in list(r.json().keys()):  # 2728
                rowID = database.child('NBA').child(i).child('ID').get().val()
                rowAge = database.child('NBA').child(i).child('Age').get().val()
                rowGames = database.child('NBA').child(i).child('Games').get().val()
                rowPlayer = database.child('NBA').child(i).child('Player').get().val()
                rowRank = database.child('NBA').child(i).child('Rank').get().val()
                rowTeam = database.child('NBA').child(i).child('Team').get().val()
                rows.append([rowID, rowPlayer, rowAge, rowTeam, rowGames, rowRank])
            returnprint = 'table'

            return render(request,'search_nba_page.html',{'returnprint':returnprint,'table_col':table_col,'table_body':rows})
        if searchByName and (not searchByTeam and not searchByCode):
            #ID and Name =>picture
            rows = []
            table_col = ['Name', 'Team','Fields Goal', 'Fields Goal Attempted', '3-points Field Goal', '2-points Field Goal Attempted','Free Throws','Rank','Year']
            r = requests.get(f'https://group-47a89-default-rtdb.firebaseio.com/NBA.json?orderBy="Player"&equalTo="{searchByName}"')
            for i in list(r.json().keys()):
                ID = database.child('NBA').child(i).child('ID').get().val()
                Player = database.child('NBA').child(i).child('Player').get().val()
                Team = database.child('NBA').child(i).child('Team').get().val()
                FG = database.child('NBA').child(i).child('Fields Goal').get().val()
                FGA = database.child('NBA').child(i).child('Fields Goal Attempted').get().val()
                pfg3 = database.child('NBA').child(i).child('3-points Field Goal').get().val()
                pfga2 = database.child('NBA').child(i).child('2-points Field Goal Attempted').get().val()
                FT = database.child('NBA').child(i).child('Free Throws').get().val()
                Rank = database.child('NBA').child(i).child('Rank').get().val()
                Year = database.child('NBA').child(i).child('Year').get().val()
                rows.append([ID, Player, Team, FG, FGA, pfg3, pfga2,FT,Rank,Year])
            returnprint = 'table'
            return render(request, 'search_nba_page.html',
                          {'returnprint': returnprint, 'table_col': table_col, 'table_body': rows})


            # return HttpResponse('A')
        if searchByCode and (not searchByTeam and not searchByName):
            feature = searchByCode.split('=')[0]
            value = searchByCode.split('=')[1]
            r = requests.get(
                f'https://group-47a89-default-rtdb.firebaseio.com/NBA.json?orderBy="{feature}"&equalTo="{value}"')
            rows = []
            table_col = ['Name', 'Age', 'Team', 'Games', 'Rank']
            for i in list(r.json().keys()):  # 2728
                rowID = database.child('NBA').child(i).child('ID').get().val()
                rowAge = database.child('NBA').child(i).child('Age').get().val()
                rowGames = database.child('NBA').child(i).child('Games').get().val()
                rowPlayer = database.child('NBA').child(i).child('Player').get().val()
                rowRank = database.child('NBA').child(i).child('Rank').get().val()
                rowTeam = database.child('NBA').child(i).child('Team').get().val()
                rows.append([rowID, rowPlayer, rowAge, rowTeam, rowGames, rowRank])
            returnprint = 'table'
            return render(request, 'search_nba_page.html',
                          {'returnprint': returnprint, 'table_col': table_col, 'table_body': rows})
        else:
            return HttpResponse('You can only check in one search box')
    return render(request,'search_nba_page.html')

def search_nfl_page(request):
    return render('search_nfl_page.html')

# db3 = boto3.resource('dynamodb',
#                      aws_secret_access_key='hY5mEvmLARSu+rRdJ/jhefw3U7xjk8DpF02DbWDF',
#                      aws_access_key_id='AKIA4GIDTGJLI27Q56QC',
#                      region_name='us-west-1')
# table = db3.Table('NFL_551')
# response = table.get_item( Key = {'ID': '1'})
# print(response['Item'])
#
