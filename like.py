from InstagramAPI import InstagramAPI
from getpass import getpass
import time

class Like :
    def __init__ (self ,username ,password) :
        self.API = InstagramAPI (username ,password)
        self.API.login()
        self.username = username
        self.username_id = self.API.username_id

    def like (self) :
        count = 0
        self.API.timelineFeed()
        timeline_feed_posts = self.API.LastJson['items'] # get 6 last post in timeline feed
        for post in timeline_feed_posts :
            try : 
                if "taken_at" and "comment_likes_enabled" in post :
                    if post["comment_likes_enabled"]==True and post['has_liked']==False :
                        media_id = post["id"]
                        self.API.like(media_id)
                        time.sleep(40)
                        count += 1
                    else : pass
                else : pass
            except : pass

        return count

    def logout (self) :
        return self.API.logout()

def main (counter_like) :
    repeat = True 
    while repeat != False :  # username , password
        username = input ("Instagram Username : ")
        password = getpass ("Instagram Password : ")
        try : 
            liker = Like(username ,password)
            repeat = False
        except :
            print ("Invalid Username or Password !!!")
    print ("Start Liking ...")
    done = liker.like()
    remaining = counter_like - done
    print ("Likes : " ,done)
    while remaining !=0 :
        done = liker.like()
        remaining = remaining - done
        print ("Likes : " ,remaining)
        if done == 0 :
            print ("No Feed to Like ")
            time.sleep(14400)
    print ("Finished .")
    liker.logout()

if __name__ == "__main__":
    counter_like = input ("How Many Likes : ")
    while not counter_like.isnumeric() :
        print ("Please Enter A Number !")
        counter_like = input ("How Many Likes : ")
    main(counter_like)