# Buffer automattion -- Schedule tweets to buffer from the clipboard
[@readwithai](https://x.com/readwithai) ([🦋](https://bsky.app/profile/readwithai.bsky.social), [𝕏](https://x.com/readwithai), [blog](https://readwithai.substack.com/), [▶️](https://www.youtube.com/@readerai/shorts)) 

This is a quite hacky automation script for the [Buffer](https://buffer.com/) social media automation website. It allows you to schedule tweets in a way that I find (and hopefully is) simpler by reading tweets in a text from the clipboard together with a date.

This is meant to allow you to do all you thinking and planning in a text file before scheduling tweets.

For the moment, you need to be familiar with the Python language to use this tool

## How this works
Instead of using an interface to schedule every tweet, you write the tweets you want to send and when in a text file like so:

```
2025-02-01T12:00:00Z  This is my first tweet

# comment
2025-02-01T13:00:00Z  This is my second tweet an hour later
```

This is useful because you can keep notes / move tweets around etc and see everything in one page.

When you want to actually schedule a tweet you copy it to the clipboard and run a command in a Python shell to read from the clipboard and send it - avoid annoying fiddling with a scheduler - instead you just tweak the date in you rfile. 

If you use this regularly you will probably want a tool to insert the current timestamp. I use [Obsidian](https://readwithai.substack.com/p/obsidian-what-and-why) for this together with a this tiny script for [plugin repl](https://readwithai.substack.com/p/obsidian-plugin-repl).

```
newCommand(function insert_timestamp() {
	insert(new Date().toISOString())
})
```

(P.s plugin repl is written by me)

# Usage
This project is a set of functions in python. You run them from a python shell that automates a browser through selenium. Once I have used this for a while I might try implementing this with a keyboard shortcut, when I tire of finding the approiate command line window to post

For the moment.

1. Check out this repository
1. Set up a virtualenv / install the requirements.
1. Start shell and run the following:

```
import buffer
b = buffer.Buffer()
b.login()
# copy something into the clipboard in the form specified above
b.post_clipboard() # run this every time you want to tweet somethingy

```

## Maintenance
I'm probably not going to make your feature for you. I will probably add my feature here. If you have something useful, that I am personally likely to find useful I will probably accept your patch. I will use this tool a lot daily so it will be moderately maintained and likely improve over time. 

## Features I'm likely to add
- Buffer supports thread - I will probably add something to suppor this eventually.
- Buffer supports bluesky and other social media sites - I may well add the ability to use these at some points
- I will probably add a feature to send multiple tweets at the same time
- I might add a feature to remove scheduled tweets (perhaps just all of them)

## Development
I tried to implement this as a bookmarklet in javascript but had issues automating the processing of typing the tweet.

## Alternatives
While buffer does not provide an API itself (any more) it does provide an API to some "integration" services such as [Zapier](https://github.com/talwrii/buffer-automation/edit/master/README.md), [if this then than](https://ifttt.com/buffer) and [microsoft power automate](https://make.powerautomate.com/connectors/shared_buffer/buffer/). I have found tools like IFTTT difficult to debug before as you run them "at a distance" but power automate looks more set up for "programming". 

I *may* have implemented this using one of these services if I had known about this before implementing (mostly to avoid the fragility of browser automation), though these "integrations" tend to have lots of moving parts, take longer than expect and often cost additional money. This works and is quite controlled.

# About me
*If you are interested in this you might specifically like to read my blog post about [reading and agency](https://github.com/talwrii/buffer-automation) since you are likely interested in social media*

I am @readwithai I am interested in tools for reading, autonomy and ai with a focus on tooling around Obsidian. If any of this sound interesting read my [blog](
https://readwithai.substack.com/). You can also follow me on [𝕏](https://x.com/readwithai).

If you find *this* tool useful maybe give me 5 dollars on my [ko-fi](https://ko-fi.com/readwithai).

Also, This was moderately fun to work on and part of my daily flow so I would be open to adapting this to your needs for a discussed fee. (See [here](https://readwithai.substack.com/p/buy-my-work))
