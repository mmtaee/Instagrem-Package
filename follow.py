from InstagramAPI import InstagramAPI
from getpass import getpass
import time ,datetime ,requests ,os

log_file = ""

class Following :
    def __init__ (self ,username ,password) :
        self.API = InstagramAPI(username ,password) 
        self.API.login()
        self.username = username
        self.username_id = self.API.username_id
        log = os.getcwd() + "/{}.txt".format(self.username)
        if not os.path.exists(log) :
            os.mknod(log)
        global log_file
        log_file = log

    def is_public(self ,page) :
        self.API.searchUsername(page)
        info = self.API.LastJson["user"]
        if info["is_private"] == False :
            return True
        elif info["is_private"] == True and info["is_favorite"] == True :
            return True
        else :
            return False
        
    def create_following_list (self ,page_list) :
        global log_file
        # pages Followers set : 
        pages_id = []
        for pagename in page_list :
            self.API.searchUsername(pagename)
            find_all_infos = self.API.LastJson
            if find_all_infos['user']['is_private'] == False :
                pages_id.append(find_all_infos["user"]["pk"])
            time.sleep(40)
            
        def TotalFollowers(page_id):
            count = 0
            id_counter = 0
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
                id_counter += len(followers)
                if count == 200 :
                    count = 0
                    time.sleep(120)
                if id_counter == 2*10**5 :
                    break
            for id in followers :
                followers_id.append(id['pk'])
            time.sleep(120)
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
            time.sleep(120)
            return followings_id

        final_followers = set()
        for page_id in pages_id :
            Followers = TotalFollowers(page_id)
            text = str(page_id) + "-- Followers ids : {} \n".format(len(Followers))
            with open (log_file ,"a") as file :
                file.write(text)
            print (text)
            {final_followers.add(id) for id in Followers}
        text = "Total Followers from Pages : {} \n".format(len(final_followers))
        with open (log_file ,"a") as file :
            file.write(text)
        print (text)
        # self followers - Followings set :
        print ("Creating List of  %s  (Followers and Followings) ."%self.username)
        selfFollowers = TotalFollowers(self.username_id)
        selfFollowings = TotalFollowings(self.username_id)
        selffinal_ids = list (dict.fromkeys(selfFollowers + selfFollowings))
        text = self.username + " : \n Follwers : {} \n Followings : {} \n Total Without Duplicate : {} \n" \
            .format(len(selfFollowers) ,len(selfFollowings) ,len(selffinal_ids))
        with open (log_file ,"a") as file :
            file.write(text)
        print (text)
        final_ids = {id for id in final_followers if id not in selffinal_ids}
        return final_ids

    def follow (self ,final_list ,follower_add) :
        global log_file
        def info () :
            self.API.searchUsername(self.username)
            find = self.API.LastJson
            info = []
            info.append (int(find['user']['follower_count']))
            info.append (int(find['user']['following_count']))
            return info
        follower , following = info()
        text = "Before Starting : \n Follower : {} \n Following : {} \n".format(follower ,following)
        with open (log_file ,"a") as file :
            file.write(text)
        print (text)
        follower_max = follower + follower_add
        count = 0
        for id in final_list :
            isfollow = self.API.follow(id)
            if isfollow :
                count += 1
                time.sleep(60)
                if count == 450 :
                    follower_now , following_now = info()
                    if follower_max != follower_now :
                        text = "At {} : \n Follower : {} \n Following : {}"\
                            .format(datetime.datetime.now() ,follower_now ,following_now) + "\n"
                        text = text + "Adding Result : \n Follower : {} \n Following : {}"\
                            .format((follower_now - follower) , (following_now - following))  + 50 * "*" + "\n"
                        with open (log_file ,"a") as file :
                            file.write(text)
                        print (text)
                        tomorrow = datetime.datetime.replace(
                                                            datetime.datetime.now() + datetime.timedelta(days=1),
                                                            hour=0, minute=0, second=0
                                                            )
                        delta = tomorrow - datetime.datetime.now()
                        time.sleep(delta.seconds+32400)
                        count = 0
                    else :
                        def follower_id1():
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
                                if id_counter == 2*10**5 :
                                    break
                            for id in followers :
                                followers_id.append(id['pk'])
                            time.sleep(120)
                            return followers_id
                        count_id = 0
                        new1 = follower_id1()   
                        for id in new1 :
                            if id in final_list :
                                count_id += 1
                        text = "Followers Added With Ids : {} \n".format(count_id) + "Finished ." 
                        with open (log_file ,"a") as file :
                            file.write(text)
                        print (text)
                        return True
            else :
                error = self.API.LastJson
                if 'message' in error :
                    if error['message'] == "feedback_required" :
                        text = "feedback_required !! Start Again in 2 Days Later . {} \n".format(datetime.datetime.now())
                        with open (log_file ,"a") as file :
                            file.write(text)
                        tomorrow = datetime.datetime.replace(
                                                            datetime.datetime.now() + datetime.timedelta(days=2),
                                                            hour=0, minute=0, second=0
                                                            )
                        delta = tomorrow - datetime.datetime.now()
                        time.sleep(delta.seconds+32400)
                
                    elif error['message'] == "Sorry, you're following the max limit of accounts. \
                        You'll need to unfollow some accounts to start following more.":
                        text = "Sorry, you're following the max limit of accounts. \
                        You'll need to unfollow some accounts to start following more. Start Agin in 3 Days later .\
                            {} \n".format(datetime.datetime.now())     
                        with open (log_file ,"a") as file :
                                    file.write(text)
                        print (text)
                        tomorrow = datetime.datetime.replace(
                                                            datetime.datetime.now() + datetime.timedelta(days=3),
                                                            hour=0, minute=0, second=0
                                                            )
                        delta = tomorrow - datetime.datetime.now()
                        time.sleep(delta.seconds+32400)
                else : 
                    with open (log_file ,"a") as file :
                        file.write(error)

        def follower_id():
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
                if id_counter == 2*10**5 :
                    break
            for id in followers :
                followers_id.append(id['pk'])
            time.sleep(120)
            return followers_id
        count_id = 0
        new = follower_id()   
        for id in new :
            if id in final_list :
                count_id += 1
        follower_final , following_finall = info()
        text = "Following is not Completed . Please Add Another Pages to Start Following . \n Resualt at {} is : \n \
            Follower : {} \n Following : {} \n Remaining : {} \n".format(datetime.datetime.now() ,follower_final ,following_finall ,(follower_max - follower_final) ) + 50 * "*"
        text = text + "Followers Added With Ids : {} \n".format(count_id)
        with open (log_file ,"a") as file :
            file.write(text)
        print (text)
        return follower_max-follower_final

    def logout (self) :
        return self.API.logout()

def main () :
    def user_pass () :
        repeat = True 
        while repeat != False :  # username , password
            username = input ("Instagram Username : ")
            password = getpass ("Instagram Password : ")
            try : 
                Follow = Following(username ,password)
                repeat = False
            except :
                print ("Invalid Username or Password !!!")
        return Follow
    Follow = user_pass ()
    global log_file
    def get_info () :
        repeat = True
        while repeat != False : # page count
            try :
                pages_count = int (input ("Number of Instagram Pages : "))
                repeat = False
            except :
                print ("Enter a Number !!!")
        count = 0
        pages= []
        while pages_count != count :  # check page invalid
            page = input ("Page Name : ") 
            try : 
                is_public = Follow.is_public(page)
                if is_public :
                    pages.append(page)
                    count += 1
                else : 
                    print (f"Please Change The Page .The Page << {page} >> is Private .")
            except :
                print ("Invalid Page Id !!! ")

        with open (log_file ,"a") as file :
            text = "Pages for getting Followers : \n {}".format(pages)
            file.write(text)
        return pages
    pages = get_info ()
    text = "Creating Ids List From Pages ... \n"
    with open (log_file ,"a") as file :
        file.write(text)
    print (text)
    final_followers = Follow.create_following_list(pages)
    text = "Number Of Ids For Following : {} \n".format(len(final_followers))
    with open (log_file ,"a") as file :
        file.write(text)
    print (text)
    repeat = True
    while repeat != False :  # follower add
        follower_add = input ("How Many Followers to Add : ")
        try :
            follower_add = int (follower_add)
            repeat = False
        except :
            print ("Enter a Number !!!")
    text = "Start Following Ids at : {} \n".format(datetime.datetime.now())
    with open (log_file ,"a") as file :
        file.write(text)
    print (text)
    remaining = Follow.follow(final_followers ,follower_add)
    while not remaining :
        text = "Your Remaining Add Follwer : {} \n".format(remaining)
        text = text + "Add New Pages to Get Followers ... \n"
        with open (log_file ,"a") as file :
            file.write(text)
        print (text)
        pages = get_info ()
        text = "Creating Ids List From New Pages ... \n"
        with open (log_file ,"a") as file :
            file.write(text)
        print (text)
        final_followers = Follow.create_following_list(pages)
        text = "Start Again Following Ids at : {} \n".format(datetime.datetime.now())
        with open (log_file ,"a") as file :
            file.write(text)
        print (text)
        remaining = Follow.follow(final_followers ,remaining)
    Follow.logout()

if __name__ == "__main__":
    main()








