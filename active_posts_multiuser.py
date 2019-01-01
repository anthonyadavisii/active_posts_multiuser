import csv
import datetime
import json
import os
import urllib.request

from beem.account import Account
from beem.comment import Comment
from beem.exceptions import AccountDoesNotExistsException, ContentDoesNotExistsException
from beem.nodelist import NodeList
from beem.instance import set_shared_steem_instance
from beem import Steem

def export_csv(name,votelist):
    cwd = os.getcwd()
    filename=datetime.datetime.now().strftime(name+"%Y%m%d-%H%M%S.csv")
    keys = votelist[0].keys()
    outfile=open(cwd+'/'+filename,'w')
    writer=csv.DictWriter(outfile, keys)
    writer.writeheader()
    writer.writerows(votelist)

def active_posts_multiuser_bl_check(userlist):
    activeposts = []
    for u in userlist:
        a = Account(u)
        contents = urllib.request.urlopen("http://blacklist.usesteem.com/user/"+u).read()
        contents = json.loads(contents)
        if contents['blacklisted'] ==[]:
            blacklisted = False
            print('@'+u+' is not on any blacklist tracked via the API')
        else:
            blacklists = []
            for bl in contents['blacklisted']:
                blacklists.append(bl)
            print('@'+u+' is on the following blacklists: ')
            blacklisted = True
        gen = a.blog_history()
        for b in gen:
            if b.is_pending():
			    c = Comment(b.identifier)
                post_dict = {
                                'Author': u,
                                'Comment': '[Comment](https://steemit.com/'+b.identifier+')', 
                                'Remaining Rewards': c['pending_payout_value'],
                                'Blacklisted?': blacklisted
                              }
                activeposts.append(post_dict)
    return activeposts

def main():
    input_string = input("Enter list of accounts delimited by commas")
    userlist  = input_string.split(",")
    activeposts = active_posts_multiuser_bl_check(userlist)
    export_csv('active_posts_multiuser',activeposts)

if __name__== "__main__":
    main()