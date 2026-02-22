#!/usr/bin/env python3
"""
🎮 HINATA GAMES MODULE
Fun games to keep the group active
"""

import random

class GamesManager:
    def __init__(self):
        self.truth_questions = [
            "kabhi kiss kiya hai",
            "tumhara crush kaun hai",
            "kabhi jhooth bola hai apne parents ko",
            "tumhara embarrassing moment kya tha",
            "kabhi phone mein kisi ka message padha hai bina bataye",
            "tumhara first impression kaisa tha group ka",
            "kabhi kisi se pyaar kiya hai",
            "tumhara favourite person kaun hai is group mein",
            "kabhi raat ko sochte sochte roye ho",
            "tumhara biggest fear kya hai",
            "kabhi kisi ko ghost kiya hai",
            "tumhara guilty pleasure kya hai",
            "kabhi kisi ka secret reveal kiya hai",
            "tumhara childhood crush kaun tha",
            "kabhi kisi se jhooth bolke fayda uthaya hai",
            "tumhara weirdest habit kya hai",
            "kabhi kisi ko stalk kiya hai social media pe",
            "tumhara favourite anime character kaun hai",
            "kabhi kisi se online fight ki hai",
            "tumhara dream date kaisa hoga",
            "kabhi kisi ka gift wapas kiya hai",
            "tumhara most used app kaunsa hai",
            "kabhi kisi ko propose kiya hai",
            "tumhara favourite food kya hai",
            "kabhi kisi se jealous feel kiya hai",
            "tumhara hidden talent kya hai",
            "kabhi kisi ka phone check kiya hai",
            "tumhara favourite singer kaun hai",
            "kabhi kisi ko block kiya hai gusse mein",
            "tumhara zodiac sign kya hai",
            "kabhi kisi se dosti todi hai",
            "tumhara favourite movie kaunsi hai",
            "kabhi kisi ko ignore kiya hai purposely",
            "tumhara favourite colour kya hai",
            "kabhi kisi ka naam galat bulaya hai",
            "tumhara favourite game kaunsa hai",
            "kabhi kisi se jhooth bola hai ki tum busy ho",
            "tumhara dream job kya hai",
            "kabhi kisi ko prank call kiya hai",
            "tumhara favourite season kaunsa hai",
            "kabhi kisi ka birthday bhool gaye ho",
            "tumhara favourite subject kya tha school mein",
            "kabhi kisi se borrowed money liya hai aur wapas nahi kiya",
            "tumhara favourite holiday destination kya hai",
            "kabhi kisi ko fake promise kiya hai",
            "tumhara favourite animal kya hai",
            "kabhi kisi ka secret group mein bataya hai",
            "tumhara favourite ice cream flavour kya hai",
            "kabhi kisi se online dating ki hai",
            "tumhara favourite superhero kaun hai",
        ]

        self.dare_challenges = [
            "apna favourite song suna group mein",
            "apna profile picture change karke 1 ghante rakh",
            "apna status mein i love hinata likh 10 min ke liye",
            "group mein apna secret batade",
            "apna crush ka naam bata",
            "apna phone ka wallpaper dikha",
            "apna last search history dikha",
            "apna favourite meme share kar",
            "apna embarrassing moment batade",
            "apna childhood photo share kar",
            "apna favourite joke suna",
            "apna favourite quote likh",
            "apna zodiac sign bata",
            "apna favourite colour bata",
            "apna favourite food bata",
            "apna favourite movie bata",
            "apna favourite TV show bata",
            "apna favourite singer bata",
            "apna favourite actor bata",
            "apna favourite actress bata",
            "apna favourite youtuber bata",
            "apna favourite tiktoker bata",
            "apna favourite app bata",
            "apna favourite game bata",
            "apna favourite sport bata",
            "apna favourite anime bata",
            "apna favourite cartoon bata",
            "apna favourite superhero bata",
            "apna favourite villain bata",
            "apna favourite character bata",
            "apna favourite emoji bata",
            "apna favourite sticker bhejo",
            "apna favourite gif bhejo",
            "apna favourite meme bhejo",
            "apna favourite photo bhejo",
            "apna favourite video bhejo",
            "apna favourite song bata",
            "apna favourite dance step dikha",
            "apna favourite dialogue bolo",
            "apna favourite shayari suna",
            "apna favourite poem suna",
            "apna favourite story suna",
            "apna favourite riddle pooch",
            "apna favourite fact bata",
            "apna favourite trivia bata",
            "apna favourite news bata",
            "apna favourite trend bata",
            "apna favourite challenge bata",
            "apna favourite filter use karke photo bhejo",
            "apna favourite sticker use karke message bhejo",
            "apna favourite emoji use karke message bhejo",
            "apna favourite gif use karke message bhejo",
        ]

    def get_truth(self):
        return random.choice(self.truth_questions)

    def get_dare(self):
        return random.choice(self.dare_challenges)

    def roll_dice(self):
        return random.randint(1, 6)

    def flip_coin(self):
        return random.choice(["Heads", "Tails"])

    def play_rps(self, user_choice):
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)

        if user_choice == bot_choice:
            return "Draw", bot_choice
        elif (user_choice == "rock" and bot_choice == "scissors") or \
             (user_choice == "paper" and bot_choice == "rock") or \
             (user_choice == "scissors" and bot_choice == "paper"):
            return "You Win", bot_choice
        else:
            return "Hinata Wins", bot_choice
