from InstagramAPI import InstagramAPI
from getpass import getpass
import time ,datetime 

class Unfollowing :
    def __init__ (self ,username ,password) :
        self.API = InstagramAPI(username ,password)
        self.API.login()
        self.username = username
        self.username_id = self.API.username_id

    def creating_list (self):
        def TotalFollowers(page_id):
            count = 0
            followers = []
            followers_id = []
            next_max_id = True
            while next_max_id:
                if next_max_id is True:
                    next_max_id = ''
                _ = self.API.getUserFollowers(page_id, maxid=next_max_id)
                followers.extend(self.API.LastJson.get('users', []))
                next_max_id = self.API.LastJson.get('next_max_id', '')
                count += 1
                if count == 200 :
                    count = 0
                    time.sleep(120)
            for id in followers :
                followers_id.append(id['pk'])
            time.sleep(60)
            return followers_id

        def TotalFollowings(page_id):
            count = 0
            followings = []
            followings_id = []
            next_max_id = True
            while next_max_id:
                if next_max_id is True:
                    next_max_id = ''
                _ = self.API.getUserFollowings(page_id, maxid=next_max_id)
                followings.extend(self.API.LastJson.get('users', []))
                next_max_id = self.API.LastJson.get('next_max_id', '')
                count += 1
                if count == 200 :
                    count = 0
                    time.sleep(120)
            for id in followings :
                followings_id.append(id['pk'])
            time.sleep(60)
            return followings_id
        
        followers = TotalFollowers(self.username_id)
        followings = TotalFollowings(self.username_id)
        final_list = [id for id in followings if id not in followers]
        print (
            self.username , " : \n \
            Follwers : %i \n \
            Followings : %i \n" \
            %(len(followers) ,len(followings))
            )
        print ("Total Ids for Unfollowing : " ,len(final_list))
        return final_list
    
    def unfollow (self ,final_list) :
        count = 0
        print ("Total Ids for Unfollowing : " ,len(final_list))
        for id in final_list :
            try :
                isUnfollow = self.API.unfollow(id)
            except :
                time.sleep(60)
                last_error= self.API.LastJson
                print (last_error)
                continue
            if isUnfollow :
                count += 1
                time.sleep(60)
                if count == 450 :
                    print ("Instagram Daily Limit . " , datetime.datetime.now())
                    tomorrow = datetime.datetime.replace(
                                                        datetime.datetime.now() + datetime.timedelta(days=1),
                                                        hour=0, minute=0, second=0
                                                        )
                    delta = tomorrow - datetime.datetime.now()
                    time.sleep(delta.seconds)
                    print (50 * "*")
                    break
            else :
                error = self.API.LastJson
                if 'message' in error :
                    if error['message'] == "feedback_required" :
                        text = "feedback_required !! Start Again in 2 Days Later . {} \n".format(datetime.datetime.now())
                        print (text)
                        tomorrow = datetime.datetime.replace(
                                                            datetime.datetime.now() + datetime.timedelta(days=2),
                                                            hour=0, minute=0, second=0
                                                            )
                        delta = tomorrow - datetime.datetime.now()
                        time.sleep(delta.seconds+32400)
                else : 
                    print (error)


    def logout (self) :
        return self.API.logout()

def main () :
    repeat = True 
    while repeat == True :  # username , password
        username = input ("Instagram Username : ")
        password = getpass ("Instagram Password : ")
        try : 
            unfollow = Unfollowing (username ,password)
            repeat = False
        except :
            print ("Invalid Username or Password !!!")
    print ("Creating Unfollowing List ...")
    final_list = unfollow.creating_list()
    while len(final_list) != 0 :
        print (50 * "*")
        print ("Start Unfollowing at : " ,datetime.datetime.now())
        unfollow.unfollow (final_list)
        print ("Creating Unfollowing List ...")
        final_list = unfollow.creating_list()
    print ("Unfollowing Complete .")
    unfollow.logout()
    return True

if __name__ == "__main__":
    main()


