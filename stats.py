import facebook, requests
import sys
import json
import time


env = json.loads(open('env.json').read())

page_id = env['page_id']
at = env['page_token']
graph = facebook.GraphAPI(access_token=at)

def rs(reaction=['LIKE', 'LOVE', 'WOW', 'SAD', 'ANGRY', 'HAHA']):
    f = open(sys.path[0] + '\postids.txt', 'r')
    likes = []
    for line in f:
        objID = line.replace('\n', '')
        likes.append((graph.get_object(objID + '/reactions', limit=100))['data'])
    f.close()
    print(likes)

    ranking = {}
    for post in likes:
        for minidict in post:
            if minidict['type'] in reaction:
                userid = minidict['id']
                ranking[userid] = ranking.get(userid, 0) + 1

    ranklikes = sorted(ranking.values(), reverse=True)
    rankids = sorted(ranking, key=ranking.__getitem__, reverse=True)

    tiedscore = ranklikes[0]+1
    scorenumber = 1
    end_string = ''
    for i in range(50):
        try:
            score = ranklikes[i]
            userdict = graph.get_object(rankids[i], fields="name")
        except IndexError:
            break
        username = userdict['name']
        try:
            if score == tiedscore:
                end_string = '\n'.join([end_string, 'Tied {} - {} - {}'.format(scorenumber, score, username)])
            elif score < tiedscore:
                scorenumber = i+1
                if ranklikes[scorenumber] == ranklikes[scorenumber-1] and scorenumber < 100:
                    end_string = '\n'.join([end_string, 'Tied {} - {} - {}'.format(scorenumber, score, username)])
                else:
                    end_string = '\n'.join([end_string, '{} - {} - {}'.format(scorenumber, score, username)])
                tiedscore = score
        except IndexError:
            pass
    
