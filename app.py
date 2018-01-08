from flask import Flask
from flask import render_template, flash, redirect, request, Markup
import searchForm
import config
import praw
from prawcore import NotFound
import os

MAX_VALUES = 30
COMMENT_DEPTH = 20

app = Flask(__name__)
app.config.from_object(config.Config)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = searchForm.Form()
    if form.validate_on_submit():
        redirectString = '/results?thread=%s&searchTerm=%s&count=%s' %(form.thread.data, form.searchTerm.data, form.searchNumber.data)
        if(form.subreddit.data):
            redirectString += '&subreddit=' + form.subreddit.data
        if(form.postAuthor.data):
            redirectString +=  '&postAuthor=' + form.postAuthor.data
        # call function to query reddit
        return redirect(redirectString)
    return render_template('index.html',form=form)

@app.route('/results')
def results():
    if not os.environ.get('envtype') == "prod":
        reddit = praw.Reddit('bot1')
    else:
        reddit = praw.Reddit(client_id=os.environ.get('cid'),
                     client_secret=os.environ.get('csecret'),
                     user_agent=os.environ.get('cagent'))
    subredditstring = request.args.get('subreddit').replace(" ", "")
    if not sub_exists(subredditstring, reddit):
        return render_template('results.html', results=Markup('<p class="error">Subreddit <b>'+subredditstring+'</b> not found!<br><br><br><a href="\\" class="goback"> Try Again! </a></p>'))
    subreddit = reddit.subreddit(subredditstring)
    keys = request.args.get('searchTerm').split()
    searchTerm = request.args.get('thread')
    if(request.args.get('postAuthor')):
        searchTerm += ' author:' + request.args.get('postAuthor')

    results = {}
    count = 0
    found = False
    submissionLimit = int(request.args.get('count'))
    for submission in subreddit.search(searchTerm, sort='new'):
        if count > submissionLimit:
            break
        count += 1
        submission.comments.replace_more(limit=None)
        for topcomment in submission.comments:
            for key in keys:
                if key.lower() in topcomment.body.lower():
                    found = True
                    if(submission in results.keys()):
                        results[submission].append(topcomment)
                    else:
                        results[submission] = [topcomment]

    if not found:
        return render_template('results.html', results=Markup('<p class="error">No Results<br><br><br><a href="\\" class="goback"> Try Again! </a></p>'))
    return render_template('results.html', results=Markup(resultBuilder(results, keys)))


def resultBuilder(results, keys):
    resString = ""
    for submission, comments in results.items():
        resString += '<a class="submissionTitle"href=%s>%s</a>' %("http://reddit.com"+submission.permalink, submission.title)
        for comment in comments:
            resString += recurseBuilder(comment, True, keys)
    return resString

def recurseBuilder(result, isTop, keys):
    resString = '<br><div class="boxes" >'
    if(isTop):
        resString += '<a class="topcomment" href=%s>%s</a>' %("http://reddit.com"+result.permalink, boldKey(result.body, keys))
    else:
        resString += "<p class=subcomment>%s</p>" %(result.body)
    for nextResult in result.replies:

        resString += recurseBuilder(nextResult, False, keys)
    resString += "</div>"
    return resString

def boldKey(body, keys):
    for key in keys:
        body = body.replace(key.lower(), "<b>"+key.upper()+"</b>")
        body = body.replace(key[0:1].upper()+key[1:],"<b>"+key.upper()+"</b>")
    return body

def sub_exists(sub, reddit):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists
