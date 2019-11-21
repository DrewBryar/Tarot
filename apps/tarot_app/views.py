from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

CARD_LIST = [
    {'name': 'The Fool', 'image': 'images/fool.jpg', 'description': 'Free spirit and unlimited potential.', 'categories': {
        'love': 'The Fool encourages you to have an open, curious mind and a sense of excitement. Throw caution to the wind and be ready to embrace the unknown, leaving behind any fear, worry     or anxiety about what may or may not happen. Today is about new experiences, personal growth, development, and adventure.', 
        'career': 'This is a time of great potential and opportunity for you right now. The world is your oyster, and anything can happen. Use your creative mind with a dash of spontaneity to     make the most of this magical time and bring forth your new ideas in powerful ways.', 
        'moody':'This is an excellent card to meditate on if you are struggling with dread, worry or self-doubt in your life. The Fool is your guide, as someone who is daring and            carefree. He is the embodiment of who you really are – your free spirit, your inner child, and your playful soul. Any time you experience fear, remember the essence of the Fool as he encourages you to acknowledge that fear and do it anyway! You never know what the future holds, but like the Fool, you must step into the unknown, trusting that the Universe will catch you and escort you along the way. Take a chance and see what happens.'}},
    {'name': 'The Magician', 'image': 'images/magician.jpg', 'description': 'Resourcefulness and power.', 'categories': {
        'love': 'a thing', 
        'career': 'The Magician brings you the tools, resources and energy you need to make your dreams come true. Seriously, everything you need right now is at your fingertips. You have the  spiritual (fire), physical (earth), mental (air) and emotional (water) resources to manifest your desires. And when you combine them with the energy of the spiritual and earthly realms, you will become a manifestation powerhouse! The key is to bring these tools together synergistically so that the impact of what you create is greater than the separate parts. Put your work into motion today. All you are missing today is discipline and momentum.',
        'home': 'a thing',
        'friendship': 'The Magician is symbolic of action and power in your life. Its positive connotations illustrate someone who is a smooth talker and good at all aspects of communication. This card suggests using your strong will power to move forward and take action. Use this superpower you have today to communicate with the people you surround yourself with. Bringing your ideas to the table and listening to others about theirs will help you form long lasting bonds.'
        'moody': 'Today is the perfect time to move forward on an idea that you recently conceived. The seed of potential has sprouted, and you are being called to take action and bring your intention to fruition. The skills, knowledge and capabilities you have gathered along your life path have led you to where you are now, and whether or not you know it, you are ready to turn your ideas into reality.' }},
    {'name': 'The High Priestess', 'image': 'images/high_priestess.jpg', 'description': 'Intuition and secret knowledge.', 'categories': {
        'love': 'The High Priestess signifies spiritual enlightenment, inner illumination, divine knowledge and wisdom. Today is a time of heightened intuitive ability and psychic insight. Follow your intuition as you may know more than others believe to do. This card may be a warning of concealed facts or influences that are, or will be important to you.', 
        'career': 'The High Priestess signifies spiritual enlightenment, inner illumination, divine knowledge and wisdom. Today, the undiscovered or repressed creative abilities you have are demanding to be expressed. Finding a spiritual guide will help you realize the full potential of your abilities. In order to get what you desire, you will need to overcome your fear of commitment.',
        'friendship': 'The High Priestess signifies spiritual enlightenment, inner illumination, divine knowledge and wisdom. This card is a signal to embrace more connection with others using your personal connection to your compassion and empathy. Feel, rather than think. Collaborate, rather than compete. Create, rather than destroy. Trust your energy even if the masculine energy around you may appear to be stronger. Be proud of your ability today to nurture, trust, sense and empathise instead of hiding it away.',
        'moody':'Your intuitive sense right now is providing you with useful information and is assisting you to become more in touch with your subconscious mind. Knowledge of how to fix these issues will not come through thinking and rationalising, but by tapping into and trusting your intuition, so allow yourself the time and space to meditate and attend to your inner voice. Look for areas in your life that may be out of balance or lacking ‘flow’ and ease.'}},
    {'name': 'The Empress', 'image': 'images/empress.jpg', 'description': 'Femininity, beauty, and nurture.', 'categories': {
        'love': 'The Empress signifies a strong connection with our femininity. Femininity translates in many ways – elegance, sensuality, fertility, creative expression, nurturing – and is necessary for creating balance in both men and women. The Empress calls on you to connect with your feminine energy. Create beauty in your life. Connect with your senses through taste, touch, sound, smell and sight. Draw on these senses to experience pleasure and deep fulfilment. /nWhen you are in tune with the energy of the Empress, you will naturally take on her mothering nature. Today, feel a strong urge to nurture and care for others, from a place of loving compassion and support. See it as a gift and an honour to tend to others, and in doing so you, too, receive benefit. In a more literal sense, you may step into the role of ‘mother’, perhaps as the mother of a newborn, caretaker of other people’s children, or spending more quality time with your kids. ', 
        'career': 'The Empress signifies a strong connection with our femininity. Femininity translates in many ways – elegance, sensuality, fertility, creative expression, nurturing – and is necessary for creating balance in both men and women. The Empress calls on you to connect with your feminine energy. Create beauty in your life. Connect with your senses through taste, touch, sound, smell and sight. Draw on these senses to experience pleasure and deep fulfilment. The Empress can also suggest pregnancy or birth. This may be an actual pregnancy or childbirth, or a metaphorical ‘birth’ of a new idea or project. Today, bring your creative ideas into being by nurturing them and supporting their growth. Allow those designs and their manifestation to flow through you, acting with compassion and love.',
        'home': 'The Empress signifies a strong connection with our femininity. Femininity translates in many ways – elegance, sensuality, fertility, creative expression, nurturing – and is necessary for creating balance in both men and women. The Empress calls on you to connect with your feminine energy. Create beauty in your life. Connect with your senses through taste, touch, sound, smell and sight. Draw on these senses to experience pleasure and deep fulfilment. The Empress in your reading today signifies abundance. You are surrounded by life’s pleasures and luxuries and have everything you need to live a comfortable lifestyle. You are in a period of growth, in which all you have dreamed of is now coming to fruition. Today, take a moment to reflect on the bounty that surrounds you and offer gratitude for all you have created so you can continue to build on this energy and create even more abundance in your life.',
        'friendship': 'The Empress signifies a strong connection with our femininity. Femininity translates in many ways – elegance, sensuality, fertility, creative expression, nurturing – and is necessary for creating balance in both men and women. The Empress calls on you to connect with your feminine energy. Create beauty in your life. Connect with your senses through taste, touch, sound, smell and sight. Draw on these senses to experience pleasure and deep fulfilment. /nToday, the Empress urges you to venture out. You have been inside, continuing the same routines. Invite a friend into nature today to ground your energy and be in flow with the earth. Take a trip to your favourite natural setting, be it a walk around your local park, beach, or lake, and sit for a couple of minutes or even hours to breathe in the energy that surrounds you while marvelling in the beauty of your surroundings. Share this often forgotten possible recess with someone you wish to connect with today! Allow the time and the space to enter a different frame of mind and receive the grounding spirit of nature into your heart and consciousness.'
        'moody':'Today, the Empress encourages you to make self-love and self-care a priority. Now is the time to bring your loving energy and focus to yourself, especially if you have been giving away your personal power by placing too much emphasis on another person’s emotional or material needs, thus neglecting your own. Book a dinner or a weekend, go for a walk on your own or start a creative project that’s just for you. It is essential that you fill your cup and care for yourself so you can then take care of others without resentment.'}},
    {'name': 'The Emperor', 'image': 'images/emperor.jpg', 'description': 'Authority and Structure', 'categories': {
        'love': 'As the father figure of the Tarot deck, the Emperor suggests that you are adopting this fatherly role (regardless of whether you are male or female), providing for your family, and protecting and defending your loved ones. You may be the breadwinner or the ‘rock’ for those who rely on your stability and security. Today, make sure you fill in this Emperor role. Assure the person most important in your life your pledge to assist them in their difficulties. Whatever they may be, your love deserves to know this.', 
        'career': 'The Emperor represents a powerful leader who demands respect and authority. Status, power and recognition are essential to you, and you are most comfortable in a leadership role where you can command and direct others. As a leader, you rule with a firm but fair hand. You have a clear vision of what you want to create, and you organise those around you to manifest your goal. Today, listen to the advice of others, but prefer to have the final say. Conflict doesn’t scare you, and you won’t hesitate to use your power to protect those you care about. And in return, those people will repay you with the loyalty and respect you deserve. Claim your authority as leader and influencer and don’t let others put you down. /nThere may be a moment where someone in a position of authority offers to help you. In any form, the more experienced hand that has come to help you may be more capable than yours. Protecting your loved ones is important, but those in a leadership position must know how to compromise. Beware the overly-dependant.',
        'home': 'As the father figure of the Tarot deck, the Emperor suggests that you are adopting this fatherly role (regardless of whether you are male or female), providing for your family, and protecting and defending your loved ones. You may be the breadwinner or the ‘rock’ for those who rely on your stability and security. Today, take a step to encourage support and happiness to those you share home with in your life.',
        'friendship': 'As the father figure of the Tarot deck, the Emperor suggests that you are adopting this fatherly role (regardless of whether you are male or female), providing for your friends, and protecting and defending your loved ones. You may be the ‘rock’ for those who rely on your stability and security.',
        'moody':'The Emperor reflects a system bound by rules and regulations. You create law and order by applying principles or guidelines to a specific situation. Today, create calm out of chaos by breaking down any problem into its parts and then mapping out the actions you need to take to resolve it. Be systematic, strategic and highly organised in your approach, and stick to your plan until the end.'}},
    {'name': 'The Hierophant', 'image': 'images/hierophant.jpg', 'description': 'Conformity, traditions, and institutions', 'categories': {
        'love': 'a thing', 
        'career': 'another thing'
        ,'home': 'a thing',
        'friendship': 'a thing',
        'moody':''}},
    {'name': 'The Lovers', 'image': 'images/lovers.jpg', 'description': 'we live in a society', 'categories': {
        'love': 'Lucky you! This card is a great card. The lovers represents the deep connection between two souls. There is a person in your life who love and care about you more than anything else. When you are away from each other, you are both on eachothers mind  ', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Chariot', 'image': 'images/chariot.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Strength', 'image': 'images/strength.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Hermit', 'image': 'images/hermit.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Wheel of Fortune', 'image': 'images/wheel_of_fortune.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Justice', 'image': 'images/justice.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Hanged Man', 'image': 'images/hanged_man.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Death', 'image': 'images/death.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Temperance', 'image': 'images/temperance.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Devil', 'image': 'images/devil.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Tower', 'image': 'images/tower.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Star', 'image': 'images/star.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Moon', 'image': 'images/moon.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Sun', 'image': 'images/sun.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Judgement', 'image': 'images/judgement.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The World', 'image': 'images/world.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},


    {'name': 'Ace of Wands', 'image': 'images/wands_ace.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Two of Wands', 'image': 'images/wands_twp.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Three of Wands', 'image': 'images/wands_three.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Four of Wands', 'image': 'images/wands_four.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Five of Wands', 'image': 'images/wands_five.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Six of Wands', 'image': 'images/wands_six.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Seven of Wands', 'image': 'images/wands_seven.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Eight of Wands', 'image': 'images/wands_eight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Nine of Wands', 'image': 'images/wands_nine.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Ten of Wands', 'image': 'images/wands_ten.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Page of Wands', 'image': 'images/wands_page.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Knight of Wands', 'image': 'images/wands_knight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Queen of Wands', 'image': 'images/wands_queen.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'King of Wands', 'image': 'images/wands_king.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},

    {'name': 'Ace of Swords', 'image': 'images/swords_ace.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Two of Swords', 'image': 'images/swords_twp.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Three of Swords', 'image': 'images/swords_three.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Four of Swords', 'image': 'images/swords_four.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Five of Swords', 'image': 'images/swords_five.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Six of Swords', 'image': 'images/swords_six.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Seven of Swords', 'image': 'images/swords_seven.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Eight of Swords', 'image': 'images/swords_eight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Nine of Swords', 'image': 'images/swords_nine.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Ten of Swords', 'image': 'images/swords_ten.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Page of Swords', 'image': 'images/swords_page.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Knight of Swords', 'image': 'images/swords_knight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Queen of Swords', 'image': 'images/swords_queen.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'King of Swords', 'image': 'images/swords_king.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},

    {'name': 'Ace of Cups', 'image': 'images/cups_ace.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Two of Cups', 'image': 'images/cups_twp.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Three of Cups', 'image': 'images/cups_three.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Four of Cups', 'image': 'images/cups_four.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Five of Cups', 'image': 'images/cups_five.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Six of Cups', 'image': 'images/cups_six.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Seven of Cups', 'image': 'images/cups_seven.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Eight of Cups', 'image': 'images/cups_eight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Nine of Cups', 'image': 'images/cups_nine.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Ten of Cups', 'image': 'images/cups_ten.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Page of Cups', 'image': 'images/cups_page.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Knight of Cups', 'image': 'images/cups_knight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Queen of Cups', 'image': 'images/cups_queen.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'King of Cups', 'image': 'images/cups_king.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},

    {'name': 'Ace of Pentacles', 'image': 'images/pentacles_ace.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Two of Pentacles', 'image': 'images/pentacles_twp.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Three of Pentacles', 'image': 'images/pentacles_three.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Four of Pentacles', 'image': 'images/pentacles_four.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Five of Pentacles', 'image': 'images/pentacles_five.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Six of Pentacles', 'image': 'images/pentacles_six.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Seven of Pentacles', 'image': 'images/pentacles_seven.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Eight of Pentacles', 'image': 'images/pentacles_eight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Nine of Pentacles', 'image': 'images/pentacles_nine.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Ten of Pentacles', 'image': 'images/pentacles_ten.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Page of Pentacles', 'image': 'images/pentacles_page.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Knight of Pentacles', 'image': 'images/pentacles_knight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Queen of Pentacles', 'image': 'images/pentacles_queen.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'King of Pentacles', 'image': 'images/pentacles_king.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
]




def index(request):
    context = {
        "cards" : CARD_LIST
    }
    return render(request, "tarot_app/tarot.html",context)


def register(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                birthday=request.POST['birthday'],
                email=request.POST['email'],
                password=pw_hash
            )
            request.session['user_id'] = new_user.id
            request.session['first_name'] = new_user.first_name
            request.session['email'] = new_user.email
            return render(request, 'welcome.html')


def welcome(request):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in!")
        return redirect ('/')
    return render(request,'welcome.html')


def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
        except:
            messages.error(request, "Either your email or password was input incorrectly.")
            return redirect('/')
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()): 
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            return redirect('/welcome')
        else:
            messages.error(
                request, "Either your email or password was input incorrectly.")
            return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
