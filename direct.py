from InstagramAPI import InstagramAPI
from getpass import getpass
import time ,datetime

class Direct :
    def __init__ (self ,username ,password) :
        self.API = InstagramAPI (username ,password)
        self.API.login()
        self.username = username
        self.username_id = self.API.username_id

    def Followers(self):
        count = 0
        id_counter = 0
        followers = []
        followers_id = []
        next_max_id = True
        while next_max_id:
            if next_max_id is True:
                next_max_id = ''
            _ = self.API.getUserFollowers(self.username_id, maxid=next_max_id)
            followers.extend(self.API.LastJson.get('users', []))
            next_max_id = self.API.LastJson.get('next_max_id', '')
            count += 1
            id_counter += len(followers)
            if count == 200 :
                count = 0
                time.sleep(120)
            if id_counter == 50000 :
                break
        for id in followers :
            followers_id.append(id['pk'])
        # time.sleep(120)
        return followers_id

    def Followings(self):
        count = 0
        id_counter = 0
        followings = []
        followings_id = []
        next_max_id = True
        while next_max_id:
            if next_max_id is True:
                next_max_id = ''
            _ = self.API.getUserFollowings(self.username_id, maxid=next_max_id)
            followings.extend(self.API.LastJson.get('users', []))
            next_max_id = self.API.LastJson.get('next_max_id', '')
            count += 1
            if count == 200 :
                count = 0
                time.sleep(120)
            if id_counter == 50000 :
                break
        for id in followings :
            followings_id.append(id['pk'])
        # time.sleep(120)
        return followings_id

    def direct (self ,recipients ,counter_direct) :
        self.API.getSelfUserFeed()  # get self user max 18 posts
        selfpost = self.API.LastJson
        if len(selfpost['items'])!=0 :
            media_id = selfpost['items'][0]['id']
        else :
            print ("no post in your feed box")
            return False
        count = 0
        count_now = 0
        for recipient in recipients :
            self.API.direct_share(media_id ,recipient ,text=None)
            count += 1
            count_now += 1
            print (count_now ,end="-")
            time.sleep(600)
            if count_now >= counter_direct :
                break
            if count == 60 :
                print ("Instagram Daily Limit . " , datetime.datetime.now())
                print (50 * "*")
                tomorrow = datetime.datetime.replace(
                                                    datetime.datetime.now() + datetime.timedelta(days=1),
                                                    hour=0, minute=0, second=0
                                                    )
                delta = tomorrow - datetime.datetime.now()
                time.sleep(delta.seconds+36000)
                count = 0
        print ("Number of Direct Shares : " ,count_now)
        return count_now

    def logout (self) :
        return self.API.logout()

def main (counter_direct) :
    repeat = True 
    while repeat != False :  # username , password
        username = input ("Instagram Username : ")
        password = getpass ("Instagram Password : ")
        try : 
            direct = Direct (username ,password)
            repeat = False
        except :
            print ("Invalid Username or Password !!!")
    print ("Start Directing ...")
    Followers = direct.Followers()
    Followings = direct.Followings()
    print (len(Followers) , len(Followings))
    recipients = [id for id in Followings if id not in Followers]
    done = direct.direct(recipients ,counter_direct)
    remaining = counter_direct - done
    while remaining != 0 : 
        print ("All Recipients Direct Share Sended .Please Try Again .")
        Followers = direct.Followers()
        Followings = direct.Followings()
        recipients_old = [id for id in Followings if id not in Followers]
        recipients_new = [id for id in recipients_old if id not in recipients]
        if len(recipients_new) == 0 :
            ask = input ("No Recipients to Send Direct Share ,Repeat Again ??? [no/any]")
            if ask.lower() != "no" :
                return main(remaining)
            else :
                direct.logout()
                exit(0)
        done = direct.direct(recipients_new ,remaining)
        remaining = remaining - done
    print ("Complete .")

if __name__ == "__main__":
    counter_direct = input ("How Many Direct Shares : ")
    while not counter_direct.isnumeric() :
        print ("Please Enter A Number !")
        counter_direct = input ("How Many Direct Shares : ")
    main(counter_direct)
 
