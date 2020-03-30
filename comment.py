from InstagramAPI import InstagramAPI
from getpass import getpass
import time ,datetime

class Comment :
    def __init__ (self ,username ,password) :
        self.API = InstagramAPI (username ,password)
        self.API.login()
        self.username = username
        self.username_id = self.API.username_id

    def comment (self ,counter_comment) :
        list_commented = []
        count_all = 0
        self.API.timelineFeed()
        timeline_feed_posts = self.API.LastJson['items'] # get 6 last post in timeline feed
        for post in timeline_feed_posts :
            try : 
                if "taken_at" and "comment_likes_enabled" in post :
                    if post["comment_likes_enabled"]==True and post["id"] not in list_commented:
                        commentText = "بسیار عالی بود " + "." +"خوشحال میشم از پیج من هم دیدین نمایید " + "@{}".format(self.username)
                        media_id = post["id"]
                        list_commented.append(media_id)
                        self.API.comment(mediaId=media_id ,commentText=commentText)
                        count += 1
                        count_all += 1
                        print (count_all ,end="-")
                        time.sleep(400)
                        if count_all >= counter_comment :
                            break
                        elif count == 50 :
                            print ("Instagram Daily Limit . " , datetime.datetime.now())
                            print (50 * "*")
                            tomorrow = datetime.datetime.replace(
                                                                datetime.datetime.now() + datetime.timedelta(days=1),
                                                                hour=0, minute=0, second=0
                                                                )
                            delta = tomorrow - datetime.datetime.now()
                            time.sleep(delta.seconds+36000)
                            count = 0
                    else : pass
                else : pass
            except : pass
        print ("Number of Comments : " ,count_all)
        return count_all

    def logout (self) :
        return self.API.logout()

def main (comment_counter) :
    repeat = True 
    while repeat != False :  # username , password
        username = input ("Instagram Username : ")
        password = getpass ("Instagram Password : ")
        try : 
            comment = Comment(username ,password)
            repeat = False
        except :
            print ("Invalid Username or Password !!!")
    print ("Start Commenting ...")
    done = comment.comment(comment_counter)
    remaining = comment_counter - done
    if done == 0 :
        print ("No Feed to Comment ")
        time.sleep(14400)
    while remaining !=0 :
        done = comment.comment(remaining)
        remaining = remaining - done
        if done == 0 :
            print ("No Feed to Comment ")
            time.sleep(14400)
    print ("Finished .")
    comment.logout()

if __name__ == "__main__":
    comment_counter = input ("How Many Comment : ") 
    while not comment_counter.isnumeric() :
        print ("Please Enter A Number !")
        comment_counter = input ("How Many Comment : ") 
    main(comment_counter)