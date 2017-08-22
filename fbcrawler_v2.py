import facebook
from datetime import timedelta
import datetime
import json
import requests
import csv
import os
from importlib import import_module



def time_process(s):
    xs = s.split("T")
    time_str = xs[0].split('-') + xs[1].split('+')[0].split(':')
    time_int = [int(s) for s in time_str]
    return time_int[:-1]

def lifetime_in_hour(created_time):
    timeNow = datetime.datetime.now()
    Y, M, D, H, m = created_time
    timeCreated = datetime.datetime(Y, M, D, H, m)
    return (timeNow - timeCreated).total_seconds() / 3600
def time_zone_revise(created_time):
    revise = timedelta(hours = 8)
    Y, M, D, H, m = created_time
    timeCreated = datetime.datetime(Y, M, D, H, m)
    timeRevised = timeCreated + revise
    return [timeRevised.year, timeRevised.month, timeRevised.day, timeRevised.hour, timeRevised.minute]

class Recorder(object):
    def __init__(self):
        print("init")

    def save(self, filename):
        print("save")
        with open(filename,'w') as f:
            json.dump(self.record, f)

    def load(self, filename):
        print("load")
        if os.path.isfile(filename):
            with open(filename) as f:
                self.record = json.load(f)
        else:
            self.record = {}

    def update(self, token):
        print("update")
        graph = facebook.GraphAPI(access_token = token, version = '2.7' )
        posts = graph.get_object("coscup/posts")['data']
        post_id_list = []
        created_time_list = []
        self.timenow = datetime.datetime.now()
        #  timestamp = (timenow.year, timenow.month, timenow.day, timenow.hour)
        #  print(timestamp)

        for post in posts:
            post_id_list.append(post['id'])
            created_time_list.append(time_zone_revise(time_process(post["created_time"])))

        for post_id, created_time in zip(post_id_list, created_time_list):
            post_likes = graph.get_object(post_id + '/likes?summary=true')
            post_impressions_fan_unique = graph.get_object(post_id + '/insights/post_impressions_fan_unique/lifetime')
            post_impressions_unique = graph.get_object(post_id + '/insights/post_impressions_unique/lifetime')
            
            if post_id in self.record:
                print("post id exists")
                #  created_time = self.record[post_id]["created_time"]
                time_after_created = lifetime_in_hour(created_time)
                record = self.record[post_id]
                record["record_time"].append(time_after_created)
                record["record_data"][0].append(post_likes["summary"]['total_count'])
                record["record_data"][1].append(post_impressions_unique['data'][0]['values'][0]['value'])
                record["record_data"][2].append(post_impressions_fan_unique['data'][0]['values'][0]['value'])
            else:
                print("post id does not exists, creat new record")
                time_after_created = lifetime_in_hour(created_time)
                self.record[post_id] = {"created_time" : created_time, 
                        "record_time" :[time_after_created],
                        "record_data" :[[post_likes["summary"]['total_count']],
                            [post_impressions_unique['data'][0]['values'][0]['value']],
                            [post_impressions_fan_unique['data'][0]['values'][0]['value']]]}

    def display(self):
        print("display")

    def plotSinglePost(self, postID):
        if postID in self.record :
            plt = import_module("matplotlib","pyplot")
            plt.clf()
            plt.plot()
            print("plot single post: ", postID)




if __name__ == "__main__":
    token = "EAACEdEose0cBAAZBiDZCYnyDzZCWies7oKL9cUaw5GZAJWMi7buIyLaHZCL37GOfAZBeCZAzkISOwYAFYwDk9ugHyg8j8L0WUZA1KpSRmxBLAJRiPgdmdF7E8pgZAno4GBgQ20z5i77oA9JzHJ0NK10vtnkX64CcoxuuZAfqcZCTPh0ekcfyvYcYY0LwE2u0hPveMYZD"
    recorder = Recorder()
    recorder.load("record.son")
    recorder.update(token)
    recorder.save("record.son")
